# A Game Theoretical Approach to Optimal Pitch Sequencing

**File:** `melville-2023-game-theory-pitch-sequencing.pdf`
**Authors:** Melville, Melville, Dawson, Nieves-Rivera, Archibald, Grimsman (MIT Sloan 2023)

## Questions answered
- What is the game-theoretically optimal pitch (type + location) for a specific
  pitcher vs. a specific batter at a specific count, given the pitches already
  thrown in the plate appearance?
- How much information does the batter actually have when deciding to swing,
  and how does that change the optimal strategy?
- How close do real MLB batters and pitchers come to playing optimally?

## Models used
- **Three zero-sum game models** of the batter/pitcher matchup, differing in
  what the batter observes before the swing decision:
  1. *Simultaneous* (batter sees nothing) → Nash equilibrium, solved by linear
     programming.
  2. *Sequential* (batter sees the full pitch) → Stackelberg equilibrium,
     solved by exhaustive search.
  3. *Decision-point* (batter sees the trajectory only up to a decision point
     24 ft from the plate; pitch type stays hidden) → "decision-point
     equilibrium," solved by LP with per-tunnel strategy constraints. This is
     the paper's preferred, most realistic model.
- **OptimusPitch (OP)**: recurrent neural net predicting a distribution over 9
  pitch outcomes (B, CS, SS, F, 1B, 2B, 3B, HR, O). Batter embedding (à la
  (batter|pitcher)2vec) + hidden state accumulating all prior pitches and
  their outcomes in the PA; two 5-layer feed-forward stacks. Trained on
  Statcast 2021–22 (75/25 split), verified with calibration plots.
- **Utility function**: count-dependent expected run value of each outcome
  (Sheehan/Tango run values), not OBP — so a HR is worth more than a single.
- **Pitcher command model (TBA)**: Bayesian execution-skill estimation. Miss
  distance modeled as symmetric 2D Gaussian noise around the intended target;
  posterior over 66 hypothesis σ values (0.17–2.81 ft) updated from each
  pitcher's last ≤1000 pitches per pitch type, with likely aiming "focal
  points" as latent targets.
- **Tunnel geometry**: Alan Nathan's trajectory physics maps
  (pitch type, plate location) → decision point; linear regression learns the
  inverse map.

## Methodology — defending & translating baseball assumptions
A model example of how to argue for a game formulation:
- Rejects prior work's simultaneous-decision assumption (Douglas et al.) by
  *demonstrating its absurd implication*: the Nash strategy tells Jansen to
  throw sliders a half-foot below the zone because the model thinks Phillips
  swings 54% regardless — but the outcome model says his true swing rate on
  that pitch is <13%, so it's not a real equilibrium.
- Grounds the decision point at 24 ft in Baseball Prospectus's pitch-tunnels
  research rather than picking it arbitrarily; "tunnel" and "decision point"
  are treated as the same object.
- Models pitcher execution error because pitchers demonstrably miss targets;
  utility is computed by convolving the intended-target value surface with the
  pitcher's noise distribution.
- Validates its own idealizations empirically: batters made the "optimal"
  swing decision only ~70% of the time under full observation and 71% at
  tunnel level; pitchers threw the optimal pitch type just 48% of the time.
  The equilibrium is then *reinterpreted* as a minimax guarantee — the pitcher
  strategy minimizing the upper bound of a perfect batter's response — so
  suboptimal real batters only make it better for the pitcher.
- Honestly flags the impossible part: a batter can't sample from a mixed
  strategy (e.g. swing 12% of the time) in the fraction of a second after the
  decision point.

## Baseball insights
- Sequence effects are real but concentrated late in the PA: OP barely beats a
  memoryless clone on average (cross-entropy 1.11 vs 1.12) but wins clearly on
  deeper pitches — first quantitative evidence a model can *learn* sequencing
  effects rather than just detect that predictability is bad.
- "Hard in, soft away" gets model support: Diaz's strikeout slider to
  Moustakas rated −0.14 expected run value with sequence context vs −0.07
  without.
- As pitcher command degrades (σ grows), the optimal target converges toward
  the middle of the zone — command is what makes corner-painting worthwhile.
- Tunneling can make swinging at a ball *correct*: in the Jansen/Phillips
  example, taking a sinker in a shared tunnel is costlier than swinging at the
  slider below the zone, so the equilibrium says swing at everything in that
  tunnel. Fans blaming hitters for "chasing" tunneled pitches are often wrong.
- If the opponent is known to be suboptimal, deviating from equilibrium is
  rational — deGrom's outside 102 mph fastball to Soto beat the "optimal"
  changeup down the middle precisely because Soto chased.
