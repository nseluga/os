# (batter|pitcher)2vec: Statistic-Free Talent Modeling With Neural Player Embeddings

**File:** `alcorn-2018-batter-pitcher2vec.pdf`
**Authors:** Michael A. Alcorn, MIT Sloan Sports Analytics Conference 2018
(research papers competition; author anonymized in this copy). The foundational
static-player-embedding paper that the Heaton & Mitra line
([[heaton-2022-player-form-embeddings]], [[heaton-2023-contextual-event-embeddings]])
and [[anon-2025-transformer-pitch-outcome]] all position themselves against.

## Questions answered
- Can a word2vec-style neural network learn player representations directly
  from raw at-bat outcomes — no counting stats, no sabermetrics — that capture
  "talent" better than the stats themselves?
- Do those embeddings generalize: can they predict outcome distributions for
  batter/pitcher matchups never seen in training?

## Models used
- **Architecture mirrors word2vec CBOW**: one-hot batter and one-hot pitcher →
  separate embedding matrices → sigmoid activation → concatenate the two
  9-dimensional embeddings → softmax over 49 at-bat outcome classes. Trained
  with cross-entropy; Keras on a laptop CPU, 100 epochs, Nesterov SGD.
- **Outcome vocabulary encodes location implicitly**: 52 possible symbols where
  outs/singles/doubles/triples are tagged by the fielder who first handled the
  ball (S7 = single to left, etc.), plus K, W, IW, HR, HBP, balk, errors E1–E9.
- **Data**: Retrosheet play-by-play 2013–2015 for training (557,436 at-bats),
  filtered to the most frequent players covering 90% of at-bats → 461,231
  at-bats, 524 batters, 565 pitchers. Test: 2016 at-bats from **previously
  unseen matchups only** (21,479 matchups, 51,580 at-bats).
- **Baselines**: (1) naïve marginal blend — average the batter's and pitcher's
  smoothed historical outcome distributions; (2) multinomial logistic
  regression on the same one-hot inputs.

## Methodology — defending & translating baseball assumptions
- Core framing: players are like words — distinct set elements whose one-hot
  encodings pretend everyone is equidistant from everyone else. Embeddings let
  geometric distance encode similarity of talent, the way scouts think
  ("grounds out to third against lefty curveballers"), not the way stat lines do.
- Explicit critique of sabermetrics as *ad hoc*: WAR's formula reflects its
  designer's intuition; PECOTA's comparable-player neighborhoods are
  proprietary; DRA is strictly linear. Learning from raw events avoids baking
  in those choices.
- Evaluation on **unseen matchups only** is the load-bearing design decision:
  generalization to new batter/pitcher pairs is what shows the model extracted
  transferable talent signal instead of memorizing matchup history.
- The naïve baseline is carefully built (add-one smoothing with a league-wide
  prior) so the ~1% cross-entropy win is against a genuinely sensible
  strategy, not a strawman. Multinomial logistic regression actually loses to
  the naïve baseline — expressiveness of the nonlinear embedding model is
  doing real work.
- Honest scope limits: 9-dim embeddings, at-bat granularity only (no pitch
  data), players fixed over the 4-season window — no notion of form change,
  aging, or rookies. This static-representation assumption is exactly what
  [[heaton-2022-player-form-embeddings]] later attacks.

## Baseball insights
- PCA of batter embeddings separates handedness cleanly and orders players by
  single rate and HR rate — the embeddings recover standard-stat information
  without ever seeing a stat.
- Nearest neighbors pass the smell test where stat-clustering fails: Trout ↔
  Goldschmidt (speed+power), Gordon ↔ Ichiro (contact/on-base), Chapman ↔
  Kimbrel (overpowering closers), Hernández ↔ Machi/Carrasco (huge-movement
  signature pitches). Clustering on common MLB stats does *not* put
  Goldschmidt near Trout.
- Embedding algebra works like word2vec analogies: Trout − (average LHB
  vector) ≈ Chris Davis / Ortiz / **Bryce Harper** — the "opposite-handed
  doppelgänger" trick.
- Test-set result: average cross entropy 2.7848 vs 2.8113 naïve and 2.8118
  logistic regression (p < 0.001, ~0.94% improvement) on unseen matchups.
- Future-work ideas still worth stealing: map minor-league embeddings to MLB
  embeddings for prospect scouting; swap embeddings and back-simulate seasons
  to evaluate trades counterfactually; add the supporting defense as input.

## Why it's on the shelf
The origin point of player-embedding work in baseball — every later paper in
this folder cites it. Useful as the "static embedding" pole when reasoning
about representation choices: identity-based embeddings generalize across
matchups but can't handle rookies, trades, or in-season form change. Also a
model of cheap-but-rigorous evaluation design (unseen-matchup split, smoothed
naïve baseline, significance test) for small models.
