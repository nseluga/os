# Audit: batting-average-ability repo vs. "Batting Average Control Stat" writeup

Repo: /workspace/batting-average-ability
Writeup: /home/user/portfolio/src/content/projects/batting-average-control.mdx
Auditor role: baseball-ops R&D review (methodological rigor, honest evaluation, baseball reasoning)

---

## What the project actually does

- **Data**: FanGraphs season-level batting stats pulled via `pybaseball.batting_stats`, **2015–2024**, min 100 PA → 4,375 rows, cleaned to **4,374 player-seasons, 1,173 unique players**, 25 kept stat columns (expanded to 55 after one-hot team dummies). Saved as `cleaned_batting_data.csv`. A separate Baseball Savant file `2023-2025_hitting_stats.csv` (214 players) is used **only** in the trivial warm-up notebook `BA_dict.ipynb` (builds a name→BA dictionary; ~1 cell).
- **Split**: plain random 80/20 `train_test_split(random_state=42)` — 3,499 train / 875 test rows, seasons mixed. **No temporal/season-based split, no cross-validation, and no next-season target anywhere.** Everything is same-season (descriptive) modeling: predict a player-season's AVG/BABIP from that same season's peripheral stats.
- **Models** (main notebook `batting_average_model.ipynb`):
  1. **OLS Linear Regression → AVG** using all 54 features *including same-season BABIP* (cell 25–29). Near-tautological (AVG is an accounting identity of BABIP, K%, HR/FB), hence Test R² 0.9828.
  2. **OLS Linear Regression → BABIP** (cells 36–46): Test R² 0.4018.
  3. **Random Forest → AVG** excluding BABIP (cell 47, 500 trees, depth 4): Test RMSE 0.0312, with permutation-style feature-importance bar chart. Notebook comment explicitly excludes BABIP "since it has a dominant effect."
  4. **Mixed-effects (statsmodels MixedLM, random intercepts by player) → BABIP** with **centered log-ratio (CLR) transform** of the batted-ball composition (LD/GB/FB), infield-fly rate re-expressed on the BIP scale, PA-based weighting via row replication (cells 49–99). Cell output: Test R² 0.3474, Test MAE 0.0266; `babip_final_model_info.txt` / `babip_model_comparison.csv` record a run at Test R² 0.3722, MAE 0.0256 (inconsistent between saved artifacts and current notebook run). ICC = 0.184.
  5. **Mixed-effects → AVG** using predicted BABIP + plate-discipline features (cells 100–132): **Test R² 0.4570, Test MAE 0.0215, Test RMSE 0.0271**, PA-weighted MAE 0.0198; ICC = 0.247; train–test R² gap +0.0015 (no overfitting).
- **BAA metric ("Batting Average Ability")** (cells 134–156): hand-transcribed standardized coefficients from the mixed models are combined into a `plate_score` (K%, BB%, chase/zone swing & contact, SwStr) + `contact_score` (LD, sprint speed, Hard%, IFFB, GB, pull/oppo), summed to `baa_raw`, then **indexed to mean 100 / SD 10 within each season** (min 200 PA). Outputs: `baa_coefficients_output.csv`, `baa_season_table.csv` (per player-season, includes `luck_component` = actual − predicted BA), `baa_player_table.csv` (1,173 career-level rows: RAWBA vs shrunk BAA, total_pa, seasons).
- **Validation** (cells 157–163): within-season fit of BA ~ BAA for 2019–2024: R² 0.4088 (2023) to 0.5273 (2021); 2024 R² = 0.4245, MAE 0.0179, RMSE 0.0232. Plus an interactive Plotly scatter of BAA vs actual BA colored by season.
- **README.md** is 4 lines ("Modeling a baseball player's batting average ability using machine learning… pip install pybaseball").

## Real findings/results (exact numbers from repo outputs)

