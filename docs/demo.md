# Demonstration script

1. Start the API and frontend using the README.
2. Run the CLI reference candidate using the README command; inspect the JSON report.
3. In the UI, run `misses-touching` and `crashes-empty` for `merge-intervals`.
4. Compare the per-case failures with the task's closed-interval and empty-input specification.
5. Record a human review rationale and retrieve the JSON or HTML report.

**Expected behavior:** The trusted reference passes all seven curated tests. The boundary and empty-input mutants are detected on their named edge cases. This validates this small test suite, not all possible generated programs. No arbitrary code is accepted or executed.
