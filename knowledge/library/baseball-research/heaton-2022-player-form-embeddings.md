# Using Machine Learning to Describe How Players Impact the Game in the MLB

**File:** `heaton-2022-player-form-embeddings.pdf`
**Authors:** Connor Heaton & Prasenjit Mitra (Penn State), MIT Sloan Sports
Analytics Conference 2022 (research paper finalist). First paper in the Heaton
& Mitra line; [[heaton-2023-contextual-event-embeddings]] is the direct sequel.
Explicitly critiques the static-embedding assumption of
[[alcorn-2018-batter-pitcher2vec]]. Code: github.com/c-heat16/learning_player_form.

## Questions answered
- Can a model learn *player form* — how a player has impacted the game over
  his last few games — as a vector, instead of describing him with career-long
  counting stats or a single static embedding?
- Do form embeddings describe players better than sabermetric profiles over
  both short (15 PA) and long (multi-season) horizons, and do they carry
  predictive signal for game winners?

## Models used
- **BERT-style bidirectional transformer encoder**: 8 layers, 8 heads, model
  dim 512. Separate batter and pitcher models, no shared weights. A [CLS]
  token's output, projected to **64 dims**, is the form embedding.
- **Event vocabulary = 325 "gamestate deltas"** — changes in (count, base
  occupancy, outs, score) — rather than event labels like "single," plus
  learnable embeddings for stadium, position, pitch type, and continuous
  Statcast features. Player context: 1,541 supplemental sabermetric features
  (career / season / last-15 / this-game scopes) projected down so roughly
  half of each input describes the event and half the participants.
- **Two training objectives**: (1) Masked Gamestate Modeling — BERT MLM
  adapted, mask 15% of gamestate-delta tokens and impute; (2) **self-supervised
  contrastive loss** on two overlapping views of a player's activity window.
  Batters: window = 20 consecutive PA, views = 15 PA with random offset 1–5;
  pitchers: window = 75 PA, views = 60 PA, offset 1–15 (~3–4 games per view).
- **Data**: pybaseball → sqlite; pitch-by-pitch 2015–2019 (12,147 games,
  925K PA, 3.6M pitches), season stats 1995–2019.
- **Downstream probes**: agglomerative clustering (Ward) of form embeddings
  into discrete form IDs vs the same clustering on sabermetric profiles;
  game-winner prediction with random forest / logistic regression / SVM using
  team metadata, lineup stats, and form embeddings (first 5 PCs per player).

## Methodology — defending & translating baseball assumptions
- The contrastive-learning bet, stated in baseball terms: **no ground-truth
  labels for "form" exist**, but two nearly-overlapping stretches of the same
  player's PAs must describe the same form — so pull their embeddings
  together and push apart other players and other windows of the same player.
  The label problem is dissolved by a temporal-consistency assumption.
- Gamestate deltas instead of event names defend the "a single is not just a
  single" argument structurally: a dribbler that advances a runner and a
  station-to-station line drive produce different deltas, so the model never
  conflates them.
- Direct challenge to prior embedding work (Alcorn; Liu et al.'s hockey agent
  representations): "we question the assumption that the same player can or
  should be described the same way in all situations" — form is
  time-varying by construction.
- Critique of action-valuation methods (VAEP, Goal Impact Metric): valuing
  actions only against scoring probability is one-dimensional; form vectors
  aim to describe *how* a player impacts play, not just how much toward runs.
- View sizes justified from usage rates (batters ~4.2 PA/game, starters ~23.3
  BF/start) so both player types are described over comparable game spans.
- Honest result reporting: form features only helped the random forest, not
  LR/SVM — reported anyway, with the interpretation that form features are
  higher-level interactions simpler models can't exploit.

## Baseball insights
- **Form clusters are temporally coherent where stat clusters thrash**: Gerrit
  Cole's stat-based cluster stays fixed from 2016 onward — blind to his
  poor 2016–17 vs All-Star 2018–19 — while his form cluster moves with the
  change. Batters (Harper, Stanton, Walker) bounce between stat clusters
  game-to-game; form clusters smooth this while still allowing streaks.
- Aggregated 2015–2019 form embeddings separate **WAR from HR rate**: in
  stat-based space, high-WAR territory sits inside high-HR territory (as if
  power were the only path to value); in form space they only partially
  overlap — power is one way to be good, not the definition. Pitcher form
  space organizes by breaking-ball usage with handedness secondary, whereas
  stat space organizes by handedness only.
- Game-winner prediction: random forest with stats + form + metadata hits
  **59.39% accuracy / 0.66 F1** vs 58.23% without form — modest, but 9 of the
  20 most important features are form features, and no form feature ranks
  below 83rd of 216.
- Appendix machinery worth reusing: time-in-form distributions and form
  transition matrices ("if X is in form y now, where is he n games later?") —
  a vocabulary for streakiness and regression that counting stats lack.
- Mike Trout is the stability outlier in both spaces: one form ID for nearly
  the whole 2015–2019 window, shared with only 2.7% of batters.

## Why it's on the shelf
The "player form" concept paper: a concrete recipe (windows → overlapping
views → contrastive loss → [CLS] embedding) for representing *player state
over a recent horizon* rather than identity or career averages. That framing —
detecting when the same player starts impacting the game differently — is
directly relevant to injury-risk modeling and any project about in-season
change. Also the cleanest worked example of validating embeddings by
descriptive coherence (cluster stories) plus a predictive probe.
