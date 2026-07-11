---
name: project-os-evals-standards
description: "Process standards for the os-evals harness — check validation gates, infra failure codes, and task selection rules"
metadata: 
  node_type: memory
  type: project
  originSessionId: 6fb20f4c-aeb2-47d6-9527-611f83aca7e8
---

Standards established for the os-evals evaluation harness. Apply these when authoring new tasks, writing check.sh scripts, or extending the harness.

**Two-sided validation gate:** Every check.sh must be validated against both a correct solution (should pass) AND a deliberately broken solution (should fail) before being trusted in the matrix. A check only validated on one side is marked NEEDS-VALIDATION and must not be promoted to the run matrix. **Why:** a check that always passes regardless of answer quality inflates scores silently; one-sided validation misses this. **How to apply:** before adding any check to the task suite, run it against the golden answer and against a known-wrong answer; only promote when both fire correctly.

**Exit code convention:** exit 1 = genuine task failure (model got it wrong); exit 2 = infra failure (server not running, missing binary, timeout). The distinction is critical for interpreting the result matrix — an exit 2 means the task is unevaluable in that rung, not that the model failed.

**Eval result as of 2026-07-09 (Sonnet 4.5, 48-task suite):** CLAUDE.md +2 tasks; memory layer -1 net (regression); skills +1 more. Hard coding tasks (dashboard-digest boundary logic, pir-workload ACWR time-window) failed at every rung including Opus+skills — these tasks may need rephrasing or are genuinely beyond current scaffolding. See [[dev-team-learnings]] for related harness lessons.

**Multi-turn harness convention (commit cb19c01):** a task runs multi-turn iff meta.yaml has `multi_turn: true` (NOT merely a non-default `timeout_sec`). Multi-turn → `--output-format stream-json --verbose`, git-init'd workspace (so dev-team/dev-team-auto can branch/worktree), a `{run}.trace.jsonl`, and `curated_skill`-driven skill-activation detection recorded as `_meta.skill_fired` (True/False/None). `timeout_sec` defaults 300; dev-team-auto tasks set ~1800. find_tasks() skips any path segment starting with `_`, so `tasks/_draft/` is auto-excluded from the scored suite.

**Caution (found 2026-07-11):** cb19c01's commit message claims "unit tests for all pure functions" were verified, but those tests were never committed (not in the tree). The four pure fns (detect_skill_fired, _parse_stream incl. truncation, looks_like_auth_error, read_task_meta) were re-verified via a re-derived test — all pass — but the repo has no standing test file for them. **How to apply:** don't trust "verified" claims in os-evals commit messages without confirming the test artifact exists; consider adding a committed harness/ test.

**Hard-task batch #1 (2026-07-11, branch worktree-draft-hard-tasks, unapproved):** two draft tasks under `tasks/_draft/coding/` — `pathguard-resolver` (dev-team, security battery) and `rangestats-engine` (dev-team-auto, PLAN.md-driven, perf+scalability via SIGALRM budget). Both two-sided validated. Await Nate's per-check approval before promotion.
