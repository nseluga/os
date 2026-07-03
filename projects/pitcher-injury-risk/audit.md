# Audit: pitcher-injury-risk repo vs. portfolio writeup

Repo: `/workspace/pitcher-injury-risk` · Writeup: `/home/user/portfolio/src/content/projects/pitcher-injury-risk.mdx` (+ chart data `/home/user/portfolio/src/data/pitcher-injury-risk.json`)

---

## What the project actually does

A far more ambitious platform than the writeup describes — "Pitcher Injury Risk+", a multi-model pitcher health research pipeline over Statcast 2015–2024:

- **Data**: Pulls Statcast pitch-level data via pybaseball (NB01) and builds an injury database from **MLB Stats API IL transactions** (NB02: fetch IL placements, parse injury types, pair placements/activations to compute days lost). No Retrosheet. Feature matrix (NB05): **205,911 pitcher-game rows × 88 cols, 3,249 pitchers, seasons 2015–2024**; models consume **76 features** (82 in later survival runs) across workload (ACWR 7:28, rolling 7/28/90d pitch counts), velocity (14/30/90d windows, intragame drop), movement/release-point drift, pitch mix (incl. slider spin), and injury history.
- **Targets**: `injured_next_30d/60d/90d` (positive rates 6.6% / 10.8% / 13.4%), plus days-to-injury, days-lost, injury type.
- **Models** (4 tracks):
  1. **Baseline classifiers** (NB06): naive rate lookup, logistic regression, random forest, XGBoost; PR-AUC-first evaluation; temporal train/test split (train 2015–2022 = 159,886 rows; test 2023–2024 = 46,025 rows); isotonic calibration on a 2022 validation split (n=21,148); walk-forward temporal CV.
  2. **Survival models** (NB07): Cox PH (with Schoenfeld PH-assumption test), Weibull/log-normal AFT, Random Survival Forest, gradient-boosted survival (GBSA), and a rank-average **3-model ensemble** (GBSA+Cox+RSF).
  3. **Multi-task models** (NB08): chained and shared-representation architectures jointly predicting injury probability, days lost (log1p-transformed), and injury type.
  4. **Injury Risk+** (NB09): ERA+/OPS+-style composite (50% calibrated injury prob, 30% expected days lost, 20% hazard), normalized to mean 100 within each season × archetype; 9,752 pitcher-seasons scored.
- **Interpretability** (NB10): TreeSHAP global/beeswarm/waterfalls on 5,000 stratified rows, path-dependent vs. **interventional SHAP comparison**, partial dependence plots.
- **Baseball insights** (NB11): Risk+ vs. pitch mix / velocity / workload / rest / role, 5 two-dimensional risk heatmaps ("danger zones"), pre-injury trajectory built from 2,620 IL stints, 6-row novel-insight candidate table.
- **Counterfactual simulation** (NB12): pitch-count reduction, rest schedules, slider reduction, role transition, injury recency — with explicit survivorship-bias and "model-conditional, not causal" caveats.
- **Dashboards** (NB13 + `dashboard/`): a working **Streamlit app** (4 panels) plus interactive Plotly HTML exports.
- **Process discipline**: `docs/model_improvement_log.md` and `docs/model_critique_log.md` document literature-cited improvement rounds (S-001…S-006 etc.) with hypothesis → implementation → measured delta → kept/reverted verdicts, including honest null results and bug fixes (e.g., `intragame_velo_drop` global-max bug; proportional-scaling simulation bug that silently held ACWR constant).

## Real findings/results (exact numbers from repo outputs)

From executed HTML exports (`notebooks/html_exports/`) and improvement logs. **Discrimination is modest — nowhere near 0.78 AUC.**

**Baseline classification, 30-day horizon (NB06, full 2015–2024 run):**
- Tuned + isotonic-calibrated, held-out 2023–24 test: **RF AUC-ROC 0.579 / PR-AUC 0.131**; XGBoost 0.572 / 0.125; logistic 0.561 / 0.119 (Brier ≈ 0.092; test positive rate 9.9%).
- Walk-forward temporal CV (RF, 5 folds, 2020–2024 test seasons): **mean AUC-ROC 0.571 (std 0.023)**; fold AUCs 0.536–0.596; PR-AUC 0.132–0.179.
- Multi-horizon (RF): 30d AUC 0.586 / PR-AUC 0.137; 60d 0.577 / 0.208; 90d 0.571 / 0.257.
- Hyperparameter tuning CV PR-AUC: LR 0.1491, RF 0.1454, XGB 0.1597. Tuning+calibration *hurt* test PR-AUC (deltas −0.002 to −0.006). Improvement-log baseline: RF temporal-CV PR-AUC mean **0.148**, holdout PR-AUC **0.135**.
- Top RF importances: `prior_il_total` 0.268, `prior_il_days_lost` 0.150, `days_since_last_injury` 0.139, `prior_il_shoulder` 0.068, `prior_il_elbow` 0.055, `fb_pct_30d_avg` 0.048 — injury history dominates.

