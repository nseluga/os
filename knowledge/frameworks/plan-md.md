# PLAN.md Reference

A PLAN.md is the pre-run contract for any autonomous or semi-autonomous session.
It defines **what to build** (or improve), in what order, and exactly how to
know each item is done. Agents read it at startup; you write it before the session.

---

## When you need one

Use PLAN.md when:
- Running `/dev-team-auto` (it requires one — the outer loop iterates over it)
- Running `/dev-team` on a multi-item backlog (it reads PLAN.md if no inline arg is given)
- Any overnight/unattended run where you want a stop marker or a resumable queue

Skip it (use an inline arg or TASK.md) when:
- You have a single task and you're running it interactively right now
- The task is disposable and you won't need to resume it

---

## Format — dev-team runs

Each item is a YAML-ish block under a top-level list. Ordering is execution order.

```markdown
- task: <one-line imperative: what to build>
  done when:
    - <testable criterion>
    - <testable criterion>
  risk: <what breaks if this is wrong, and how you'd find out>
  difficulty: <why this might not work first try — or `low` and why it's obvious>
  status: not started
```

### Fields

**`task:`** (required) — one imperative sentence scoped to one logical change.
If you can't describe it in one sentence, split the item.

**`done when:`** (required) — the acceptance criteria QA converts to tests and
uses as its binary gate. See "Writing good criteria" below.

**`status:`** (required, start at `not started`) — the agent updates this in
place as items resolve. Values: `not started` | `in progress` | `done` | `blocked`.
Do not change this manually mid-run.

**`risk:`** (required) — one line: **what breaks if this is wrong, and how you'd
find out.** The second half is not optional — it is the half the orchestrator
routes on.

The decisive property is **silent vs loud**. A failure the user sees on first
page load needs no reviewer to find it; a failure you learn about from a bank
statement three weeks later does. Say which, in plain words:

```
risk: a replayed event double-charges the customer, and nobody notices until
      the bank statement — silent, and not revertible
risk: nav renders wrong on five pages; obvious on first page load
risk: none — copy only
```

Write the consequence, not a rating. `risk: high` tells the orchestrator
nothing it can act on, and ratings inflate — a factual claim about the world
doesn't. `risk: none` is a valid and common answer; most items are not risky.

**`difficulty:`** (required) — one line: **why this might not work first try**,
or `low` plus the reason it's obvious. Names open design space, unfamiliar
tooling, or fiddly behaviour.

```
difficulty: open — role model, column masking, and policy composition across
            four tables are genuinely competing designs
difficulty: low — Stripe's idempotency pattern is well-established
```

**Risk and difficulty are independent, and that is the point.** They buy
different things: risk buys a review pass, a higher model tier, and a
behavioral gate; difficulty buys competing outlines and more attempts. A
one-axis "importance" score cannot express a hard-but-harmless item (a fiddly
layout algorithm — several attempts, no reviewer) or an easy-but-dangerous one
(a settled webhook pattern — a top-tier reviewer, no exploration), and those two
are exactly where a run wastes the most money.

The orchestrator chooses the agent team from these two lines — see
`~/os/skills/dev-team/agent-glossary.md`. The plan does not name agents,
models, or attempt counts.

