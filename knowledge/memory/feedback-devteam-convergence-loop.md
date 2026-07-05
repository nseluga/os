---
name: feedback-devteam-convergence-loop
description: dev-team and dev-team-auto must work as converge-until-working loops per plan item (build → QA test gate → review → fix, repeat), not linear one-pass pipelines
metadata:
  type: feedback
---

The dev-team skills are **convergence loops**, not linear pipelines. Each plan item is driven through a loop — Engineer builds, `dt-qa` gates it with a binary `VERDICT: PASS/FAIL`, `dt-review` reviews once QA is green, `dt-fix` applies findings — and the loop repeats until the item works as specified (QA PASS + zero Critical/Important review findings) or hits a 5-attempt cap (then BLOCKED). Shared engine lives in `skills/dev-team/convergence-loop.md`; the `dt-qa` agent is the gate. See [[feedback-devteam-auto-merge]] for the auto-run shutdown behavior.

**Why:** Nate explicitly wanted every plan aspect implemented, tested, quality-reviewed, and bug-fixed iteratively until working — not run once and hoped-for. The Optimization Reviewer must run on *every* implemented item, at the point after it passes its correctness gate. `dev-team` (interactive, one item) uses gate mode `tests`; `dev-team-auto` (overnight, all items) uses the stronger `tests+behavioral`.

**How to apply:** When editing these skills, preserve the loop shape and the QA-gate-before-done invariant — don't collapse them back to a single Engineer→Review→Fix pass. Correctness gate (QA) runs before the quality gate (Review) to avoid optimizing broken code.

**Design-level failure handling (important):** On a design-level QA failure, do NOT re-design from scratch on the same branch. Instead, spawn up to 2 alternative engineers — each forks a new branch from the current item branch (e.g. `feat/x-alt-1`), tries a structurally different approach for the failing criterion, and is immediately QA-gated. The original branch is untouched. The first alternative that passes QA becomes the `winning_branch` passed to all subsequent agents. Failed alt branches can be discarded. If no alternative passes, one outer attempt is consumed and the loop continues. The Bug Fixer handles bug-level failures (no branching needed). Note: this project (Patio) starts with near-zero test coverage, so early `dt-qa` runs build test infra as they go.
