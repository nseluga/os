---
name: feedback-research-log-entry-format
description: "How to write decision-log and lab-notebook entries on research projects — five fields only, tight, and never a narration of the working session"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 72e69333-210f-4797-a60b-e42f0f35ef75
  modified: 2026-07-31T03:11:05.698Z
---

Applies whenever `/research-partner` or `/research-review` appends to a project's
decision log or lab notebook. Nate had to have both files rewritten twice on
2026-07-30 because entries had grown into essays.

## Field lists are closed

Decision log — exactly these, no others:
`Decision` / `Alternatives` / `Rationale` / `Reference` (optional) / `Revisit if`

Lab notebook — exactly these:
`Did` / `Why` / `Found` / `Learned` / `Next`

**Never invent a field.** Almost all the bloat that had to be cleaned up lived in
invented ones: `Tier`, `Effect`, `Status`, `Correction this entry carries`,
`Consequences carried forward`, `Known open at time of writing`, `Related gap
found while writing this`, `Named fallback and its firing condition`. Anything
that doesn't fit a canonical field belongs in the notebook, in `results/`, or
nowhere. Fold it into `Rationale` or `Revisit if` instead of opening a new bullet.

## Length

One to three sentences per field; at most two per topic covered. Match the
register of the first entry in each file — that entry is the reference for
"right length," not the most recent one. If the entry doesn't fit on a screen,
the excess was never a decision.

## These are Nate's design record, not a session transcript

- Never narrate the working session, the tooling, or who proposed what.
- **Never enumerate the agent's own errors, miscitations, corrections, or
  retracted readings.** A decision that changed is recorded as the decision, not
  as a story about how it changed. Same for "caught before it reached a claim"
  framings.
- The repo docs are read by outside reviewers, so process notes about how the
  work was produced stay out of them — put durable ones here in memory instead.

## Numbers cite the artifact, they don't inline it

No CI dumps, sensitivity tables, or per-threshold sweeps in the log. A number
appears only when it *is* the decision — "removes 36.6% of the low stratum" earns
its place; a three-way interval comparison does not.

## Supersession

Mark the old entry's title `— SUPERSEDED <date>, see below` and keep it to
Decision / Alternatives / Rationale / Revisit if, then write a short new entry.
Never a full retained entry plus a long override entry.

## Known drift

`research-standards.md` §4 lists a `Tier` field that the hitter-embedding repo
template omits. Follow the repo's template; raise the divergence rather than
silently adding `Tier` back.

**Related:** [[skills/research-partner/SKILL|research-partner]] · [[skills/research-review/SKILL|research-review]] · [[research-standards]]
