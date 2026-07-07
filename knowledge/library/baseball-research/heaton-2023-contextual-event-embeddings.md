# Learning Contextual Event Embeddings to Predict Player Performance in the MLB

**File:** `heaton-2023-contextual-event-embeddings.pdf`
**Authors:** Connor Heaton & Prasenjit Mitra (Penn State), MIT Sloan Sports
Analytics Conference 2023. Sequel to [[heaton-2022-player-form-embeddings]]
(same dataset methodology, extended to 2021) and the direct predecessor that
[[anon-2025-transformer-pitch-outcome]] builds on. Code:
github.com/c-heat16/contextual_performance_prediction.

## Questions answered
- Can a pre-train/fine-tune pipeline — learn baseball as a sequence of events
  first, then attach a small prediction head — forecast single-game player
  performance (pitcher strikeouts, batter has-hit) well enough to compete
  with major US sportsbooks?
- How far does only 10 games of play-by-play context and 6 years of training
  data go, versus the decades of career stats the books use?

## Models used
- **Transformer encoder over sequences of pitches spanning 10 games.** Each
  event = gamestate delta + pitch type + result type (learnable embeddings) +
  continuous Statcast features + a thin sabermetric description of pitcher,
  batter, and matchup (last 15 days / season / career — deliberately <5% of
  the input vector).
- **Pre-training: Masked Gamestate Modeling** (BERT MLM adapted) — mask 15%
  of event vectors, predict the missing gamestate and event. **Player
  embeddings are prepended to the sequence** with a doctored attention mask so
  each player token can only attend to events that player was involved in —
  the model fills them with player-describing signal to help unmask events.
- **Fine-tuning**: identify the starting pitcher and nine starting batters for
  a game, embed their previous N=10 games, predict per-player strikeouts,
  hits, and walks with a new linear layer.
- **Asymmetric context construction**: pitchers get their own last 10 starts;
  batters get their *team's* batting sequences vs the last 10 opposing
  starters, with the batter's embedding derived from his involvement in them.
- **Data**: season stats 1995–2021, play-by-play 2015–2021 — 15,743 games,
  1.2M PA, 4.6M pitches, 2,229 batters, 1,884 pitchers. Evaluation vs three
  major sportsbooks' published 2021 lines.

## Methodology — defending & translating baseball assumptions
- The framing argument: sports analytics is stuck in a **"bag-of-events" era**
  — BABIP, ERA, OPS, even WAR all reduce to counting how often events occur,
  never how (the paper walks WAR's linear-weights construction to show it).
  Contextual embeddings are the analog of NLP's move from bag-of-words to
  BERT: the same "single" should mean different things in different contexts.
- Benchmarking against sportsbooks is the external-validity play — books are
  the strongest public predictions available — but the comparison is caveated
  honestly: books predict has-hit *per game*, the model predicts it *vs the
  starting pitcher only* (fewer PA, strictly harder), and books only post
  lines they're confident in while the model predicts every starter.
- Pitcher >> batter performance (K prediction R² 0.21 vs 0.06) is explained
  mechanistically rather than hidden: a starter participates in ~9× more
  events per game than any single batter, and batters often have fewer than
  10 games of effective context (shown in a context-count figure). Proposed
  fixes: longer team windows, minor-league sequences for rookies.
- The embedding-visualization section is framed as a check against "is it just
  exploiting a statistical shortcut?" — ~300K event embeddings are extracted
  and inspected for baseball-meaningful structure before the predictive claims
  are taken at face value.

## Baseball insights
- **Competitive with the books on quality, ahead on coverage**: pitcher
  single-game strikeouts MAE 1.85 / R² 0.21 vs best book 1.80 / 0.23; longest
  correct has-hit streak 16 vs the books' best 17 — while making 4,856
  predictions, ~50% more than the widest book (3,239), because it prices
  *every* starter, not just the confident ones.
- Fine-tuned raw errors: pitcher K MSE 5.37 / MAE 1.85; batter-level targets
  are much noisier (R² 0.02–0.06) — a calibration point for anyone promising
  single-game batter predictions.
- Event embeddings of ~12K singles striate by outs recorded, base occupancy,
  and runs scored — the model finds "more than one way to describe a single."
  Strikeout embeddings cluster high-leverage (runners-on) situations together
  **without leverage ever being an input** — it rediscovers the concept from
  context.
- 10 games of play-by-play ≈ decades of career counting stats, for pitchers:
  a strong data-efficiency argument for sequence models over stat aggregation.

## Why it's on the shelf
The bridge paper: it turns the form representations of
[[heaton-2022-player-form-embeddings]] into an actual performance-prediction
pipeline, and its pre-train/fine-tune + masked-event recipe is what
[[anon-2025-transformer-pitch-outcome]] refines to the single-pitch level.
Practical templates for the upcoming project: constructing player context
windows from Statcast, prepending player tokens with restricted attention,
benchmarking against betting markets (with honest task-mismatch caveats), and
sanity-checking learned representations before trusting predictions.
