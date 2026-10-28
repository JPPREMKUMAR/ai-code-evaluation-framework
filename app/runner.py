import json, subprocess, sys, time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
WORKER=ROOT/"app"/"worker.py"
PROBLEMS={"merge-intervals":ROOT/"data"/"merge-intervals.json"}
CANDIDATE_IDS={"reference","misses-touching","crashes-empty"}

def load_problem(problem_id:str):
    path=PROBLEMS.get(problem_id)
    if path is None: raise KeyError("Unknown problem")
    problem=json.loads(path.read_text(encoding="utf-8"))
    for case in problem["test_cases"]:
        if case["case_id"]=="large-overlap":
            case["input"]=[[i,i+1] for i in range(1000)]
            case["expected"]=[[0,1000]]
    return problem

def run_candidate(problem_id:str,candidate_id:str,case_input:list,timeout_seconds:float=2.0)->dict:
    if problem_id not in PROBLEMS: raise KeyError("Unknown problem")
    if candidate_id not in CANDIDATE_IDS: raise ValueError("Candidate is not in the trusted local allowlist")
    started=time.perf_counter()
    try:
        completed=subprocess.run([sys.executable,"-I",str(WORKER),problem_id,candidate_id],
                                 input=json.dumps(case_input),text=True,capture_output=True,
                                 timeout=timeout_seconds,shell=False,cwd=ROOT)
    except subprocess.TimeoutExpired:
        return {"status":"timeout","duration_ms":round((time.perf_counter()-started)*1000,2)}
    duration=round((time.perf_counter()-started)*1000,2)
    if completed.returncode!=0:
        return {"status":"worker_error","error":completed.stderr[-1000:],"duration_ms":duration}
    try: result=json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"status":"invalid_output","error":"Worker returned invalid JSON.","duration_ms":duration}
    return {"status":"ok",**result,"duration_ms":duration}

def evaluate_candidate(problem_id:str,candidate_id:str,timeout_seconds:float=2.0)->dict:
    problem=load_problem(problem_id);results=[]
    for case in problem["test_cases"]:
        actual=run_candidate(problem_id,candidate_id,case["input"],timeout_seconds)
        if case.get("expected_error"):
            passed=actual.get("error_type")==case["expected_error"]
        else:
            passed=actual.get("output")==case.get("expected") and actual.get("status")=="ok"
        results.append({"case_id":case["case_id"],"description":case["description"],"passed":passed,
                        "expected":case.get("expected",{"error":case.get("expected_error")}),"observed":actual})
    total=len(results);passed=sum(r["passed"] for r in results)
    return {"problem_id":problem_id,"candidate_id":candidate_id,"test_count":total,"passed_count":passed,
            "failed_count":total-passed,"pass_rate":round(passed/total,3) if total else None,"results":results,
            "limitation":"Results cover this fixed test set only; a pass is not proof of correctness."}
