import html,json
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from app.models import CodeReview,RunRequest
from app import storage
from app.runner import CANDIDATE_IDS,evaluate_candidate,load_problem

app=FastAPI(title="AI-Generated Code Evaluation Framework",version="0.1.0",
            description="Runs only bundled allowlisted candidates in a timed local worker; arbitrary code is not accepted.")
storage.initialize()

@app.get("/api/health")
def health():return {"status":"ok"}

@app.get("/api/problems")
def problems():return [{k:v for k,v in load_problem(pid).items() if k!="test_cases"}|{"problem_id":pid} for pid in ["merge-intervals"]]

@app.get("/api/candidates")
def candidates():return [{"candidate_id":"reference","label":"Reference solution","notes":"Trusted baseline; expected to pass the specified examples."},{"candidate_id":"misses-touching","label":"Boundary mutant","notes":"Merges overlaps but mishandles intervals that meet at an endpoint."},{"candidate_id":"crashes-empty","label":"Empty-input mutant","notes":"Assumes a first element exists."}]

@app.post("/api/evaluate")
def evaluate(payload:RunRequest):
    try:report=evaluate_candidate(payload.problem_id,payload.candidate_id)
    except KeyError as exc:raise HTTPException(404,str(exc)) from exc
    except ValueError as exc:raise HTTPException(400,str(exc)) from exc
    report["run_id"]=storage.save(report);return report

@app.get("/api/history")
def history():return [{k:v for k,v in row.items() if k!="report_json"}|{"report":json.loads(row["report_json"])} for row in storage.history()]

@app.patch("/api/runs/{run_id}/review")
def save_review(run_id:int,payload:CodeReview):
    if not storage.update_review(run_id,payload.model_dump()):raise HTTPException(404,"Run not found")
    return {"saved":True,"run_id":run_id}

@app.get("/api/reports/{run_id}.json")
def json_report(run_id:int):
    row=next((r for r in storage.history(1000) if r["id"]==run_id),None)
    if not row:raise HTTPException(404,"Run report not found")
    return json.loads(row["report_json"])

@app.get("/api/reports/{run_id}.html",response_class=HTMLResponse)
def html_report(run_id:int):
    row=next((r for r in storage.history(1000) if r["id"]==run_id),None)
    if not row:raise HTTPException(404,"Run report not found")
    report=json.loads(row["report_json"]);rows="".join(f"<tr><td>{html.escape(r['case_id'])}</td><td>{'PASS' if r['passed'] else 'FAIL'}</td><td><pre>{html.escape(json.dumps(r['observed'],indent=2))}</pre></td></tr>" for r in report["results"])
    return f"<!doctype html><meta charset='utf-8'><title>Run {run_id}</title><h1>Code evaluation run {run_id}</h1><p>{html.escape(report['candidate_id'])}: {report['passed_count']}/{report['test_count']} passed</p><table><thead><tr><th>Case</th><th>Result</th><th>Observed</th></tr></thead><tbody>{rows}</tbody></table>"
