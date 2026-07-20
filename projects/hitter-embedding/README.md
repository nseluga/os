---
name: Hitter Embedding
status: active
priority: high
last_active: 2026-07-20
next_step: "Phase B underway (B.1 stabilization done). Next: scaffold notebooks/02_feature_value.ipynb (common PA axis, clipped-spray check, signal-per-PA ranking), then B.2 GBM screening. Phase A /research-review still deferred — run before logging any Phase B finding."
repo: ~/hitter-embedding
github: https://github.com/nseluga/Hitter-Embedding
summary: "Conditional-query hitter embedding on Statcast process signals targeting platoon-skill identification and market mispricing; research target SSAC27, abstract due Oct 1."
tags: [ml, baseball, research]
---

## Where it stands

Phase A is complete and Phase B (feature-value stage) is underway; bat-tracking is excluded from v1. Phase A froze the 7.35M-pitch modeling table, the swing/contact/quality labels, and the walk-forward split. Phase B so far: the 48-dim context vectorizer (train-only fit), the complete-source wOBA eval-target table (FanGraphs weights sourced + reconciled to published league wOBA within ±0.0005), and the split-half stabilization estimator. B.1 result — process signals stabilize an order of magnitude faster than the outcome: whiff ~34 swings, EV ~34 BBIP, LA ~21 BBIP, spray ~77 BBIP vs side-specific wOBA ~407 PA. Next: write B.1 up in notebooks/02_feature_value.ipynb (common PA axis, clipped-spray check, signal-per-PA ranking), then B.2 GBM screening, then Phase C baselines before any model training. Note: the Phase A /research-review was deferred and must run before any Phase B result becomes a logged finding.

## Key files

- **Architecture spec:** `~/os/knowledge/library/baseball-research/Layer1_Architecture_Plan_v2.md` — canonical build order, frozen decisions (§5.13), evaluation protocol
- **Authority docs:** `~/os/knowledge/library/baseball-research/` — handoff v2, literature notes
- **Research docs:** `~/hitter-embedding/docs/` — decision-log, lab-notebook, research-manifest (gitignored)
- **Claude Code context:** `~/hitter-embedding/CLAUDE.md`
