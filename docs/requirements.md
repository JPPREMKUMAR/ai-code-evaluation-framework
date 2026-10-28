# Product requirements and acceptance criteria

## Problem and users

Reviewers need repeatable tests that catch common coding defects and reports that explain which specification cases failed. Users are coding evaluators, mentors, and developers inspecting generated code.

## MVP behavior

1. Maintain a small library of task specifications, trusted reference solutions, and known faulty candidates.
2. Exercise normal, boundary, empty, duplicate, invalid, and larger inputs.
3. Run only repository-owned, allowlisted functions in a bounded subprocess and persist run history.
4. Export JSON/HTML reports and provide a CLI, FastAPI API, and React interface.
5. Capture human ratings for correctness, edge cases, complexity, readability, and specification adherence.

## Acceptance checks

- Reference implementation passes the curated suite; mutants fail their intended cases.
- Unknown candidate IDs are rejected; timeout handling is tested.
- API never accepts caller-supplied source code, shell commands, or arbitrary paths.
- Reports include per-test outcomes; tests and frontend build pass.

## Risks and limits

The subprocess is defense in depth, not an operating-system sandbox. Do not expose arbitrary untrusted code execution. The sample timing and generated input validate mechanics only and are not general performance claims. Authentication is not implemented.
