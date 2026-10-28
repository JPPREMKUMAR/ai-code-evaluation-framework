# Security and execution boundary

- No source code or shell command is accepted from the API or UI.
- The runner permits only a fixed problem ID and candidate IDs from a Python allowlist.
- The child process runs a repository-owned worker with isolated Python mode, `shell=False`, JSON-only arguments, captured output, and a timeout.
- Inputs are drawn from the repository's fixed test bank; user-provided test values are not passed to the worker.
- Candidate functions are small and bundled with the project. This is a constrained process runner, not a hardened operating-system sandbox.

Do not expose untrusted code execution publicly. If a future feature accepts code, isolate it in a proper sandbox with CPU, memory, process, filesystem, network, and output limits and perform a separate security review.