**Survival (NB07 + improvement log):**
- HTML export run: RSF C-index **0.514**, AFT-Weibull 0.501, Cox PH 0.499; tuned Cox 0.5346, tuned RSF 0.5195.
- Later documented rounds (arm-only events, ~91% censoring): GBSA subsample=0.8 C=**0.5591**; rank-average ensemble GBSA+Cox+RSF C=**0.5658** (best; TEST_MODE 2022–24, full run "pending" in log). Cox hazard ratios: `fb_pct_delta_30d` HR=1.28 (p<0.01), `sl_pct` HR=1.21, `prior_il_elbow` HR=1.20 (p<1e-9), `acwr_7_28` HR=1.06.
- Documented failures/reversions: log-normal AFT 4th member (−0.0021), ExtraSurvivalTrees (C=0.5381, hurt ensemble), IPCWLS loss (incompatible with 91% censoring).

**Multi-task (NB08, TEST_MODE export):** chained model 30d AUC 0.557 / PR-AUC 0.144; 60d 0.552; 90d 0.551.

**Injury Risk+ (NB09, full run):**
- Isotonic calibration on held-out 2024: ECE 0.0590→**0.0294**, MCE 0.1901→0.1048, Brier 0.0934→0.0891; calibration slope 0.128→0.247 (still heavily compressed — honestly reported).
- 9,752 pitcher-seasons scored; mean = 100.0 within every season × archetype cell.
- Year-over-year IR+ stability: mean r = **0.583** (0.433 in 2018→19 up to 0.723 in 2022→23).
- Empirically optimized blend weights (0.911/0.086/0.004) vs. design defaults (0.50/0.30/0.20) — defaults retained, divergence documented.

**Baseball-specific insights (NB11, full run, model-predicted Risk+):**
- Velocity-decline dose-response: mean Risk+ 96.9 (at/above season avg) → 104.3 (0–1 mph decline) → 108.0 (1–2 mph) → **119.5 (>2 mph)**; **observed 30d injury rate 6% → 12%** across the same bins (n=88,704 … 13,311).
- Slider-usage quartiles: Risk+ 91.8 (Q1) → 112.3 (Q4).
- ACWR zones: Risk+ 95.5 (<0.8) → 103.0 (1.3–1.5) → 106.2 (>1.5).
- 25.2% of pitcher-games have Risk+ >120; 0.7% >200. Pre-injury trajectory from 2,620 IL stints.
- Interventional vs. path-dependent SHAP (NB10): `acwr_7_28` rank 58→48; `pitches_90d` genuinely rank 5 — 90-day cumulative load beats the ACWR ratio in this dataset.

**Simulation (NB12, full run):** pitch-count curve inverted by survivorship bias (explicitly caveated); flat rest curve (null, acknowledged); recency simulation ~flat for injured subsample. Outputs in `simulation_results.csv` + 5 figures.

## Strongest visualizations/dashboards (paths + descriptions)

Note: `reports/figures/` and `models/` are empty in the committed repo (only `.gitkeep`) — rendered outputs live inside `notebooks/html_exports/*.html`.

1. **Streamlit dashboard app** — `dashboard/app.py` + `dashboard/components/{leaderboard,pitcher_profile,trend_comparison,archetype_panel}.py`. Four interactive panels: season IR+ leaderboard (top/bottom 25, season + archetype filters), pitcher profile with fuzzy name search and IR+ trend vs. archetype ±1 SD band, multi-pitcher comparison, archetype analysis. The single strongest portfolio asset.
2. **Interactive Plotly dashboard exports** (NB13; `notebooks/html_exports/13_dashboard.html`, writes `reports/figures/dashboard/*.html`): `leaderboard.html` (4.7 MB interactive), `pitcher_lookup.html`, `trend_explorer.html`, `component_breakdown.html` (e.g. Kenley Jansen 2024 IR+ = 78.4), `archetype_comparison.html`.
3. **Risk interaction heatmaps** (NB11; in `11_baseball_specific_insights.html`, 4 MB export): `risk_heatmap_velocity_slider.png`, `risk_heatmap_velocity_workload.png`, `risk_heatmap_slider_rest.png`, `risk_heatmap_acwr_prior_injury.png`, `risk_heatmap_age_workload.png` — annotated 10×10 danger-zone grids centered at Risk+ 100. The age × workload heatmap is the *real* analog of the MDX's fabricated age/usage chart.
4. **Velocity-decline dose-response** (`velo_decline_threshold.png`, NB11) — the cleanest validated finding (Risk+ 97→119, injury rate 6%→12%).
5. **SHAP suite** (NB10 export): `shap_global_importance.png`, `shap_beeswarm.png`, interventional comparison, high/low-risk waterfalls, 4 partial-dependence panels.
6. **Calibration reliability diagrams** (NB06 `fig_20/_20b`), IR+ distribution by archetype (NB09 `fig_24`), pre-injury trajectory + performance-risk frontier (NB11), 5 simulation figures (NB12).

