# Optimizing Baseball Fielder Positioning with Consideration for Adaptable Hitters

**File:** `melville-2024-fielder-positioning.pdf`
**Authors:** Melville, Wise, Nielson, Mott, Archibald, Grimsman (~2024; same
group as [[melville-2023-game-theory-pitch-sequencing]], with Texas Rangers
proprietary-data collaboration)

## Questions answered
- Where should the seven fielders stand against a *specific* hitter to
  maximize outs or minimize runs?
- Does the optimization survive an adaptable hitter who watches the defense
  and changes his approach (going oppo, bunting)?
- Was the 2023 shift ban even necessary?

## Models used
- **Batter-specific batted-ball distributions**: Bayesian hierarchical models
  of the joint distribution p(spray, launch, exit speed), factored as
  p(h)·p(v|h)·p(s|v):
  - Spray angle p(h): mixture of two beta distributions; posteriors via ADVI
    (PyMC).
  - Launch angle p(v|h): normals conditioned on pull vs. oppo; NUTS sampling.
  - Exit speed p(s|v): gammas on flipped speed (s_max − s), one per launch
    angle type (GB / LD / FB / PU); NUTS. Priors fit empirically by MLE across
    the player population.
- **Out models** (logistic regressions on 2023 Statcast, average starting
  positions from Baseball Savant):
  - Ground balls: features = min |spray angle difference to nearest infielder|
    and "ball time to fielder" (depth ÷ exit speed), with a quadratic term.
  - Non-ground balls: feature = hang time − (distance to landing spot ÷ 27
    ft/s MLB avg sprint speed). Hang time / landing distance predicted by
    XGBoost models trained on Alan Nathan's trajectory calculator outputs.
  - Both calibration-checked on holdout data.
- **Run objective**: hit-type classifier → expected wOBA of un-fielded balls,
  using 2023 wOBA weights (wOBA is affine in runs).
- **Optimizer**: projected mini-batch stochastic gradient descent with
  momentum over a *continuous* positioning space (vs. prior work's discrete
  grids), with projection steps enforcing the 2023 shift-ban rules (infielders
  on the dirt, two per side of second base, 1B within 40 ft of the bag).
- **Adaptable-hitter game**: zero-sum sequential game — defense commits to a
  positioning, batter observes it and picks a batted-ball distribution from an
  action set 𝒟 (e.g. {pull, oppo} or {bunt, swing away}); equilibrium found by
  gradient descent against the batter's best response.

## Methodology — defending & translating baseball assumptions
- The independence structure is *shown, not assumed*: partitioned histograms
  demonstrate launch angle depends on spray direction, and that exit speed is
  conditionally independent of spray given launch angle — that empirical check
  licenses the factorization p(h)p(v|h)p(s|v).
- Hierarchical priors are motivated by a real roster problem: rookies with
  sparse ball-in-play data borrow strength from the population instead of
  overfitting to 30 batted balls.
- Handedness handled by mirroring lefties' spray angles so all hitters share
  information; switch hitters get two separate distributions.
- The weakest assumption — that fielders stood at Savant's *average* starting
  positions — is confronted head-on: the public model's expected BA (0.319)
  misses actual (0.293), so they re-ran everything with the Texas Rangers'
  proprietary true starting positions (expected 0.292 vs actual 0.293) and
  confirmed the conclusions hold.
- Sensible data hygiene translated from baseball reality: 2023-only data to
  avoid pre-ban extreme shifts; plays with baserunners removed (holding the
  runner moves the 1B); "standard" outfield alignments only; Tropicana Field
  chosen as the physics testbed because a dome has constant atmospherics.
- When the optimizer produced baseball nonsense (infielders absurdly deep), a
  100-ft depth constraint was added — and they admit the public model's
  depth–out relationship is under-learned, deferring the bunt-depth question
  to the Rangers model.

## Baseball insights
- Optimizing to minimize wOBA beats optimizing to maximize outs *on both
  metrics* — chase run value, not outs.
- Individualized positioning is worth roughly **31 hits and 22.5 runs saved
  per team per season** vs. league-average positioning (public model); the
  Rangers-data model says ~25 outs per team.
- Real "shift-beaters" exist (Josh Bell L, Josh Rojas, Chas McCormick, Adam
  Frazier, Tyler O'Neill) — but even for McCormick, his pull approach
  *dominates* his oppo approach, so the equilibrium defense is just the
  anti-pull alignment. Adapting oppo doesn't actually pay for him.
- **The bunt is the real shift-killer**: against a shifted infield, expected
  BA on a bunt is .453 for Carlos Santana and .574 for Joey Gallo. A credible
  bunt threat forces the equilibrium third baseman shallower, and the hitter
  then gains ~4 points of BA *even when swinging away*. Quantitative
  confirmation of Tango/Lichtman/Dolphin's claim in The Book.
- Punchline: the 2023 shift ban may have been unnecessary — teaching pull-heavy
  lefties to bunt would have raised batting averages without a rule change.
