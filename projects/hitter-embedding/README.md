---
name: Hitter Embedding
status: active
priority: high
last_active: 2026-07-21
next_step: "B.1 complete and banked to results/phase_b/ (no notebook — logic is in tested code). Next: run deferred Phase A /research-review, then B.2 GBM feature screening (XGBoost + SHAP on the 48 context features vs process outcomes, frozen split). Open: spray label decision (drop |spray|>90 vs keep) — evidence in, Nate's call."
repo: ~/hitter-embedding
github: https://github.com/nseluga/Hitter-Embedding
summary: "Conditional-query hitter embedding on Statcast process signals targeting platoon-skill identification and market mispricing; research target SSAC27, abstract due Oct 1."
tags: [ml, baseball, research]
---

## Where it stands

Phase A is complete and Phase B (feature-value stage) is underway; bat-tracking is excluded from v1. Phase A froze the 7.35M-pitch modeling table, the swing/contact/quality labels, and the walk-forward split. Phase B so far: the 48-dim context vectorizer (train-only fit), the complete-source wOBA eval-target table (FanGraphs weights sourced + reconciled to published league wOBA within ±0.0005), and the stabilization estimator — now hardened with a variance-components estimator (bootstrap CIs, all-hitter signal/noise decomposition) and a sequential-split mode alongside split-half (70 tests pass).

**B.1 complete**, results banked to `results/phase_b/` (CSVs + figures; no notebook — the logic is in the tested module, so a notebook would only re-paste it). Corrected finding: process stabilizes **several-fold faster than the outcome, not an order of magnitude** — on a common PA axis, whiff ~28 PA-equiv (~7×), swing ~31, LA ~62, EV ~63 (~3×), spray ~122 (~1.6×) vs side-specific wOBA ~190–198 PA. The earlier ~407 PA outcome figure was survivorship-inflated: split-half at large n only uses durable hitters, whose skill spread is compressed; the variance-components estimator on all hitters halves that to ~190 (the divergence is population, not estimator — the two agree on a fixed population). Matched side-specific process stays fast (whiff vs LHP 45 ≈ pooled 51). Spray remains the laggard; clipping the ~1% near-plate artifact barely helps.

Next: run the deferred Phase A `/research-review` (gates promoting B.1 to a logged finding), then B.2 GBM feature screening, then Phase C baselines before any model training.

## Key files

- **Architecture spec:** `~/os/knowledge/library/baseball-research/Layer1_Architecture_Plan_v2.md` — canonical build order, frozen decisions (§5.13), evaluation protocol
- **Authority docs:** `~/os/knowledge/library/baseball-research/` — handoff v2, literature notes
- **Research docs:** `~/hitter-embedding/docs/` — decision-log, lab-notebook, research-manifest (gitignored)
- **Claude Code context:** `~/hitter-embedding/CLAUDE.md`
