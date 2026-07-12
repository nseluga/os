---
name: os-evals
status: active
priority: medium
last_active: 2026-07-11
next_step: "Run full iterations to measure ablation ladder effectiveness"
repo: ~/os-evals
github: https://github.com/nseluga/os-evals
summary: "Ablation ladder that measures which layers of ~/os (CLAUDE.md, memory, skills) earn their keep."
tags: [meta, testing]
---

**Related:** measures which layers of the [os](../os/README.md) setup earn their keep via ablation.

## Where it stands

An optimization loop measuring the value stack: bare Claude → + CLAUDE.md → + memory → + skills. Two-sided check validation gate and exit-code convention (1 = fail, 2 = infra) in place. Active — most recent work is eval-harness fixes (meta.yaml parser).

## Run / verify

    cd ~/os-evals && ./run.sh      # 72 runs across 12 tasks × 4 rungs, plus an Opus-tier spot check

## Key files

- **SPEC.md** — complete design (local only; gitignored, not on GitHub).
- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- Eval-task fixtures under `tasks/` (incl. their own `PLAN.md`/`PROGRESS.md`) are part of the harness and **stay tracked on GitHub** — the gitignore is root-anchored so it only ignores root-level PLAN/PROGRESS/SPEC.
