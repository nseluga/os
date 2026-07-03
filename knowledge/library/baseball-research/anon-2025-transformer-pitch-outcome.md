# Transformer-Based Baseball Modeling for Pitch Outcome Prediction and Strategy Optimization

**File:** `anon-2025-transformer-pitch-outcome.pdf`
**Authors:** anonymized submission (ID 20251439, ~2025). Explicitly builds on
Heaton & Mitra's contextual event embeddings and positions itself against
[[melville-2023-game-theory-pitch-sequencing]]'s game-theoretic approach.

## Questions answered
- Can a sequence model predict the outcome (10 classes) *and* hit location
  (9 fielder positions) of a single pitch, in real time, for any batter —
  including players not in the training data?
- Can that predictive model be inverted into a pitch recommender ("what should
  I throw to get a strikeout / ground-ball double play here?") without
  computing game-theoretic equilibria?

## Models used
- **12-layer transformer encoder**, ~800K parameters. Input: sequences of 400
  consecutive pitches faced by the batter, each pitch an 87-dim vector
  (standardized continuous features + one-hot categoricals + mask dims).
  Sinusoidal positional encodings; the final pitch's raw features also bypass
  the encoder via a residual/concat path so last-pitch detail survives.
- **Sub-token masking**: on the final pitch, outcome features (result, hit
  location, launch speed, hit coordinates) are masked; observable pre-outcome
  features (velocity, spin rate, release point) stay visible. BERT-style
  masking adapted so the mask boundary matches what is physically knowable
  before the ball arrives.
- **Multi-task loss**: 0.7 · (CE pitch outcome + CE hit location) + 0.3 · MSE
  on continuous targets. Continuous predictions turned out inaccurate and were
  dropped from the outputs, kept only as auxiliary training signal.
- **Baselines**: 2022 historical outcome distribution; XGBoost on the same
  features without sequence context. Data: Statcast 2015–22 train/val,
  2023–24 test.
- **Pitch recommender**: enumerate the pitcher's (pitch type × 13 zones) grid
  using his average velo/spin per type, append each candidate as the 400th
  pitch, score S = ω₁·P(desired outcomes) + ω₂·P(desired hit locations) −
  ω₃·P(undesired), rank.

## Methodology — defending & translating baseball assumptions
- Central design bet: **no player identifiers at all**. Batter identity is
  implicit in the 400-pitch context window. Defended on baseball grounds:
  static embeddings can't handle rookies, trades, or in-season skill change,
  while a context window works for any player with recent pitches and enables
  real-time deployment. (Window size 400 chosen by validation over
  {200, 400, 600}.)
- Top-4 precision as headline metric, argued from class imbalance: balls and
  strikes dominate, so raw accuracy hides whether the model ranks rare but
  strategically decisive events (HR, 2B) highly.
- Realism constraints in the recommender: candidate pitches use the pitcher's
  own repertoire and historical average velo/spin, so it never recommends a
  pitch he doesn't throw.
- Rare events (pickoffs, IBB) dropped; near-synonymous outcomes (GIDP,
  fielder's choice) merged into Field Out — acknowledged as a granularity
  trade-off and listed as future work to undo.
- Honest limitation: the model is "playerless" on the pitcher side; pitcher
  embeddings built from his own pitch history are proposed future work.

## Baseball insights
- The transformer's edge over XGBoost concentrates exactly where strategy
  lives — rare outcomes: top-4 precision 97% vs 86% (singles), 43% vs 30%
  (doubles), 34% vs 23% (HR). On balls/strikes both are ~99%.
- It infers hitter archetypes from context alone: predicted 25.6 HR for Judge
  (XGBoost: 13.9, actual: 32) and 100.4 singles / 38.0 K for Arraez (XGBoost:
  64.5 / 88.2, actual: 116 / 25). Sequence context substitutes for knowing who
  the hitter is.
- Hit-location predictions match spray profiles (Judge deep outfield, Arraez
  up-the-middle infield) — usable for defensive positioning, not just pitch
  calling.
- Case-study sanity checks: 0-2 to Ohtani → low fastballs zones 7–9, matching
  his actual low-zone strikeout heat map and Cole's best pitch; swap in
  Gregory Santos and the recommendation flips to his slider — the model
  respects pitcher arsenal without being told to.

## Why it's on the shelf
Directly reusable patterns for pitch-level modeling work (pitcher-injury-risk
project): sequence construction from Statcast, sub-token masking, playerless
context windows, and calibration/top-k evaluation under class imbalance.