- Linear AVG model (with BABIP as a feature): Test MAE 0.0035, RMSE 0.0048, **R² 0.9828** (leak/identity — not a skill result).
- Linear BABIP model: Test MAE 0.0253, RMSE 0.0324, **R² 0.4018**. Top coefficients: ld +0.314, fb −0.240, contact +0.139.
- Random Forest AVG (no BABIP): **Test RMSE 0.0312**.
- Mixed-effects BABIP: Test R² **0.3474** (notebook) / **0.3722** (`babip_final_model_info.txt`, `babip_model_comparison.csv` baseline row), Test MAE 0.0266/0.0256, ICC 0.184, prediction-interval coverage 54.5%. Significant standardized effects: LD-vs-FB ↑0.0174***, **sprint speed ↑0.0087***\* (2nd largest — speed→infield hits), Hard% ↑0.0082***, IFFB ↓0.0079***.
- `babip_model_comparison.csv`: Linear baseline Test R² 0.372 **beats** Linear+Interactions (0.361, −3.0%), **Random Forest (0.293, −21.2%)**, and Ensemble (0.328, −11.7%); RF overfit gap 0.166 vs linear 0.027.
- Mixed-effects AVG (pred-BABIP + discipline): **Test R² 0.4570, MAE 0.0215, RMSE 0.0271**, PA-weighted MAE 0.0198, ICC 0.247, R² gap +0.0015. Top effects: K% ↓0.0247***, predicted BABIP ↑0.0168***, BB% ↑0.0029***.
- BAA within-season validation R² by year: 2019 0.4450, 2020 0.4298, 2021 0.5273, 2022 0.4703, 2023 0.4088, **2024 0.4245** (MAE 0.0179, RMSE 0.0232).
- Face-validity leaderboard (cell 154): Top BAA — Luis Arraez 2023 (133.2), Freddie Freeman 2020/2018/2022 (131.4/130.3/130.0); Bottom — Joey Gallo 2023 (61.2), Mike Zunino 2015 (65.9).
- Corpus: 4,374 player-seasons, 1,173 players, 2015–2024 (2020 short season = 310 rows).

## Strongest visualizations/dashboards (paths + descriptions)

All in `/workspace/batting-average-ability/batting_average_model.ipynb` cell outputs (no standalone image files or dashboards in repo):
1. **Cell 161 — Plotly interactive scatter, BAA vs actual BA, 2019–2024**, colored by season, per-season OLS trendlines, hover showing player name/PA/BAA/BA. The flagship visual; directly demonstrates the metric's validity.
2. **Cell 47 — Random-forest feature-importance horizontal bar chart** (BABIP-free AVG model): shows contact/zcontact/hard dominating once BABIP is removed.
3. **Cell 31 — Actual vs Predicted AVG scatter (test) with y=x line** (linear model; visually striking but reflects the BABIP leak).
4. **Cell 44 — Actual vs Predicted BABIP scatter (test)** — honest picture of the ~0.40 R² BABIP problem.
5. **Cell 4 — EDA figure (2-axis, 600x805) + printed correlation rankings** with AVG (babip 0.764, ld 0.363, contact 0.348) and BABIP.
6. Cell 159 — season-level summary table (mean BAA vs mean BA per season), HTML output.

## Inaccuracies & gaps in current writeup (writeup claim → repo reality)

