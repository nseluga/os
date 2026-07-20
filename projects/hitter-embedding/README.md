---
name: Hitter Embedding
status: active
priority: high
last_active: 2026-07-17
next_step: "Phase A complete. Run /research-review on Phase A, then start Phase B (feature-value stage: stabilization, GBM screening, bat-tracking placement, outcome-dimension ablations)."
repo: ~/hitter-embedding
github: https://github.com/nseluga/Hitter-Embedding
summary: "Conditional-query hitter embedding on Statcast process signals targeting platoon-skill identification and market mispricing; research target SSAC27, abstract due Oct 1."
tags: [ml, baseball, research]
---

## Where it stands

Phase A is complete. The 2015–2025 Statcast snapshot is pulled and frozen to versioned parquet (7.80M pitches); batted-ball spin was verified unavailable, so the contact-quality space is EV/LA/spray; the cleaning pipeline produces a 7.35M-pitch modeling table; the label module derives the swing/contact/quality process-head targets (in-play-only quality masking, three-source-sourced spray angle) into pitch_events_labeled.parquet; and the walk-forward split (train 2015–2023 / val 2024 / test 2025) is frozen and validated in config. Next: /research-review on Phase A, then Phase B (feature ablations), then Phase C (baselines) before any model training begins.

## Key files

- **Architecture spec:** `~/os/knowledge/library/baseball-research/Layer1_Architecture_Plan_v2.md` — canonical build order, frozen decisions (§5.13), evaluation protocol
- **Authority docs:** `~/os/knowledge/library/baseball-research/` — handoff v2, literature notes
- **Research docs:** `~/hitter-embedding/docs/` — decision-log, lab-notebook, research-manifest (gitignored)
- **Claude Code context:** `~/hitter-embedding/CLAUDE.md`
