---
name: Batting Average Ability
status: on-hold
priority: medium
last_active: 2025-12-01
next_step: "Refine the GitHub repo using baseball-research tooling to make it more presentable for viewers"
repo: ~/Downloads/Archive/Batting Average Ability/Batting-Average-Ability
github: https://github.com/nseluga/Batting-Average-Ability
summary: "Separates MLB hitter batting-average skill from luck via ML and statistical modeling."
tags: [ml, baseball]
---

## Where it stands

On hold. Decomposes batting average into skill vs. luck via a BABIP model (CLR features, linear + random-forest comparison) on 2023–2025 hitting data. Trained models and player/season output tables are committed; headline finding is the skill/luck split (ICC ~24.7%). Last touched 2025-12-01 — next work is presentation polish for viewers, not new modeling.

## Run / verify

    # Jupyter notebooks (no scripted entrypoint):
    #   BA_dict.ipynb, batting_average_model.ipynb
    # Committed outputs: linear_regression_*.pkl, rf_avg_model.pkl, baa_*_table.csv

## Key files

- **audit.md** (in this os folder) — prior code audit of the repo.
- Notebooks + committed model artifacts (`*.pkl`, `*_table.csv`) live in the repo root.

Related: [[projects/pitcher-injury-risk/README|pitcher-injury-risk]] · [[projects/hitter-embedding/README|hitter-embedding]]
