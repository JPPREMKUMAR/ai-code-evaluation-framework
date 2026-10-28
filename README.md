# AI-Generated Code Evaluation and Automated Testing Framework

Specification-driven test runner for a small library of coding tasks and repository-owned candidate solutions. The web API accepts only task and candidate IDs from a fixed allowlist. It does not accept or execute arbitrary code.

Status: **Implemented, tested, and frontend build verified.** Not deployed or published to GitHub.

## Features

- Problem statement and explicit expected behavior.
- Normal, boundary, empty, duplicate, invalid, and larger-input cases.
- Timed subprocess worker, structured failures, SQLite run history, and JSON/HTML reports.
- Correct reference plus deliberately faulty boundary and empty-input candidates.
- Manual review dimensions for correctness, edge cases, complexity, readability, and spec adherence (see methodology).

## Security boundary

Only functions compiled into `app/worker.py` and names listed in `app/runner.py` can execute. The API does not accept source code, shell commands, arbitrary paths, or caller-provided arguments. `shell=False`, isolated Python mode, closed stdin, captured output, and a timeout are used as defense in depth. This is not an OS sandbox; never add arbitrary untrusted code execution without a real sandbox and resource limits.

## Run locally

Use Python 3.12 and Node.js 22 or compatible versions. Copy `.env.example` to `.env` if you need to change `DATABASE_PATH`; the default writes the local SQLite database. The dotenv file is loaded by the API and must remain uncommitted.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`. The React UI is in `frontend/`; use `npm ci` and `npm run dev` in a second terminal.

## Example workflow

Call `POST /api/evaluate` with `{"problem_id":"merge-intervals","candidate_id":"misses-touching"}`. The report shows a failed `touching-boundary` test. The reference candidate should pass all seven bundled cases. These are locally run synthetic examples, not benchmark evidence about general coding ability or any model.

Run the framework tests with `python -m pytest -q`. Build JSON/HTML from the CLI with `python -m app.cli --candidate reference --format json --output reports/run.json` or `--format html --output reports/run.html`. Tests verify known faulty candidates, invalid IDs, timeout reporting, and persisted human review scores. See `docs/evaluation-methodology.md`, `docs/security.md`, and `docs/test-report.md`.

## Limitations

The candidate functions are fixed and trusted, no arbitrary source upload is supported, wall-clock timing is environment dependent, and the sample suite is small. Any future code-upload feature requires a separate operating-system-level sandbox, memory/CPU/process limits, and security review.

See [`docs/requirements.md`](docs/requirements.md) for MVP acceptance criteria, [`docs/architecture.md`](docs/architecture.md) for data flow, [`docs/demo.md`](docs/demo.md) for a short walkthrough, [`docs/response-quality-examples.md`](docs/response-quality-examples.md) for labeled cases, and [`docs/deployment.md`](docs/deployment.md) for the current hosting assessment.

## License

MIT. See `LICENSE`.

