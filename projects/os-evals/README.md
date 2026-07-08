---
name: os-evals
status: active
priority: medium
last_active: 2026-07-07
next_step: "Run full iterations to measure ablation ladder effectiveness"
repo: ~/os-evals
github: https://github.com/nseluga/os-evals
summary: "Ablation ladder that measures which layers of ~/os (CLAUDE.md, memory, skills) earn their keep."
tags: [meta, testing]
---

An optimization loop measuring the value stack: bare Claude → + CLAUDE.md → + memory → + skills.

**How to run:** `cd ~/os-evals && ./run.sh` — executes 72 runs across 12 tasks × 4 rungs, plus Opus-tier spot check.

See [SPEC.md](../../os-evals/SPEC.md) for complete design.
