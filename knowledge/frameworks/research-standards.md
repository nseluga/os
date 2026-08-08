# Research Standards

Shared process standards for research work. Loaded by both `/research-partner`
(build-time) and `/research-review` (review-time). This file is about **process,
not content** — domain knowledge (baseball, ML, economics) never lives here; it
comes from each project's research manifest and library.

**Related:** [[notebook-code-standards]]

## 1. Challenge checklist

Every major decision must be defensible across seven categories:

1. **Data choice** — why this source, this time range, this level of aggregation?
2. **Feature engineering** — what mechanism does this feature proxy? Could it be a confounder?
3. **Modeling approach** — what alternatives were considered and ruled out, and why?
4. **Evaluation methodology** — is the test set truly held out? Is the metric the right one for the research question?
5. **Statistical assumptions** — independence, stationarity, distributional assumptions — are they met?
6. **Domain assumptions** — does the result make sense given how the domain actually works? (Use the domain sanity questions from the project manifest.)
7. **Interpretation** — is causation being claimed where only correlation is shown?

Hunt specifically for:

- Hidden assumptions
- Selection bias and survivorship bias
- Data leakage
- Confounding variables
- Small-sample fragility
- Overfitting risk
- Correlation-vs-causation slippage

## 2. Pushback taxonomy

Classify every contested decision into exactly one tier. The tier — not
strength of feeling — determines the response.

- **Tier 1 — BLOCK.** Data leakage, evaluation-validity violations,
  statistical-assumption violations, or violations of the project's own frozen
  rules (as listed in the manifest). Argue with a reference and do not proceed
  until the issue is resolved or the user explicitly overrides in writing (the
  override goes in the decision log).
- **Tier 2 — PROPOSE.** Choices that are empirically resolvable (architecture
  variants, feature inclusion, hyperparameter families). Do not debate at
  length — propose the cheapest ablation/test that settles it, sized to the
  project's compute budget. If the project mandates ablation-decided choices,
  enforce that rule.
- **Tier 3 — DEFER.** Taste, scope, prioritization, and deadline tradeoffs.
  State the tradeoffs concretely, give a recommendation, then explicitly mark
  the decision as the user's and accept it without relitigating.

### Pushback block format

All Tier 1/2 interjections use this structure, visually set off from the
surrounding work:

> **⚠ Pushback (Tier N)**
> - **Claim:** what is wrong or risky, in one sentence
> - **Evidence:** the concrete mechanism or failure mode
> - **Reference:** citation per §3 (or "unverified — parametric" if none)
> - **Resolution:** what would change my mind / the ablation that settles it

## 3. Reference policy

Two tiers. Default A. Escalate to B only on trigger (B spawns agents, costs
tokens).

### 3a. Tier A — direct check (default, no subagents)

- Search before proposing/adopting, unprompted. Applies to user's proposals too.
- Library first, then one WebSearch/WebFetch pass. No subagent.
- Tag reliability, highest wins on conflict: peer-reviewed/replicated >
  official data/preprint > primary-source practitioner report > blog/anecdote.
- Quote the exact supporting passage, not just title/URL — no quote, no source.
- Save worthwhile finds to the library (one file per doc).
- Nothing found → say so explicitly, don't proceed silently.
- Memory-only claims → flag "unverified"; can't anchor a Tier 1 block alone.

### 3b. Tier B — contested-claim verify (rare, on trigger only)

Trigger: claim is sole evidence for a Tier 1 block, Tier A sources conflict,
or a 3c fidelity check fails.

1. Spawn 2 agents: one FOR, one AGAINST. Each searches independently, returns
   position + evidence w/ tier + quote + confidence (1-10).
2. Agree → cite stronger-tier source, done.
3. Disagree → don't resolve it — surface both to user as `Reference:` or a
   Tier 3 call.

Never for routine sourcing or Tier 2/3 pushback.

### 3c. Citation fidelity check (review time, `/research-review` only)

Don't redo 3a's search — audit what's already logged.

- For each decision-log `Reference:`: fetch the cited source, confirm the
  quote is accurate/in context and the tier assignment holds.
- No reference logged → that's a finding itself (3a was skipped); don't
  backfill it by searching.
- Fails (misquoted, wrong tier, source unreachable) → triggers 3b.

## 4. Decision log format

Every settled decision gets an append-only entry in the project's decision log
(path in the manifest):

```
## <YYYY-MM-DD> — <decision title>
- **Decision:** what was chosen
- **Alternatives:** what was considered and rejected
- **Rationale:** why, in terms a skeptical reviewer would accept
- **Reference:** supporting citation(s), or "none — judgment call"
- **Revisit if:** the condition under which this should be reopened
```

Frozen decisions are never silently edited — reopening one requires a new
entry that names the old one and the evidence that justified reopening.

## 5. Lab notebook format

One entry per working session, appended to the project's notebook (path in the
manifest). Written for future-you and interview prep:

```
## <YYYY-MM-DD> — <session focus>
- **Did:** what was built/run, and where it lives
- **Why:** the reasoning, at explain-it-in-an-interview depth
- **Learned:** new concepts introduced this session (these mark the concept as
  "explained" — see teaching rule)
- **Next:** the concrete next step
```

## 6. Evidence standards

- A claim about model behavior requires a run, not an expectation.
- Negative results are kept and reported, never discarded.
- Any coverage shortcut (sampling, top-N, skipped strata) is stated where the
  result is stated — silent truncation reads as full coverage.
- Numbers are reproducible: seeded, config-driven, with the config committed.
