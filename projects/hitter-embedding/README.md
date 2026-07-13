---
name: Hitter Embedding
status: active
priority: high
last_active: 2026-07-09
next_step: "Complete Phase A data foundation (Statcast snapshot, feature engineering, walk-forward config frozen) → launch Phase B feature-value ablations"
repo: ~/hitter-embedding
github: null
summary: "Deep-learning hitter representation model on process signals (Layer 1) + platoon-skill market-value framework (Layer 2). Research target: SSAC27, abstract due Oct 1."
tags: [ml, baseball, research]
---

## Context

Supervised representation learning project targeting MIT Sloan Sports Analytics Conference (SSAC27). Core thesis: process-signal embedding can identify and value hitters with suppressed market prices due to exploitable platoon splits.

Two-layer architecture:
- **Layer 1:** Conditional-query model p(process outcome | hitter, pitch context) trained on Statcast 2015–2025
- **Layer 2:** Platoon-skill query framework + economics backtest (market mispricing identification)

## Authority Documents

- **Layer 1 Architecture Plan (v2):** `~/os/knowledge/library/baseball-research/Layer1_Architecture_Plan_v2.md` — canonical specification, frozen decision log (§5.13), non-negotiable rules (§2)
- **Project Handoff (v2):** `~/os/knowledge/library/baseball-research/` — framing, Layer 2 scope, cross-layer open items
- **Claude Code Context:** `/Users/nateseluga/hitter-embedding/docs/` and this project index
- **Research Manifest:** `~/hitter-embedding/docs/research-manifest.md` — config for `/research-partner` and `/research-review` (staged copy in [research-manifest.md](research-manifest.md) until moved into the repo)

## Non-Negotiable Rules

1. **Baseline-first gate:** No deep-learning claim without beating bucketed averages, XGBoost, and empirical-Bayes platoon regression out-of-sample, especially in low-exposure strata
2. **Ablation-decided:** Every unclear choice settled by ablation on claim-1 metric; negative results kept and reported
3. **Frozen walk-forward splits:** Season splits frozen in config before any model comparison; flag leakage immediately
4. **No luck/price/salary leakage into Layer 1:** Never train on outcome luck or market prices

## Build Order (Phase Sequence)

**Phase A — Data foundation** (start immediately)  
- Statcast snapshot (2015–2025, frozen versioning)
- Verify batted-ball spin field availability; derive spray angle
- Pitch-event table: context features + swing/contact/quality labels
- Freeze walk-forward split config

**Phase B — Feature-value stage** (decides bat-tracking placement, outcome dimensions)  
- Reliability/stabilization analysis
- XGBoost GBM screening (permutation importance, SHAP)
- Common-window ablations (with/without bat tracking)

**Phase C — Baselines** (before any DL training)  
- Bucketed trailing averages
- Empirical-Bayes platoon regression
- XGBoost with interaction features

**Phase D — v1 model training** (per architecture spec)  
- 5-seed deep ensemble

**Phase E — Checkpoints & evaluation**  
- Probe checkpoint (early go/no-go)
- Claim-1 evaluation (stratified by prior exposure)
- Composition validation, calibration check

**Phase F — Gated v2 upgrades** (history encoder, pitcher-ID residual)  
- Only if their specific gates fire

**Phase G — Layer 2 handoff**  
- Query library for candidacy/mispricing code

## Open Cross-Layer Items

- **WAR-conversion assumption** (Phase 0): How often a candidate gets their strong-side matchup — needed before economics pipeline closes
- **Sequence-architecture gap:** Heaton & Mitra (2023) and Melville et al. (RNN) need fresh reads
- **BERT-style self-supervised alternative:** Formally deferred to future work
- **Contrastive learning:** Formally deferred (as primary objective risks manufacturing the archetype hypothesis)

## Key Principles (Settled)

- Market inefficiency = measurement-and-identification problem, not team ignorance
- Validation uses only free-agent contract prices; team-controlled players never validation targets (avoids monopsony confound)
- Archetype-cluster hypothesis is testable, not assumed; trait-direction fallback if no cluster structure emerges
- Measurement confound (Powers & Yurko) acknowledged as open for subgroup case; mitigated via count/location conditioning
- Competing salary drivers (defense, position scarcity, durability) are a confound gap; Krautmann's critique of Scully-style MRP estimates is the resource

## Standing Risks

- Interaction-learning failure → mitigated by probe checkpoint + bilinear ablation
- Deployment/selection bias → mitigated by audit + natural-experiment evaluation
- Ensemble calibration on very-low-exposure hitters → assumed until checked; expensive fallback if it fails
- Honest prior: empirical Bayes is genuinely hard to beat in low-exposure strata; clean finding if it wins

## Tools & Compute

- **Stack:** PyTorch, W&B or MLflow, seeded config-driven runs, unit-tested data pipeline
- **Scale:** <1M parameters, 7–8M pitches, no distributed training
- **Estimated compute:** <$200 total (Colab Pro or rented A10/T4)
- **Collaborate:** Economics partner owns Layer 2 (seven-phase salary modeling → backtest)
