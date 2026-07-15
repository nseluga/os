---
name: os-evals
status: active
priority: medium
last_active: 2026-07-14
next_step: "Run iteration 3 (./run.sh) and verify: ~73 runs, dashboard-digest in Difficulty Anchors only, portfolio-writeup rung3 passes, (K/3) annotations for noisy tasks"
repo: ~/os-evals
github: https://github.com/nseluga/os-evals
summary: "Ablation ladder that measures which layers of ~/os (CLAUDE.md, memory, skills) earn their keep."
tags: [meta, testing]
---

**Related:** measures which layers of the [os](../os/README.md) setup earn their keep via ablation.

## Where it stands

All five iteration-2 defects fixed (2026-07-14, main @ 7184de4): stale transcript cleanup, `dashboard-digest` sentinel (rung-1 only + Difficulty Anchors scorecard section), portfolio-writeup `"elevate"` false positive removed, `repeat: 3` majority-vote for noisy tasks (`portfolio-writeup`, `pir-workload-feature`), and unit tests for three harness pure functions. Iteration 3 will be the first clean run: expected ~73 transcripts (13 tasks × 4 rungs + 2 noisy tasks × 2 extra repeats × 4 rungs), `dashboard-digest` absent from main table, `portfolio-writeup` rung3 expected to pass.

## Run / verify

    cd ~/os-evals && ./run.sh      # 72 runs across 12 tasks × 4 rungs, plus an Opus-tier spot check

## Key files

- **SPEC.md** — complete design (local only; gitignored, not on GitHub).
- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- Eval-task fixtures under `tasks/` (incl. their own `PLAN.md`/`PROGRESS.md`) are part of the harness and **stay tracked on GitHub** — the gitignore is root-anchored so it only ignores root-level PLAN/PROGRESS/SPEC.
