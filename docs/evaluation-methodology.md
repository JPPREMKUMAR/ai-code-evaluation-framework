# Evaluation rubric and interpretation

## Automated run

Each candidate runs against the same versioned interval-merge task and seven cases: normal overlap, touching boundary, empty input, duplicate intervals, unsorted/nested intervals, invalid reversed interval, and a generated 1,000-interval input. The closed-interval specification merges when the next start is less than or equal to the previous end.

The report includes number of cases, passes, failures, and a pass fraction. Pass fraction is `passed_count / test_count`, with the denominator shown. It measures only these cases, not overall correctness.

## Human review rubric (1–5)

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Correctness | Core output is wrong | Common cases work, some failures remain | Satisfies the specification across examined cases |
| Edge cases | Empty/boundary/invalid cases ignored | Some important edges covered | Relevant boundaries and invalid inputs handled explicitly |
| Complexity | Grossly inefficient for the stated task | Acceptable but not well justified | Appropriate asymptotic cost with clear trade-offs |
| Readability | Hard to follow | Understandable with friction | Clear names and simple structure |
| Specification adherence | Changes or misses requirements | Meets most requirements | Matches all stated behavior and error handling |

Write a rationale tied to a failing or passing case and the specification. Do not allow readability or a high average to hide a correctness failure.

## Known defects

- `misses-touching` uses a strict comparison and fails the endpoint-touching case.
- `crashes-empty` indexes the first item and fails empty input.
- `reference` is the bundled expected implementation and should pass this fixed suite.

These tests demonstrate that known mutations are detectable; they do not prove the test suite is complete.
