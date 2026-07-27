# PLAN.md Reference

A PLAN.md is the pre-run contract for any autonomous or semi-autonomous session.
It defines **what to build** (or improve), in what order, and exactly how to
know each item is done. Agents read it at startup; you write it before the session.

---

## When you need one

Use PLAN.md when:
- Running `/dev-team-auto` (it requires one — the outer loop iterates over it)
- Running `/dev-team` on a multi-item backlog (it reads PLAN.md if no inline arg is given)
- Running `/layout-loop` with more than one page, or when you want the queue
  to persist across sessions
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
  status: not started
  track: full
  flag: security
```

### Fields

**`task:`** (required) — one imperative sentence scoped to one logical change.
If you can't describe it in one sentence, split the item.

**`done when:`** (required) — the acceptance criteria QA converts to tests and
uses as its binary gate. See "Writing good criteria" below.

**`status:`** (required, start at `not started`) — the agent updates this in
place as items resolve. Values: `not started` | `in progress` | `done` | `blocked`.
Do not change this manually mid-run.

**`track:`** (required) — the rigor level for this item:
- `trivial` — copy/text/config/comments only; no logic. Build check, no QA.
- `light` — one file/function, no schema/API/auth/money touch. QA, no review.
- `full` — everything else; multi-file; new endpoints/schema/auth/money. Full loop.
When between tracks, choose the heavier one.

**`flag:`** (optional) — marks the item for elevated scrutiny. Values: `security`,
`money`, `data-path`. Triggers: Opus model on the engineer + fixer + reviewer,
design exploration (2–3 parallel architects before the first build), and the
`tests+behavioral` gate including a live smoke pass. Use for auth, payments,
migrations, or anything where a mistake is hard to reverse.

**`critical:`** (optional) — marks the item for maximum scrutiny, one tier above
`flag:`. Values: `security`, `reliability`, or any description. Triggers: **Fable
at medium effort** on the engineer + fixer + reviewer, and design exploration with
Fable architects. Use when a defect would be catastrophic or irreversible: auth
systems, cryptography, authorization, PII/PHI handling, financial transactions,
production data integrity. Composes with any track above `trivial`.

**`research:`** (optional) — a topic `dt-research` investigates before the first
build (e.g. `research: astro auth patterns`). Use when the item hinges on
choosing a current external tool, library, or hosted service — the knowledge
training data gets wrong. `flag:`/`critical:` items get a research pass
automatically when they involve an external tool choice; this field is the
manual trigger for everything else. Cache-first
(`~/.claude/skills/dev-team/research-notes/`), so repeat topics are near-free.

**`parallel-group:`** (optional) — consecutive items sharing the same value run
concurrently under `/dev-team-auto` (up to 3 at once, each in its own worktree
branch, merged in completion order). Set it only when the items are file- and
resource-disjoint: no shared files, no shared schema/migration, no
producer/consumer relationship between them. Never infer independence at
run-time — this field is the only signal `/dev-team-auto` trusts. The plan
author (or plan-md's own scan of the codebase) sets it when writing the plan,
not the executing agent.

---

## Format — layout-loop runs

Layout-loop plans describe visual pages to improve, not code tasks. The queue
is ordered; each page gets its own full visual loop.

Plan-level metadata goes at the top (applies to the whole run):

```markdown
launch: pnpm dev
url: http://localhost:3000
```

Items follow:

```markdown
- page: /
  notes: hero section feels cluttered — prioritize whitespace pass

- page: /projects
  notes: card grid — check spacing rhythm and image crop consistency
```

### Fields

**`launch:`** (required, plan-level) — the dev-server command
(e.g. `pnpm dev`, `pnpm --filter web dev`).

**`url:`** (required, plan-level) — the base URL to open in the browser
(e.g. `http://localhost:3000`).

**`page:`** (required per item) — the route path to view and improve.
Each page gets its own 5-pass loop.

**`notes:`** (optional per item) — hints about where to focus. Not instructions;
the agent still applies the full rubric. Think of it as "look here first."

**`status:`** (same as dev-team) — `not started` | `done` | `blocked`.
Layout-loop updates this in place.

---

## The preamble (context above the items)

