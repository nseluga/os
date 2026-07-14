---
name: os-evals
status: active
priority: medium
last_active: 2026-07-13
next_step: "Interpret ablation sign-test results (most comparisons are ties — decide whether to prune rungs or redesign low-signal tasks)"
repo: ~/os-evals
github: https://github.com/nseluga/os-evals
summary: "Ablation ladder that measures which layers of ~/os (CLAUDE.md, memory, skills) earn their keep."
tags: [meta, testing]
---

**Related:** measures which layers of the [os](../os/README.md) setup earn their keep via ablation.

## Where it stands

Full 14-task × 4-rung suite running. Latest scorecard (2026-07-13, SHA b612249, 60 runs): rung pass rates are 14/16, 12/14, 12/14, 15/16. Hard tasks batch #1 (pathguard-resolver, rangestats-engine) promoted from draft and passing. Persistent failures: `coding/dashboard-digest` fails all rungs; `writing/portfolio-writeup` is inconsistent (rung1/rung3 fail). Sign-test shows most ablation comparisons are ties (≤1 non-tie win per ladder step), suggesting individual layers add minimal marginal value on the current task set — the signal question is whether to redesign tasks or prune rungs.

## Run / verify

    cd ~/os-evals && ./run.sh      # 72 runs across 12 tasks × 4 rungs, plus an Opus-tier spot check

## Key files

- **SPEC.md** — complete design (local only; gitignored, not on GitHub).
- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- Eval-task fixtures under `tasks/` (incl. their own `PLAN.md`/`PROGRESS.md`) are part of the harness and **stay tracked on GitHub** — the gitignore is root-anchored so it only ignores root-level PLAN/PROGRESS/SPEC.
