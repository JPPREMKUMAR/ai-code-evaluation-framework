import argparse,html,json
from pathlib import Path
from app.runner import evaluate_candidate

def main():
    parser=argparse.ArgumentParser(description="Run a trusted, bundled code candidate against its fixed test suite.")
    parser.add_argument("--problem",default="merge-intervals")
    parser.add_argument("--candidate",choices=["reference","misses-touching","crashes-empty"],required=True)
    parser.add_argument("--format",choices=["json","html"],default="json")
    parser.add_argument("--output",default="reports/run.json")
    args=parser.parse_args();report=evaluate_candidate(args.problem,args.candidate)
    path=Path(args.output);path.parent.mkdir(parents=True,exist_ok=True)
    if args.format=="json":
        path.write_text(json.dumps(report,indent=2),encoding="utf-8")
    else:
        rows="".join(f"<tr><td>{html.escape(r['case_id'])}</td><td>{'PASS' if r['passed'] else 'FAIL'}</td><td><pre>{html.escape(json.dumps(r['observed'],indent=2))}</pre></td></tr>" for r in report["results"])
        path.write_text(f"<!doctype html><meta charset='utf-8'><h1>{html.escape(args.candidate)}</h1><p>{report['passed_count']}/{report['test_count']} passed</p><table>{rows}</table>",encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("problem_id","candidate_id","test_count","passed_count","failed_count","pass_rate")},indent=2))

if __name__=="__main__":main()