## Inaccuracies & gaps in current writeup (writeup claim → repo reality)

1. **"78% AUC-ROC" (title metric, summary, takeaways)** → Real held-out AUC-ROC ≈ **0.57–0.59** (tuned RF 0.579; temporal CV mean 0.571; best horizon 0.586). No 0.78 anywhere in the repo. This is the most serious fabrication.
2. **"Training AUC 0.79 / CV 0.78 ±0.04 / holdout-2024 0.76"** → None exist. CV mean is 0.571 (std 0.023); test set is 2023–2024 jointly, not 2024 alone.
3. **"High-risk precision (top 10%): 64%"** → No such analysis exists; actual test precision ≈ 0.12 (RF), and NB10 notes the probability range is compressed to [0.31, 0.70].
4. **"Logistic 0.77 vs XGBoost 0.79, ~1% gap"** → Fabricated values; real gap (tuned, test): logistic 0.561 vs XGBoost 0.572 AUC, and RF beats both.
5. **"2,847 pitchers" training data** → Feature matrix has **3,249 pitchers / 205,911 pitcher-game rows** (train split 159,886 rows).
6. **"12 primary features / 12 risk variables"** → **76 model features** (88 columns; 82 in survival rounds).
7. **"Injury is rare (~3–4% of pitcher-seasons)"** → Unit is pitcher-game observations; 30d positive rate is **6.6% overall** (5.7% train / 9.9% test).
8. **"Stratified 5-fold CV; class weighting"** → Repo uses **temporal/walk-forward CV** and a chronological season holdout (a stronger design the writeup fails to claim); stratified k-fold would leak across time. Class weighting is real (`class_weight='balanced'`, `scale_pos_weight`).
9. **"Injury history: Retrosheet + manual research, 15+ years"** → Injury DB is built programmatically from **MLB Stats API IL transactions**, 2015–2024. Retrosheet is not used anywhere.
10. **Age & usage chart (ECharts, 3.2%→13.1% curves; "inflection at age 30")** → Data appears in no repo output; NB11's real age analysis is the age × workload heatmap. The specific percentages, the "inflection at age 30", and the accessibility summary are all invented.
11. **"Prior IL stint +35% risk; multiple +70%; velocity loss >2mph +20% risk"** → Not repo outputs. Real analogs: prior-IL features are the top 3 RF importances; >2 mph chronic velocity decline doubles observed 30d injury rate (6%→12%) and Cox `prior_il_elbow` HR=1.20, `fb_pct_delta_30d` HR=1.28.
12. **"Model selection: logistic regression first, then XGBoost"** → Repo trains naive baseline, LR, RF, XGBoost (and LightGBM in a logged round); **random forest** wins on PR-AUC and is the production model feeding IR+.
13. **"~78% discrimination between high and low-risk scenarios"** → Discrimination is honestly weak (AUC ~0.57); the repo's own docs treat this candidly. The writeup's central performance narrative misrepresents the project's actual (and more interesting) story.
14. **Framing gap — writeup describes a simple binary classifier project** and never mentions: survival/time-to-injury modeling, multi-task severity/days-lost models, the **Injury Risk+ composite score** (the project's namesake and organizing idea), isotonic calibration work (ECE 0.059→0.029), SHAP interventional-vs-path-dependent analysis, the pitches_90d-beats-ACWR finding, the counterfactual usage-strategy simulator with survivorship-bias caveats, the Streamlit dashboard, the 6-insight candidate table, or the literature-cited critique/improvement logs with documented null results — all real, verifiable strengths.
15. **"Prospective tracking planned / validation through 2025"** → No prospective infrastructure exists; roadmap items in docs differ.
16. Minor: MDX date 2024-03-15 predates the repo's logged work (2026-06); `/home/user/portfolio/src/data/pitcher-injury-risk.json` duplicates the fabricated chart data.

## Recommended framing for rewrite

Frame this as an honest, research-grade pitcher-health platform, not a high-AUC classifier: "I built Injury Risk+, an ERA+-style composite injury-risk score for 3,249 MLB pitchers (205,911 pitcher-game observations, 2015–2024), combining calibrated classification, survival, and multi-task models — and found that discrimination is genuinely hard (temporal-CV AUC ≈ 0.57, C-index ≈ 0.57), that injury history and 90-day cumulative workload dominate the signal (with ACWR notably weaker than the literature suggests), and that a >2 mph chronic velocity decline doubles observed 30-day injury rates." Lead with the validated dose-response findings, the calibration and temporal-validation rigor, the interventional-SHAP and simulation caveats (survivorship bias), and the interactive Streamlit/Plotly dashboards — the honest-negative-results engineering discipline in the improvement logs is precisely what a baseball-ops R&D group wants to see.
