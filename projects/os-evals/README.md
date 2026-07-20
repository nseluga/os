---
name: os-evals
status: on-hold
priority: low
last_active: 2026-07-15
next_step: "Promote validated draft tasks (memory-notes-format, claude-md-comment-gate) from _draft/ into live suite, then run ./run.sh for iteration 4 to see if discrimination is restored"
repo: ~/os-evals
github: https://github.com/nseluga/os-evals
summary: "Ablation ladder that measures which layers of ~/os (CLAUDE.md, memory, skills) earn their keep."
tags: [meta, testing]
---

**Related:** measures which layers of the [os](../os/README.md) setup earn their keep via ablation.

## Where it stands

Iteration 3 (2026-07-15, main @ 64218dd) **flatlined** — all 13 tasks pass at every rung, zero discriminating signal, +0 layer attribution across all four rung pairs. Bare Sonnet 4.6 passes everything. Batch-2 dev-team-auto session landed four fixes: `pir-workload-feature` rung1 timeout fixed (`multi_turn: true` + 900s), Opus spot check wired by default (`OPUS_SPOTCHECK=1`), loud ⚠️ no-signal verdict added to `stats.py`, and two validated discriminating task drafts in `tasks/_draft/knowledge/` (`memory-notes-format` and `claude-md-comment-gate` — both rung1→rung2 discriminating; `memory-tradeoffs-reflex` cut for non-discrimination). The two validated drafts need user promotion into the live suite before running iteration 4.

## Run / verify

    cd ~/os-evals && ./run.sh      # full matrix: Sonnet rungs 1-4 + Opus spot check (rungs 1,4)

## Key files

- **SPEC.md** — complete design (local only; gitignored, not on GitHub).
- **PLAN.md / PROGRESS.md** (repo root) — local, gitignored trackers.
- Eval-task fixtures under `tasks/` (incl. their own `PLAN.md`/`PROGRESS.md`) are part of the harness and **stay tracked on GitHub** — the gitignore is root-anchored so it only ignores root-level PLAN/PROGRESS/SPEC.
