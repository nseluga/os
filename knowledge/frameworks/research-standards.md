# Research Standards

Shared process standards for research work. Loaded by both `/research-partner`
(build-time) and `/research-review` (review-time). This file is about **process,
not content** — domain knowledge (baseball, ML, economics) never lives here; it
comes from each project's research manifest and library.

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

- **Library first.** Cite from the project's library area (see manifest) when
  the topic is covered. Cite the document and the specific section or finding,
  not the paper title alone.
- **Search for gaps.** When the library doesn't cover a topic that matters,
  search for a source before asserting. Add worthwhile findings to the library
  (one file per document, per the library-notes format).
- **Parametric knowledge is always flagged.** Anything asserted from memory
  without a checkable source is labeled "unverified" inline. Unverified claims
  cannot anchor a Tier 1 block on their own.

## 4. Decision log format

Every settled decision gets an append-only entry in the project's decision log
(path in the manifest):

```
## <YYYY-MM-DD> — <decision title>
- **Decision:** what was chosen
- **Alternatives:** what was considered and rejected
- **Rationale:** why, in terms a skeptical reviewer would accept
- **Reference:** supporting citation(s), or "none — judgment call"
- **Tier:** 1/2/3, and whether it was a user override
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
- **Ideas parked:** proposals deferred to the next phase boundary
- **Next:** the concrete next step
```

## 6. Evidence standards

- A claim about model behavior requires a run, not an expectation.
- Negative results are kept and reported, never discarded.
- Any coverage shortcut (sampling, top-N, skipped strata) is stated where the
  result is stated — silent truncation reads as full coverage.
- Numbers are reproducible: seeded, config-driven, with the config committed.
