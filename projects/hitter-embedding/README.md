---
name: Hitter Embedding
status: active
priority: high
last_active: 2026-07-13
next_step: "Start Phase A — pull Statcast 2015–2025 via pybaseball, verify batted-ball spin field availability, build pitch-event table"
repo: ~/hitter-embedding
github: https://github.com/nseluga/Hitter-Embedding
summary: "Conditional-query hitter embedding on Statcast process signals targeting platoon-skill identification and market mispricing; research target SSAC27, abstract due Oct 1."
tags: [ml, baseball, research]
---

## Where it stands

Research scaffolding complete: repo initialized, `.gitignore`, root README, and `docs/` in place (decision-log and lab-notebook as blank templates). No code or data yet. Phase A is the immediate next step — pull the Statcast snapshot, verify batted-ball spin availability, build the pitch-event table, and freeze the walk-forward split config. Phases B (feature ablations) and C (baselines) follow before any model training begins.

## Key files

- **Architecture spec:** `~/os/knowledge/library/baseball-research/Layer1_Architecture_Plan_v2.md` — canonical build order, frozen decisions (§5.13), evaluation protocol
- **Authority docs:** `~/os/knowledge/library/baseball-research/` — handoff v2, literature notes
- **Research docs:** `~/hitter-embedding/docs/` — decision-log, lab-notebook, research-manifest (gitignored)
- **Claude Code context:** `~/hitter-embedding/CLAUDE.md`