1. **"Predictive R²: 0.52" (frontmatter + Results)** → No predictive (next-season) model exists. Closest real numbers: same-season mixed-model Test R² **0.4570**; BAA-vs-BA within-season R² 0.4088–0.5273 (0.52 appears cherry-picked from 2021's 0.5273 and relabeled "holdout 2024"; actual 2024 R² is **0.4245**).
2. **"Correlation with Future BA: 0.58"** → Fabricated. No future-BA/lagged analysis exists anywhere in the repo.
3. **"Target: Next-season batting average"** → False. All models predict the **same season's** AVG/BABIP from that season's peripherals. This is a skill-isolation/descriptive project, not a forecasting one.
4. **"Model: Elastic Net (L1 + L2 regularization)"** → No elastic net. Actual models: unregularized `LinearRegression`, `RandomForestRegressor`, and statsmodels **MixedLM** (random intercepts by player).
5. **"Validation: 5-fold cross-validation on 2015–2023; test on 2024" and "Why cross-validation by season, not random split?"** → Repo uses exactly the **random 80/20 split** the writeup disparages (cell 20, `train_test_split(random_state=42)`), mixing all seasons. No CV of any kind.
6. **"Shrinkage adjustment: weighted average of current BA and component expectation, weighted by PA confidence"** → No such step. The real (different, and defensible) mechanisms are mixed-model partial pooling via player random intercepts and PA-weighted fitting.
7. **Feature list: "hard-hit (EV ≥90 mph), sweet-spot rate (LA 8–32°), barrels per PA, spray angle variance," "from public Statcast data"** → None of these Statcast features are used in the models. Actual features are FanGraphs rates: K%, BB%, SwStr%, O/Z-swing, O/Z-contact, LD/GB/FB/IFFB%, HR/FB, Pull/Oppo%, Hard%, sprint speed. (Also, Statcast hard-hit is ≥95 mph, not ≥90 — a domain error.)
8. **RMSE bar chart: Component 0.032 vs Naive-current-BA 0.041 vs Average 0.035; "predicts within 32 points"** → Fabricated comparison; no naive-baseline evaluation exists. Real test RMSEs: mixed AVG model **0.0271**, RF 0.0312, BAA per-season 0.0225–0.0279. (Ironically the real model is *better* than the invented 0.032.)
9. **"Correlation with 2024 actual BA: 0.58 vs 0.48"** → Fabricated; no such correlations computed.
10. **Archetype table (120/95/140/320 players, year-to-year BA SDs 0.018–0.035, "Model Advantage")** → Entirely absent from the repo; no year-to-year volatility analysis exists.
11. **Example predictions (Betts .305 pred/.295 actual; Judge .280/.289; "beats naive 58% of the time across 200+ qualified hitters")** → Fabricated; no player-level next-year predictions exist. Real, citable examples the writeup ignores: Arraez 2023 BAA 133.2 (BA .354) and Gallo 2023 BAA 61.2 (BA .177).
12. **"Why not a black-box model?"** → The repo *did* train a random forest — and the honest, stronger story is in `babip_model_comparison.csv`: RF Test R² 0.293 vs linear 0.372 (−21.2%, overfit gap 0.166), which empirically justifies the interpretable choice.
13. **"1,200+ hitters"** → 1,173 unique players (4,374 player-seasons). Minor inflation; "~1,170 hitters / 4,374 player-seasons" is both accurate and more impressive.
14. **"wider prediction intervals on rookies… correctly reflects that"** → No rookie-specific intervals. The only interval statistic is BABIP PI coverage of **54.5%** (`babip_final_model_info.txt`) — i.e., intervals are poorly calibrated, the opposite of the claim.
15. **Name: "BA Control Stat" / "control score"** → Repo calls it **BAA (Batting Average Ability)**, indexed to mean 100 / SD 10 per season. No "control" terminology anywhere.
16. **"Chart data referenced in /src/data/"** → No BA data file exists there (only `pitcher-injury-risk.json`, `site.ts`); the MDX chart values are hardcoded and fabricated.
17. **Training-data metric "MLB 2015–2024"** → This one is actually **correct** despite the repo filename `2023-2025_hitting_stats.csv` (that file is only the side notebook); main dataset is FanGraphs 2015–2024.

### Real strengths the writeup fails to mention
- **Mixed-effects modeling** with player random intercepts (partial pooling) and **ICC quantifying skill share of variance**: 24.7% for AVG, 18.4% for BABIP — a genuinely publishable framing of "how much of BA is the player."
- **CLR (centered log-ratio) transform** for compositional batted-ball data (LD/GB/FB sum to 1) — real statistical sophistication rarely seen in portfolio projects.
- **PA-weighted fitting** (row replication) so small samples don't distort coefficients.
- **Disciplined model selection**: interactions, RF, and ensemble all tried and rejected with recorded evidence (`babip_model_comparison.csv`).
- **Near-zero overfitting**: AVG mixed model train/test R² gap +0.0015.
- **Season-normalized index (100 ± 10)** = era adjustment, plus a per-player-season **luck_component** (actual − predicted BA) in `baa_season_table.csv` — the actual "separating skill from luck" deliverable.
- **Sprint speed as the #2 BABIP driver** (std coef +0.0087***) — a concrete baseball insight (fast hitters beat out grounders).
- Statistical significance reporting (p-value stars) on standardized coefficients.

## Recommended framing for rewrite

Frame the project as what it truly is: a **skill-isolation metric, not a forecasting model** — "BAA (Batting Average Ability), a season-indexed (100 ± 10) measure built from a player-random-intercept mixed-effects model with CLR-transformed batted-ball composition and PA weighting, that explains ~46% of same-season BA variance (Test R² 0.457, MAE 0.0215) from peripherals alone and decomposes each player-season into plate score + contact score + a residual luck component." Lead with the honest methodological wins (mixed effects/ICC, CLR, RF rejected on evidence at Test R² 0.293 vs 0.372) and real face-validity results (Arraez 133.2 vs Gallo 61.2), and delete every next-season/elastic-net/archetype/Betts-Judge claim; if forecasting is desired, list it as explicit future work (a year-over-year BAA stability test would be the natural next step).
