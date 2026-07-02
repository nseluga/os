# Pitcher Injury Risk

**Repo:** `~/Pitcher-Injury-Risk`  
**GitHub:** https://github.com/nseluga/Pitcher-Injury-Risk  
**Status:** active

One-line purpose: Multi-dimensional MLB pitcher health modeling platform — predicts injury probability, severity, and time-to-injury; produces normalized **Injury Risk+** composite score; enables counterfactual usage-strategy analysis.

## Overview

A research-grade project framed around five core questions:
1. **When** will a pitcher get injured?
2. **How severe** will it be?
3. **How long** until recovery?
4. **What factors** drive risk?
5. **How can usage strategies be optimized** to reduce risk proactively?

## Goals

- Build **injury probability ensemble** from Statcast pitch-level data, workload metrics, velocity trends, pitch mix
- Construct **injury severity** and **expected days lost** models (complement binary prediction)
- Develop **time-to-injury survival models** (Cox PH, accelerated failure time)
- Produce **Injury Risk+ composite score** — normalized like ERA+/OPS+, indexed to 100 = league-average risk for pitcher archetype
- Achieve **full interpretability** via SHAP, permutation importance, partial dependence
- Build **simulation infrastructure** for counterfactual workload/pitch-mix analysis ("what if this pitcher threw 10 fewer pitches per start?")

## Tech Stack

- **Data:** Statcast (PyBaseball), MLB Stats API, Baseball Savant, injury transactions
- **Pipeline:** Python, Conda, pandas, numpy
- **Modeling:** scikit-learn, XGBoost/LightGBM, statsmodels (survival), neural nets
- **Interpretability:** SHAP, permutation importance, partial dependence
- **Infrastructure:** Structured data pipeline (raw → processed → engineered), modular src/, notebook-driven analysis
- **Testing:** Unit + integration tests included

## Current Status

**Phase 1 (Foundation):** Scaffolding complete; awaiting data pipelines  
**Phase 2–7:** Feature engineering through simulation (roadmap in repo)

See [Pitcher-Injury-Risk/docs](file:///Users/nateseluga/Pitcher-Injury-Risk/docs) for architecture, data dictionary, and research roadmap.

## Open Questions

- Integration of biomechanical data (arm angle, release point drift, acceleration metrics) beyond Statcast
- Real-time injury prediction during ongoing season vs. preseason modeling
- Optimal calibration between false-positive rate and actionable lead time for front offices
- How to validate counterfactual predictions (simulation accuracy relative to actual outcomes)

## Key Files

- `environment.yml` / `requirements.txt` — reproducible env setup
- `Pitcher-Injury-Risk/src/` — modular pipeline code (data, features, models, scoring, simulation, viz)
- `Pitcher-Injury-Risk/notebooks/` — numbered sequential analysis pipeline
- `Pitcher-Injury-Risk/models/` — serialized trained models
- `Pitcher-Injury-Risk/docs/future_research_questions.md` — full research agenda

## Links

- **GitHub:** https://github.com/nseluga/Pitcher-Injury-Risk
- **Repo README (full):** Pitcher-Injury-Risk/README.md
- **Architecture:** Pitcher-Injury-Risk/docs/
- **Data sources:** PyBaseball, MLB Stats API, Baseball Savant
