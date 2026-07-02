# NBA Shot Value

**Repo:** https://github.com/nseluga/Shot-Value-Machine-Learning  
**Status:** active  
**Collaborators:** Nate Seluga + Michael O'Brien (Harvey Mudd CS)

One-line purpose: Predicting expected point value of NBA shot attempts from play-by-play context (location, defender proximity, game conditions) using machine learning.

## Overview

A machine learning research project that moves beyond simple made/missed binary prediction to estimate the *expected value* of individual shot attempts. Incorporates shot context (distance, defenders, game state) and models the relative value of different shot types and locations across the court.

## Goals

- Build **multi-model shot-value predictor** (logistic regression, tree ensembles, neural networks)
- Engineer **basketball-specific features:** shot distance, defender proximity, court spatial position, game context
- Achieve **full interpretability:** SHAP feature importance, partial dependence, interaction effects
- Produce **actionable visualizations:** shot-value heatmaps by zone, feature contribution analysis
- Demonstrate **rigorous ML methodology:** train/test splits, cross-validation, calibration, ROC-AUC
- Compare **multiple modeling approaches** to identify best tradeoff between accuracy, interpretability, and practical utility

## Tech Stack

- **Language:** Python / Jupyter Notebook
- **Data:** NBA play-by-play tracking data (source: [specify — NBA Stats API, Kaggle, etc.])
- **Modeling:** scikit-learn, XGBoost/LightGBM, TensorFlow/Keras (neural nets)
- **Interpretability:** SHAP, permutation feature importance, calibration curves
- **Evaluation:** accuracy, precision/recall, F1, ROC-AUC, calibration plots
- **Visualization:** matplotlib, seaborn (heatmaps, importance rankings, calibration)

## Current Status

Project complete with writeup. Includes:
- Full feature engineering pipeline
- Three model families trained and evaluated
- Comprehensive results documentation in `Project_Writeup.pdf`
- Shot-value heatmaps and feature importance visualizations

## Key Findings

- [Summarize key insights — e.g., which features matter most, which shot types/zones are undervalued, etc.] — see `Project_Writeup.pdf`
- Model calibration: [specify which model is best-calibrated and why]
- Range of shot value across court: [heatmap ranges]

## Open Questions

- Integration with real-time game data for live shot-value analysis
- Extension to other sports (e.g., soccer xG models, hockey, etc.)
- Player-specific shot-value models (does shot value vary by shooter skill?)
- Defensive impact quantification (how much does defender proximity/quality affect expected value?)

## Project Structure

- `notebooks/` — numbered analysis pipeline (data prep → EDA → features → models → evaluation)
- `Project_Writeup.pdf` — full methodology, results, visualizations
- Data, models, and outputs (structure may vary)

## Audiences

- **NBA teams / analytics departments** — shot-value and shot-selection analysis
- **Sabermetrics / sports analytics community** — methodology and model comparison reference
- **ML practitioners** — computer vision and tracking data case study

## Links

- **GitHub:** https://github.com/nseluga/Shot-Value-Machine-Learning
- **Writeup:** Project_Writeup.pdf
- **Co-author:** Michael O'Brien (Harvey Mudd CS)
