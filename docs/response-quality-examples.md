# Response-quality examples

The evaluator executes only repository-owned allowlisted candidates. The malformed/incomplete samples below are review illustrations and are never submitted to the subprocess runner as arbitrary source.

| Category | Candidate behavior or specification issue | Evaluation |
|---|---|---|
| Correct | Bundled `reference` candidate merges closed intervals, including touching endpoints, sorts input, rejects reversed intervals, and handles empty input. | Expected result: 7/7 curated tests pass. |
| Incorrect | `misses-touching` fails to merge `[1,2]` and `[2,4]`. | The named boundary case fails against the closed-interval specification. |
| Incomplete | A hypothetical solution processes only the first interval and ignores the rest. | Mark missing required behavior; it is not included in the executable candidate allowlist. |
| Misleading | A hypothetical nested-loop implementation returns correct answers but claims its complexity is O(n log n). | Separate functional correctness from complexity rationale; do not accept the unsupported complexity claim. |
| Ambiguous | A hypothetical prompt says “merge overlapping intervals” but never states whether touching closed endpoints merge. | Request a specification decision; do not invent an expected output. The bundled task explicitly says closed intervals that touch are merged. |
| Poorly formatted | A hypothetical source string has a syntax error. | Reject as an untrusted/non-allowlisted candidate; do not run it. A future upload feature would require a real sandbox. |

Use expected/observed values and case IDs in written feedback. A pass means only that the fixed test cases passed; it is not proof of general correctness.
