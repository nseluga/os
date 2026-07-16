---
name: Hitter Embedding
status: active
priority: high
last_active: 2026-07-15
next_step: "Phase A: freeze the walk-forward split config, then build the label and feature-derivation module. Cleaning pipeline complete."
repo: ~/hitter-embedding
github: https://github.com/nseluga/Hitter-Embedding
summary: "Conditional-query hitter embedding on Statcast process signals targeting platoon-skill identification and market mispricing; research target SSAC27, abstract due Oct 1."
tags: [ml, baseball, research]
---

## Where it stands

Phase A is underway. The 2015–2025 Statcast snapshot is pulled and frozen to versioned parquet (7.80M pitches); batted-ball spin was verified unavailable, so the contact-quality space is EV/LA/spray; and the cleaning pipeline is built and unit-tested, producing a 7.35M-pitch modeling table. Remaining in Phase A: freeze the walk-forward split config and build the label and feature-derivation module. Phases B (feature ablations) and C (baselines) follow before any model training begins.

## Key files

- **Architecture spec:** `~/os/knowledge/library/baseball-research/Layer1_Architecture_Plan_v2.md` — canonical build order, frozen decisions (§5.13), evaluation protocol
- **Authority docs:** `~/os/knowledge/library/baseball-research/` — handoff v2, literature notes
- **Research docs:** `~/hitter-embedding/docs/` — decision-log, lab-notebook, research-manifest (gitignored)
- **Claude Code context:** `~/hitter-embedding/CLAUDE.md`