Everything above the first item block (`- task:` for dev-team, the plan-level
`launch:`/`url:` metadata or first `- page:` for layout-loop) is an
optional **preamble**: orientation the orchestrator reads for global guidance
but does not execute as an item. Recommended by default for every file-based
PLAN.md; the only thing that varies is depth. Skip it only for a throwaway
inline/TASK.md task.

The loop reads top-to-bottom and is LLM-driven, so a clearly-separated preamble
is safe — but keep the items unambiguous: start each with the exact `- task:` /
`- page:` block format, and never put an executable item inside the preamble.
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

Works the same in both dev-team and layout-loop plans.

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

**Speed + reliability criteria (standard for `full` items):** functionality
criteria alone let slow or fragile code pass QA. Every `full`-track item also
carries:

- One **speed** criterion: a measured number against seeded data — "median of
  5 runs of <the operation> stays under <threshold> with <N> rows seeded."
  Defaults when you have no better number: API route < 200ms, full page render
  < 1s, background job < 30s. Set thresholds at ~2× the real target — the
  criterion exists to catch regressions (an unindexed scan, an N+1 loop), not
  to benchmark the laptop — and always name the seed size; a timing against an
  empty DB proves nothing.
- One **reliability** criterion matching the item's likeliest failure mode:
  double-submit/retry creates no duplicate row; a down dependency degrades to
  a defined fallback within a timeout instead of hanging; behavior holds under
  both `TZ=UTC` and a non-UTC TZ; invalid input at the boundary returns the
  defined error, not a 500.

Waive either with one visible line in the item — `speed: N/A — <reason>` —
never silently; a written waiver is something the Reviewer can challenge.
`light` items take the reliability criterion when they touch a system entry
point; `trivial` items are exempt. QA verifies speed criteria by measurement
(running the timed test), never by inspection.

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
- **Right-size `track:`.** Defaulting everything to `full` wastes the loop on
  copy edits; defaulting to `light` under-gates schema changes. Classify each
  item; when torn, go heavier.
- **Escalate per item, not per run.** `flag:`, `critical:`, and `research:` buy
  targeted scrutiny exactly where the stakes or staleness risk live — cheaper
  than raising the whole run's model tier.
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
  status: not started
  track: full
  flag: security

- task: Rewrite session token signing to use HMAC-SHA256
  done when:
    - All tokens are signed with HMAC-SHA256 using a server-side secret
    - A token with a tampered payload fails verification and returns 401
    - Existing sessions are invalidated on deploy (no legacy unsigned tokens accepted)
  speed: N/A — in-memory signing, no data-size dependence
  status: not started
  track: full
  critical: security

- task: Replace inline SQL in UserRepository with parameterized queries
  done when:
    - No raw string interpolation remains in UserRepository
    - A test covers a value that would have triggered injection if unparameterized
    - Median of 5 runs, findByEmail stays under 50ms with 100k users seeded (parameterization didn't lose the index)
    - All existing UserRepository tests pass
  status: not started
  track: full
  parallel-group: a

- task: Add a /health endpoint returning build SHA and uptime
  done when:
    - GET /health returns 200 with { sha, uptimeSeconds } when the app is up
    - Returns 503 while a dependency the app requires (DB) is unreachable
  status: not started
  track: light
  parallel-group: a

> **⚠️ AUTONOMOUS RUN — STOP HERE**

- task: Add last_login_at column to users table
  done when:
    - Migration runs without error on dev DB
    - Column is populated on every successful login, and a retried login write does not error or duplicate
    - Rolling back the migration restores the prior schema
  speed: N/A — single-column write on an existing indexed path
  status: not started
  track: full
  flag: data-path
```

## Example PLAN.md — layout-loop

```markdown
launch: pnpm dev
url: http://localhost:3000

- page: /
  notes: hero feels heavy — whitespace and type hierarchy first
  status: not started

- page: /projects
  status: not started

> **⚠️ AUTONOMOUS RUN — STOP HERE**

- page: /about
  status: not started
```

---

## Lifecycle

| Phase | Action |
|---|---|
| Before a session | Author PLAN.md; all items at `status: not started` |
| During a run | Agents update `status:` in place; do not edit mid-run |
| After a run | Review [[progress-md|PROGRESS.md]] for blocked items; move the stop marker; update `os/projects/README.md` if a milestone was hit |
| When the project is complete | Delete or archive PLAN.md — a fully-done plan left in place will be picked up by the next run |
