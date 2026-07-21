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

**`flag:`** (optional) — marks the item for maximum scrutiny. Values: `security`,
`money`, `data-path`. Triggers: Opus model on the engineer + fixer + reviewer,
design exploration (2–3 parallel architects before the first build), and the
`tests+behavioral` gate including a live smoke pass. Use for auth, payments,
migrations, or anything where a mistake is hard to reverse.

---

## Format — layout-loop runs

Layout-loop plans describe visual pages to improve, not code tasks. The queue
is ordered; each page gets its own full visual loop.

Plan-level metadata goes at the top (applies to the whole run):

```markdown
brand: portfolio
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

**`brand:`** (required, plan-level) — the brand file to load from
`~/os/knowledge/library/design-language/brands/<brand>.md`. Must match an
existing file. Never guess for client work; confirm before the run.

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
`brand:`/`launch:`/`url:` metadata or first `- page:` for layout-loop) is an
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

---

## Example PLAN.md — dev-team

```markdown
- task: Add rate limiting to /api/submit
  done when:
    - Requests beyond 10/min from the same IP receive a 429 response with Retry-After header
    - The rate limit window and max requests are configurable via environment variables
    - Existing passing tests remain passing
  status: not started
  flag: security

- task: Replace inline SQL in UserRepository with parameterized queries
  done when:
    - No raw string interpolation remains in UserRepository
    - A test covers a value that would have triggered injection if unparameterized
    - All existing UserRepository tests pass
  status: not started

> **⚠️ AUTONOMOUS RUN — STOP HERE**

- task: Add last_login_at column to users table
  done when:
    - Migration runs without error on dev DB
    - Column is populated on every successful login
    - Rolling back the migration restores the prior schema
  status: not started
  flag: data-path
```

## Example PLAN.md — layout-loop

```markdown
brand: portfolio
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
| After a run | Review PROGRESS.md for blocked items; move the stop marker; update `os/projects/README.md` if a milestone was hit |
| When the project is complete | Delete or archive PLAN.md — a fully-done plan left in place will be picked up by the next run |
