# Agent Glossary — what each agent buys, costs, and when it's waste

Read this when choosing a team in `convergence-loop.md` → "Team selection".

Rough unit: **one spawn ≈ 125k tokens**. A team of 7 is ~8× a team of 1, so the
skip decisions below are where nearly all the cost of a run is decided.

The **Waste when** field is the load-bearing one. Every agent here sounds worth
spawning if you only read what it buys.

---

## dt-analyze
**Buys you:** a shared file/dataflow map, so five later agents don't each pay to
rediscover the same layout. Its value scales with team size.
**Costs:** 1 spawn (Sonnet/medium; Haiku for its `Explore` fan-out).
**Waste when:** the item is single-file, the plan item already names the files,
or a live `analyze-report.md` from this run already covers the area. With a
2-agent team it rarely repays itself — it's an amortiser, and there's nothing to
amortise across.

## dt-research
**Buys you:** current external-tool facts that training data gets wrong — API
shapes, current package names, deprecations.
**Costs:** 1 spawn (Sonnet/medium), near-zero on a cache hit.
**Waste when:** every package the item touches already has a note in
`research-notes/`, or the question is about *this* codebase's architecture —
`system-standards.md` owns that, and research will not answer it.
**Not optional:** the cache check itself always runs. Skipping the *spawn* is the
common case; skipping the *check* is a bug.

## dt-engineer
**Buys you:** the build. Always in the team. Also runs in **outline mode** for
design exploration — same agent, ≤30 lines of approach instead of code.
**Costs:** 1 spawn to build; 2–3 cheap outline spawns when exploration runs.
**Waste when:** never — but the *model* is a real decision. Sonnet handles a
bounded change on a settled pattern; paying Opus there buys nothing a fix pass
wouldn't have caught for less.

## dt-qa
**Buys you:** the binary gate. Converts `done when:` into executed tests, and
classifies failures as bug-level vs design-level — which is what steers the rest
of the loop.
**Costs:** 1 spawn, plus re-gates. `tests+behavioral` costs substantially more
than `tests`: seeding data, a real server, a real dev DB, browser QA.
**Waste when:** copy, docs, static config, comments — where the build check
already proves it. Never below Sonnet; a weak gate passes broken code with
confidence, which is worse than no gate.

## dt-review
**Buys you:** what QA structurally cannot. QA tests the criteria you thought to
write; review finds what you didn't — the N+1, the unindexed scan, the missing
timeout, the auth hole nobody specified.
**Costs:** 1 spawn at Opus/high (its floor — see below), plus the fix pass its
findings trigger.
**Waste when:** the `risk:` line says the failure is **loud and revertible**. A
wrong nav renders wrong on first page load; a reviewer tells you nothing the
page didn't. This is the single biggest saving available and the one most often
left on the table.
**Why Opus is the floor, not an escalation:** you only spawn a reviewer on an
item whose risk earned one, so the cheap-review case doesn't exist. A reviewer
below the tier of the builder that wrote the code finds nothing worth the spawn.

## dt-fix
**Buys you:** applies QA failures and review findings.
**Costs:** 1 spawn per pass. Match the builder's tier — a fixer below the builder
re-introduces what the builder got right.
**Waste when:** there are no findings. Don't spawn it to "polish".

## dt-ui
**Buys you:** layout, hierarchy, interaction states, responsiveness, a11y.
**Costs:** 1 spawn.
**Waste when:** the change isn't user-visible frontend. Backend items with a
thin template do not need it.

---

## Worked routing examples

Four quadrants. Follow the nearest one rather than re-deriving.

### 1. Loud + easy → Engineer + build check

```
task: Render the hero banner as a contained bottom-anchored box inside the hero
risk: banner sits in the wrong place; visible on first page load
difficulty: low — CSS containment on an existing component
```

**Team:** `dt-engineer` (Sonnet/medium) + the project build check.
**Skipped:** QA suite (the build check proves it), review (loud + revertible),
analyze (single file), research (no new package).

```
TEAM hero banner — risk: loud, revertible difficulty: low → engineer | skipped: qa+review, failure visible on load
```

### 2. Loud + hard → parallel outlines + Engineer + QA + extra attempts, **no review**

```
task: Render the knowledge graph as an interactive force-directed layout
risk: graph looks wrong or unreadable; obvious the moment the page opens
difficulty: open — layout algorithm, tick budget, and collision strategy are
            genuinely competing approaches
```

**Team:** 2 × `dt-engineer` in parallel, **outline only** (Opus/high — one
prompted for a physics-tick approach, one for precomputed layout) → pick →
1 × `dt-engineer` builds the winner (Sonnet/high) → `dt-qa` (`tests`).
MAX_ATTEMPTS 5.
**Skipped:** `dt-review` — difficulty is not risk. This item may take four
attempts, and none of them are made better by a reviewer; a wrong layout is its
own bug report.

```
TEAM knowledge graph — risk: loud, revertible difficulty: open: layout algorithm → 2 outlines+engineer+qa | skipped: review, failure is self-evident on render
```

This is the quadrant the old single-axis schema got wrong in the expensive
direction: it read "hard" as "full track" and bought a review pass that had
nothing to find.

### 3. Silent + easy → Engineer + QA(behavioral) + review at Opus, **no exploration**

```
task: Wire the Stripe webhook handler for checkout.session.completed
risk: a missed or double-processed event charges a customer wrong, and nobody
      notices until the bank statement — silent and not revertible
difficulty: low — Stripe's idempotency pattern is well-established; the only
            open question is where the event log lives
```

**Team:** `dt-research` (only if no `stripe` note cached) → `dt-engineer`
(Opus/high) → `dt-qa` (`tests+behavioral`) → `dt-review` (Opus/high) →
`dt-fix` (Opus/high). Review runs **sequentially**, after QA is green.
**Skipped:** design exploration — the pattern is settled. Three engineers
outlining a documented idempotency key is the other expensive mistake.

```
TEAM stripe webhook — risk: silent, not revertible difficulty: low → engineer(opus)+qa(behavioral)+review(opus) | skipped: design exploration, pattern is settled
```

### 4. Silent + hard → the full engine

```
task: Write RLS policies — admins read/write all rows; subs read only their
      assigned jobs and only non-financial fields
risk: a policy gap exposes another client's financial data; nothing surfaces it
      until someone looks, and the leak is not revertible
difficulty: open — role model, column-level masking, and policy composition
            across four tables are all unsettled
```

**Team:** `dt-analyze` ∥ `dt-research` (supabase RLS, if uncached) →
3 × `dt-engineer` in parallel, **outline only** (Fable/medium — one per role
model: policy-per-table, view-based masking, security-definer functions) →
pick → 1 × `dt-engineer` builds the winner (Fable/medium) → `dt-qa`
(`tests+behavioral`) → `dt-review` (Fable) → `dt-fix` (Fable).
**Skipped:** nothing. This is the item the maximal engine exists for — and it
should be rare. If a plan has many of these, the plan is the problem.

```
TEAM RLS policies — risk: silent, not revertible difficulty: open: role model + masking → analyze+research+3 outlines+engineer+qa(behavioral)+review, all fable | skipped: nothing
```

---

## Sanity check on your own choice

- Spawning `dt-review` on a loud, revertible failure? Cut it.
- Spawning design exploration on a settled pattern? Cut it.
- Spawning `dt-analyze` on a single-file item? Cut it.
- Buying `tests+behavioral` for code no user or route reaches? Downgrade to `tests`.
- Writing `skipped: nothing` on anything but quadrant 4? Look again.
