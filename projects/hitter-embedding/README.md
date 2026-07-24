---
name: Hitter Embedding
status: active
priority: high
last_active: 2026-07-22
next_step: "B.2 GBM feature screen DONE (5 XGBoost heads through the frozen split; 10 keep / 6 flag — spin + fine-release features flag as redundant, joint-drop deferred to Phase D ablation). Spray label clipped (|spray|>90 nulled, ~0.94%, parquet regenerated). B.3–B.5 moot (bat-tracking out of v1), B.6 satisfied by construction → Phase B done. Next: run deferred Phase A+B /research-review (gates promoting B.1+B.2 to logged findings), then Phase C baselines (bucketed trailing avg, empirical-Bayes The Book [read source first], XGBoost context-interaction) before any DL. B.1+B.2 provisional until review."
repo: ~/hitter-embedding
github: https://github.com/nseluga/Hitter-Embedding
summary: "Conditional-query hitter embedding on Statcast process signals targeting platoon-skill identification and market mispricing; research target SSAC27, abstract due Oct 1."
tags: [ml, baseball, research]
---

## Where it stands

Phase A is complete and Phase B (feature-value stage) is underway; bat-tracking is excluded from v1. Phase A froze the 7.35M-pitch modeling table, the swing/contact/quality labels, and the walk-forward split. Phase B so far: the 48-dim context vectorizer (train-only fit), the complete-source wOBA eval-target table (FanGraphs weights sourced + reconciled to published league wOBA within ±0.0005), and the stabilization estimator — now hardened with a variance-components estimator (bootstrap CIs, all-hitter signal/noise decomposition) and a sequential-split mode alongside split-half (70 tests pass).

**B.1 complete**, results banked to `results/phase_b/` (CSVs + figures; no notebook — the logic is in the tested module, so a notebook would only re-paste it). Corrected finding: process stabilizes **several-fold faster than the outcome, not an order of magnitude** — on a common PA axis, whiff ~28 PA-equiv (~7×), swing ~31, LA ~62, EV ~63 (~3×), spray ~122 (~1.6×) vs side-specific wOBA ~190–198 PA. The earlier ~407 PA outcome figure was survivorship-inflated: split-half at large n only uses durable hitters, whose skill spread is compressed; the variance-components estimator on all hitters halves that to ~190 (the divergence is population, not estimator — the two agree on a fixed population). Matched side-specific process stays fast (whiff vs LHP 45 ≈ pooled 51). Spray remains the laggard; clipping the ~1% near-plate artifact barely helps.

**B.2 complete** (`src/analysis/b2_screen.py`, results in `results/phase_b/b2_*`). Five XGBoost heads (swing/whiff/EV/LA/spray) screened on the exact 48-dim context vector through the frozen split — trained on ≤2023, early-stopped on val 2024, test 2025 never touched; grouped permutation importance + SHAP on val. All ml-engineer gates passed on the full 7.35M table. Verdict is a **triage, not a decision**: 10 features keep, 6 flag (effective_speed, spin_axis, release_spin_rate, release_pos_y/z, release_extension) — the spin flags corroborate the Phase A Magnus spin↔movement redundancy. Because permutation importance is redundancy-blind, the flags are candidates for a Phase D joint-drop ablation (§4), not proven dead. Separately, the **spray label was clipped** (|spray|>90 near-plate artifact nulled, 12,020 rows / 0.94%; EV/LA retained; parquet regenerated, vectorizer params byte-identical) — physical justification (fair balls lie in the foul-line wedge), not the small n\* gain.

B.3–B.5 (bat-tracking placement) are moot with bat-tracking out of v1; B.6 (intent-confound guardrail) is satisfied by construction (count + location in the context vector), so **Phase B is effectively complete**. A scratch stabilization check (not banked) confirmed swing mechanics stabilize in tens of swings (bat_speed ~7 vs whiff ~53), quantifying the gated v2 history-encoder upside without committing to it.

Next: run the deferred Phase A + B `/research-review` (gates promoting B.1 and B.2 to logged findings), then Phase C baselines (bucketed side-specific trailing averages, empirical-Bayes platoon regression — read The Book directly first, XGBoost with context-interaction features) before any model training.

## Key files

- **Architecture spec:** `~/os/knowledge/library/baseball-research/Layer1_Architecture_Plan_v2.md` — canonical build order, frozen decisions (§5.13), evaluation protocol
- **Authority docs:** `~/os/knowledge/library/baseball-research/` — handoff v2, literature notes
- **Research docs:** `~/hitter-embedding/docs/` — decision-log, lab-notebook, research-manifest (gitignored)
- **Claude Code context:** `~/hitter-embedding/CLAUDE.md`

Related: [[projects/pitcher-injury-risk/README|pitcher-injury-risk]] · [[projects/batting-average-ability/README|batting-average-ability]] · [[research-standards]] · [[notebook-code-standards]]
