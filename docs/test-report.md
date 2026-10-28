# Test report — 2026-10-28

Environment: Windows host, bundled Python 3.12.14, pytest 8.3.5, Node.js 22, npm 10.9.x, Vite 6.4.5.

| Check | Result | Evidence |
|---|---|---|
| Backend unit / runner tests | **7 passed, 0 failed, 0 skipped** | `python -m pytest -q` |
| Reference candidate | **7/7 passed** | Automated suite, including 1,000 generated intervals |
| Known faulty candidates | **Detected** | Boundary mutant and empty-input mutant each fail their intended edge case |
| Allowlist and timeout | **Passed** | Unknown code-like candidate ID rejected; short timeout reported as timeout |
| Frontend production build | **Passed** | `npm run build`; TypeScript and Vite succeeded |
| Lint / type check | **No separate lint configured; TypeScript type check passed** | `tsc -b` runs as part of the production build; no Python static type checker is configured |
| API live smoke check | **Passed** | Reference 7/7; boundary mutant 5/7; review saved; HTML report returned HTTP 200 |
| Manual browser workflow | **Passed at the current browser viewport** | Loaded the task and trusted candidates, ran the reference, and rendered all seven passing cases and JSON/HTML report links |
| Deployment / GitHub publication | **Not done** | No deployment; local repository is committed, but remote repository creation and push remain pending |

No arbitrary candidate source was executed. The generated large case and millisecond timings are local test mechanics, not a general performance benchmark. One smoke-check revision exposed that the stored JSON omitted its run ID; the persistence logic now writes that identifier into the report as well.

Known gaps: no systematic desktop/mobile breakpoint matrix or deployed smoke test has been completed.
