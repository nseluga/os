# An Extensive Investigation of Strategies in Baseball

**File:** `anon-2025-ai-manager-strategies.pdf`
**Authors:** anonymized submission (ID 20251404, ~2025). Title and framing
deliberately extend George Lindsey's 1963 "An Investigation of Strategies in
Baseball."

## Questions answered
- Can we build "AI managers" that make optimal matchup-level in-game decisions
  (pinch hit, reliever choice, intentional walk), and how do we validate that
  they're actually good?
- Do MLB managers who follow the AI's recommendations win more?
- Were two infamous World Series decisions — Kevin Cash pulling Blake Snell
  (2020 G6) and Aaron Boone's 10th-inning calls (2024 G1) — actually mistakes?

## Models used
- **Game model**: baseball as a stochastic, zero-sum, perfect-information,
  extensive-form game between two managers. States track inning, score,
  baserunner-out state, lineups, bench, bullpen, batters faced; nodes are
  choice / chance / terminal. Actions are matchup-level only (no pitch-level
  or bunt/steal decisions). Utility = home win ∈ {0,1}.
- **Matchup model**: Marcel projections of per-PA outcome rates by handedness
  → log odds → multinomial logistic regression giving
  P(outcome | batter, pitcher) over 8 outcomes; combined with outcome-specific
  25×24 baserunner-out transition matrices (deterministic for HR/3B/BB/HBP/K,
  empirical from Retrosheet 2019–23 for outs/1B/2B). Calibration-checked.
- **Five AI managers**:
  1. *Lindsey strategy* (baseline): xgboost re-estimate of Lindsey's HiW(l)
     win-probability contour + empirical P(runs rest of inning | base-out
     state); expectiminimax on a subtree one PA deep.
  2. *Deep Lindsey*: same, n = 3 PAs deep (mirrors the three-batter minimum).
  3. *MCTS*: vanilla UCT with random rollouts, C = 1/√2.
  4. *Half game*: splits the game into two independent half-games (each team's
     offense vs. the other's pitchers), objective = runs; solves for a
     subgame-perfect equilibrium by expectiminimax before the game, plays from
     a lookup table.
  5. *Pseudo-full game*: half game + a chance node between innings for the
     runs the other team scores, restoring wins (not runs) as the utility.

## Methodology — defending & translating baseball assumptions
- The infinite state space (any number of runs, endless extras) is truncated
  with two defended assumptions: a team leading by a huge margin has won, and
  all extra innings are equivalent to the 10th. Even truncated, the space is
  estimated larger than Heads-Up Limit Hold'em — hence approximation, since
  lineups are only known hours before first pitch and answers are needed in
  minutes.
- **Validation-by-history is the paper's best trick**: in 2,296 actual 2023
  MLB games (Gameday event data + MLB Stats API rosters), the manager whose
  decisions deviated less (in cumulative win-probability cost) from the
  Lindsey strategy won 52.7% of the time (p = 0.0045). That establishes the
  baseline as real, so any AI that beats Lindsey in simulation inherits
  credibility.
- The half-game decomposition is justified *by the matchup model's own
  limitation*: since it ignores fielding skill, offense and defense genuinely
  don't interact in the model, so the game factorizes exactly.
- The pseudo-full game exists because runs ≠ wins: Lindsey's classic example
  (bottom 9th, down 1, runners on 2nd/3rd, one out) where an IBB *raises*
  expected runs allowed by 0.082 but *lowers* win probability by 0.041. The
  inter-inning chance node restores the win objective without blowing up the
  state space.
- Roster constraints (26-man roster, 6 of 9 starters locked in, four bench
  bats, 8 relievers) mirror real MLB rules and the practice of never pinch
  hitting for stars, and are what make equilibrium solving tractable in hours
  on one CPU core.
- Known gaps stated plainly: no pitcher fatigue (a 100-pitch starter looks
  identical to a fresh one) and no fielder skill — the latter is why
  defensive-substitution decisions were excluded from evaluation.

## Baseball insights
- The **pseudo-full game manager is the champion**: 57.1% vs. Lindsey over
  80,000 sims; half game 56.3%; deep Lindsey 53.3%; vanilla MCTS *lost* to the
  baseline (48.3%) — naive tree search with random rollouts is not good enough
  for in-game use.
- Managers who managed closer to a 1963 operations-research strategy won a
  statistically significant majority of 2023 games — six decades on, Lindsey
  still beats gut feel.
- **Cash was wrong to pull Snell**: staying with Snell vs. Betts = 0.584 win
  probability, bringing in Anderson = 0.554. (Though Anderson was the *best*
  reliever choice available, and the authors concede fatigue modeling might
  have sided with Cash.)
- **Boone was basically right**: his entire 10th inning cost the Yankees only
  ~0.0096 win probability. Cortes over Hill to face Ohtani was the *optimal*
  call (0.669 vs 0.627) despite the criticism; the IBB to Betts cost 0.009.
  "We encourage Yankees fans to be more forgiving."
