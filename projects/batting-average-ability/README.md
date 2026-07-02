# Batting Average Ability

**Repo:** `~/Downloads/Batting Average Ability/Batting-Average-Ability`  
**GitHub:** https://github.com/nseluga/Batting-Average-Ability  
**Status:** active

One-line purpose: Separating MLB hitter batting-average skill from luck — models true-talent ability vs. noise via machine learning and statistical regression-to-mean analysis.

## Overview

A tutorial and reference project for baseball-operations analysts and scouts. Demonstrates how to build a hitter-evaluation metric that isolates batting-average control skill from random variance, using plate discipline, power, and batted-ball indicators as underlying performance drivers.

## Goals

- Develop a **skill-vs-luck separation framework** for batting average (regression to mean / true talent estimation)
- Predict **forward-looking batting average ability** (age-adjusted)
- Identify **leading indicators** of batting-average skill (approach metrics, batted-ball profile, contact quality)
- Create an **interpretable metric** suitable for scouts and front office decision-making
- Serve as a **reference example** for building performance-evaluation models in baseball analytics

## Tech Stack

- **Data:** PyBaseball (Statcast, FanGraphs, Baseball Reference)
- **Language:** Python / Jupyter Notebook
- **Methods:** Machine learning (regression, random forest, gradient boosting), statistical modeling
- **Evaluation:** Cross-validation, prediction accuracy on held-out seasons, residual analysis

## Current Status

Active; tutorial-ready for reference and knowledge-sharing.

## Open Questions

- Optimal feature set and model complexity for forward prediction (simplicity vs. explanatory power tradeoff)
- How much of batting-average variance is truly attributable to skill vs. luck (expected upper bound on R²)
- Age-curve shape for batting-average ability (how does skill change over a career?)
- Integration with broader hitter evaluation (combining BA control with power, plate discipline, speed into a composite score)

## Key Files

- `Batting-Average-Ability/README.md` — project overview
- Jupyter notebooks — analysis pipeline (feature engineering, modeling, evaluation)
- `pybaseball` — data loading and cleaning

## Audiences

- **Baseball operations / front office** — hitter evaluation, player comps
- **Sabermetrics community** — model design, methodology reference
- **Sports analytics practitioners** — tutorial on building interpretable player metrics

## Links

- **GitHub:** https://github.com/nseluga/Batting-Average-Ability
- **Data source:** PyBaseball (Statcast, FanGraphs, Baseball Reference)