**`parallel-group:`** (optional) — consecutive items sharing the same value run
concurrently under `/dev-team-auto` (up to 3 at once, each in its own worktree
branch, merged in completion order). Set it only when the items are file- and
resource-disjoint: no shared files, no shared schema/migration, no
producer/consumer relationship between them. Never infer independence at
run-time — this field is the only signal `/dev-team-auto` trusts. The plan
author (or plan-md's own scan of the codebase) sets it when writing the plan,
not the executing agent.

---

## The preamble (context above the items)

Everything above the first item block (`- task:` for dev-team) is an
optional **preamble**: orientation the orchestrator reads for global guidance
but does not execute as an item. Recommended by default for every file-based
PLAN.md; the only thing that varies is depth. Skip it only for a throwaway
inline/TASK.md task.

The loop reads top-to-bottom and is LLM-driven, so a clearly-separated preamble
is safe — but keep the items unambiguous: start each with the exact `- task:`
block format, and never put an executable item inside the preamble.
Close the preamble with a `---` rule before the first item.

**Shape (all parts optional, scale to the plan):**
- An H1 title.
- A one-to-three-line **Status / where-it-stands** — what's done, what's next,
  any blocker. Mirrors the project README's stance so a reader orients fast.
- A short **Global rules / conventions** block: constraints that apply to *every*
  item and that the agent must respect (stack limits, voice rules, "AI is
  enhancement-only", accuracy rules). These are the rubric the loop carries into
  each item — not per-item criteria.
- A **pointer** to fuller context (`CLAUDE.md`, README, a reference file) rather
  than duplicating it. The preamble is a lean orientation; the exhaustive spec
  lives in the auto-loaded `CLAUDE.md` or the project README. Duplicated context
  drifts — link, don't copy.

The item list remains the contract; the preamble only frames it. Keep it short
enough that it never competes with the items for attention. (The examples below
omit the preamble for brevity — a real file should carry one.)

## The stop marker

```markdown
> **⚠️ AUTONOMOUS RUN — STOP HERE**
```

Place this line between items. Agents stop the moment they reach or pass it.
Items below the marker are not touched.

Use it to:
- Require human review before a risky item (e.g. after a DB migration, before a
  deploy-adjacent change)
- Break a large plan into sessions — move the marker down each morning

---

## Writing good `done when:` criteria (dev-team)

This is the highest-leverage field. QA converts it directly into tests.
Vague criteria → vague tests → false PASS verdicts.

**A criterion is testable when:**
- It describes a *behavior*, not an intent. "Returns 429 after 10 requests/min"
  not "rate limiting is implemented."
- It names a specific observable: status code, DB row, file, rendered text,
  error message.
- A skeptic could verify it without asking you anything.
- It would fail meaningfully if the code were deleted.

**Red flags — rewrite these:**
| Vague | Better |
|---|---|
| "Works correctly" | "Returns the correct total including tax for a cart with 3 items" |
| "Is handled gracefully" | "A missing `user_id` param returns a 400 with `error: user_id required`" |
| "Performance is acceptable" | "Median response time under load (50 rps) stays below 200ms" |
| "Tests pass" | "The UserRepository.findById test covers a non-existent ID and returns null" |

**Quantity:** 2–4 per item. More than 5 usually means the item should be split.
Fewer than 2 usually means the item is under-specified.

**Hygiene criterion:** include "Existing passing tests remain passing" when
regression risk is real. Skip it for trivial items where it's obvious.

**Speed + reliability criteria — conditional on the item, not on its size.**
Buy each one only where it measures something. A speed criterion forces QA to
seed data and run the app, which is the most expensive part of the gate.

- **Speed** — add only when the item's cost **grows with rows or request rate**:
  a query, a list endpoint, a job over a table, an N+1-shaped render, an
  index-dependent lookup. Format: "median of 5 runs of <operation> stays under
  <threshold> with <N> rows seeded." Defaults when you have no better number:
  API route < 200ms, page render < 1s, background job < 30s. Set thresholds at
  ~2× the real target — the criterion catches regressions (an unindexed scan, an
  N+1 loop), it doesn't benchmark the laptop — and always name the seed size; a
  timing against an empty DB proves nothing.
  **Skip it silently** for pure logic, UI, copy, config, and one-shot scripts.
  Nothing grows, so the test proves nothing. No waiver line.
- **Reliability** — add only when a failure mode can be **pinned by a test**:
  double-submit/retry creates no duplicate row; a down dependency degrades to a
  defined fallback within a timeout instead of hanging; behavior holds under both
  `TZ=UTC` and a non-UTC TZ; invalid input at the boundary returns the defined
  error, not a 500. Skip it when the only failure mode is "the logic is wrong" —
  the functional criteria already cover that.

**When the `risk:` line describes a silent or non-revertible failure, both are
required** — that is precisely the case where tests written from the functional
criteria miss the defect. There, waive only with a visible
`speed: N/A — <reason>` line the Reviewer can challenge. Everywhere else their
absence is the default, not an omission.

QA verifies speed criteria by measurement (running the timed test), never by
inspection.

---

## Writing items for cheaper agents

Plan items are mostly executed by Sonnet-tier agents. A well-written item lets a
cheaper model succeed on attempt 1; a vague one burns attempts (and escalations
to Opus/Fable) rediscovering what you already knew. Rules:

- **One logical change per item.** If the task sentence needs an "and", split it.
  Small items converge in one loop pass; compound ones fork alternatives.
- **Name known files and functions.** "Add the toggle to `src/components/Nav.astro`"
  removes an exploration pass. Only omit paths when you genuinely don't know them.
- **State the approach when you have one.** "Reuse the existing `readManual()`
  helper" is one line that prevents an alternative-engineer fork. Leave the
  approach open only when you actually want design exploration.
- **Write `risk:` as a consequence, never a rating.** "High" is unactionable and
  inflates; "a duplicate charge nobody catches until the bank statement" tells
  the orchestrator to buy a reviewer, and "obvious on first page load" tells it
  not to. This one line decides most of what the item costs.
- **Don't describe the process.** No agents, models, attempt counts, or gate
  modes in the plan. You know what breaks and why it's hard; the orchestrator
  knows what has already been mapped, what the code looks like, and what each
  agent costs. Describing the team from the plan overrides better information.
- **Mark disjoint items `parallel-group:`.** When the codebase scan shows two
  consecutive items touch no common file, schema, or dependency chain, tag
  them with a shared `parallel-group:` value so `/dev-team-auto` runs them
  concurrently. Skip it when unsure — a wrong merge conflict costs more than
  sequential execution saved.
- **Global constraints go in the preamble once**, not repeated per item — agents
  read the preamble; duplication drifts.
- **Testable `done when:` always** (previous section) — it is the contract a
  cheap QA gate can enforce mechanically.

---

## Example PLAN.md — dev-team

```markdown
- task: Add rate limiting to /api/submit
  done when:
    - Requests beyond 10/min from the same IP receive a 429 response with Retry-After header
    - The rate limit window and max requests are configurable via environment variables
    - Median of 5 runs, a request under the limit responds in < 200ms with 100k rows in the request log seed
    - Two concurrent requests at the limit boundary yield exactly one 429 (no double-count or double-pass)
    - Existing passing tests remain passing
  risk: an ineffective limit lets an abuser exhaust the endpoint; nothing
        surfaces it until the bill or an outage — silent
  difficulty: low — standard fixed-window counter on the existing Redis client
  status: not started

- task: Rewrite session token signing to use HMAC-SHA256
  done when:
    - All tokens are signed with HMAC-SHA256 using a server-side secret
    - A token with a tampered payload fails verification and returns 401
    - Existing sessions are invalidated on deploy (no legacy unsigned tokens accepted)
  risk: a signing flaw lets anyone forge a session; silent, unrecoverable, and
        every issued token has to be treated as compromised
  difficulty: low — HMAC via the stdlib crypto module; the only open question is
        where the secret is read from
  speed: N/A — in-memory signing, no data-size dependence
  status: not started

- task: Replace inline SQL in UserRepository with parameterized queries
  done when:
    - No raw string interpolation remains in UserRepository
    - A test covers a value that would have triggered injection if unparameterized
    - Median of 5 runs, findByEmail stays under 50ms with 100k users seeded (parameterization didn't lose the index)
    - All existing UserRepository tests pass
  risk: an injection path survives, or parameterization silently drops the index
        and the table scans — neither shows up in normal use
  difficulty: low — mechanical rewrite against the existing driver's bind API
  status: not started
  parallel-group: a

- task: Add a /health endpoint returning build SHA and uptime
  done when:
    - GET /health returns 200 with { sha, uptimeSeconds } when the app is up
    - Returns 503 while a dependency the app requires (DB) is unreachable
  risk: none — a broken health check fails the first time anything curls it
  difficulty: low — one route, no state
  status: not started
  parallel-group: a

> **⚠️ AUTONOMOUS RUN — STOP HERE**

- task: Add last_login_at column to users table
  done when:
    - Migration runs without error on dev DB
    - Column is populated on every successful login, and a retried login write does not error or duplicate
    - Rolling back the migration restores the prior schema
  risk: a bad migration corrupts the users table in place; recoverable only from
        a backup, and a botched backfill is silent
  difficulty: low — single nullable column, existing migration tooling
  speed: N/A — single-column write on an existing indexed path
  status: not started
```

Note what the examples do *not* contain: no agent names, no models, no attempt
counts. Four of these five items are `difficulty: low` — that is normal. Most
work is not architecturally open; it is ordinary work with varying stakes.

## Lifecycle

| Phase | Action |
|---|---|
| Before a session | Author PLAN.md; all items at `status: not started` |
| During a run | Agents update `status:` in place; do not edit mid-run |
| After a run | Review [[progress-md|PROGRESS.md]] for blocked items; move the stop marker; update `os/projects/README.md` if a milestone was hit |
| When the project is complete | Delete or archive PLAN.md — a fully-done plan left in place will be picked up by the next run |
