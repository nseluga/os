---
name: prescribe-stakes-not-process
description: "When designing agent orchestration, the human author should specify stakes and uncertainty; the runtime orchestrator should choose the process. Authoring-time process prescription degenerates to round-up-everything."
metadata:
  node_type: memory
  type: feedback
---

When building any system where a human hands work to an agent (plan files, task
specs, ticket templates, skill inputs), split the contract this way:

**Author specifies what only they know** — the consequence of failure, and why
the work might be hard. **The runtime chooses the process** — which agents, which
models, how many attempts, which gates.

Three rules that make this work:

**1. Consequences, not ratings.** `risk: high` inflates and is unactionable.
"A replayed event double-charges the customer and we find out from the bank
statement" is a factual claim about the world — it resists inflation and it
carries the routing signal (silent vs loud failure). Never ask a human to
self-assess importance on a scale; ask what breaks and how they'd find out.

**2. Stakes and difficulty are independent axes.** *Hard-but-harmless* (a fiddly
layout algorithm — more attempts, no reviewer) and *easy-but-dangerous* (a
settled webhook pattern — a top-tier reviewer, no design exploration) are the
two cases a single "importance" score necessarily mis-routes, and they are where
a run wastes the most money.

**3. Latitude needs a forced declaration, not a request.** "Do as much as
necessary but no more" is unenforceable prose. Under-running is a visible
failure; over-running is invisible tokens — so an agent with latitude and no
counter-signal drifts heavy. Make it *write down* what it chose and what it
skipped, before it acts. Cheap, self-correcting, and it produces the data to
tune the guidelines on evidence instead of a second guess.

**Why:** Evidence from Nate's own plans, 2026-07-28. `bcns-client-coventry`'s
PLAN.md set 20 of 20 items to `track: full` and 16 to `flag:`, then wrote **zero**
of the speed/reliability criteria those choices mandated. `project-dashboard`
waived 5 of 8. A human, in a careful grilling session, rounded up everything —
so the field carried no information — and ignored the rules it triggered.
Prescription that isn't enforced by control flow is already being ignored; you
are choosing between "ceremonial and ignored" and "explicitly absent."

**How to apply:** Before adding a field that makes the author classify *process*
(a track, a tier, a priority number), ask: does the runtime have more information
about this at decision time than the author had at authoring time? For anything
it can read from the code, it does — so capture the stakes instead and let it
decide. Pair with the Pre-Flight Principle: every rule you write needs a
verification step, or it won't survive creative flow. See
[[tool-building-efficiency-without-sacrifice]] and [[dev-team-learnings]].
