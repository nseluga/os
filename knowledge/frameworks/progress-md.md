# PROGRESS.md Reference

PROGRESS.md is the running ledger for an autonomous session. It tracks what
happened to each PLAN.md item — done, blocked, or not yet reached — so that a
run can be resumed, audited, and handed off without reading the full transcript.

---

## Who writes it

**`/dev-team-auto`** — writes a row the moment each item resolves (DONE or
BLOCKED), before touching the next item. The two writes (PROGRESS.md row +
team-memory entry) are treated as one atomic action.

**`/dev-team` (interactive)** — does **not** write PROGRESS.md. It reports
results to you in the conversation. PROGRESS.md is exclusively for unattended runs. It reports
results to you in the conversation. PROGRESS.md is exclusively for unattended runs.

You never hand-edit PROGRESS.md mid-run. Read it to check status; let the agent
write to it.

---

## When you need one

PROGRESS.md is created automatically by the agent on first item completion — you
do not create it yourself. It exists as long as a PLAN.md is active.

Read it when:
- Checking what an overnight run accomplished before the agent has reported back
- Deciding whether to resume a partial run (find the first non-`done` row)
- Auditing which track ran on each item (rigor is recorded per row)
- Handing a BLOCKED item to a human for diagnosis

---

## Format

A Markdown table with one row per PLAN.md item, in the same order as PLAN.md.

```markdown
# Progress

| Item | Status |
|------|--------|
| <task or page> | <status string> |
```

### The preamble (recommended)

A PROGRESS.md should open with a short preamble the agent maintains alongside
the rows — the same "lean orientation, don't duplicate" rule as PLAN.md:

- An **H1 title**.
- A one-line **what-this-is** note, including the reconciliation rule: *PLAN.md
  is the contract; this tracks where we are in it — if they disagree, PLAN.md
  wins for scope.*
- A **Current position** pointer — `Status` / `Next` / `Blockers` / `Last
  updated` — that names the resume point explicitly. dev-team-auto resumes at
  the first item not marked `done`; this pointer makes that unambiguous and
  human-auditable without reading every row.

The agent updates the Current-position pointer in the **same atomic write** as
each item's row (alongside the PROGRESS row + team-memory entry), so the pointer
never lags the rows. Then the per-item table follows as below.

### dev-team-auto row conventions

**Done:**
```
done [track] — [one-line summary of what was built] — [commit hash]
```
Example:
```
done full — rate limiting via Redis middleware on /api/submit — a3f92c1
```

**Blocked:**
```
blocked — VERDICT: FAIL — [unmet done-when criteria] — Root Cause: [hint]
```
Example:
```
blocked — VERDICT: FAIL — parameterized bulk insert not supported by ORM — Root Cause: design-level gap, no workaround found in 5 attempts
```

**Not yet reached (below stop marker or not started):**
```
not started
```
or
```
skipped — below stop marker
```

---

## Example PROGRESS.md — dev-team-auto

```markdown
# Progress

| Item | Status |
|------|--------|
| Add rate limiting to /api/submit | done full — rate limiting via Redis middleware, configurable via env vars — a3f92c1 |
| Replace inline SQL in UserRepository | done light — all UserRepository queries parameterized, injection test added — b7d04e3 |
| Add last_login_at column to users table | blocked — VERDICT: FAIL — column not populated on OAuth login path — Root Cause: OAuth callback skips the login hook where timestamp is set |
```

---

## Multiple rounds

A project outlives any one PLAN.md. When a round finishes and a new plan
replaces it, **the ledger is not reset** — the new round's table is added above
the previous one, and the Current-position pointer is rewritten to describe the
new round. Older sections stay untouched forever.

```markdown
# Project — Progress

## Current position          <- rewritten each round; describes the newest only
## v4 — the brain shell      <- newest round, one row per PLAN.md item
## v3 — the os dashboard     <- prior round, left exactly as it was
## v2 archive (stages 0–7)   <- older still
```

Name each section for the round, and note the ship date on completed ones. A
reader scanning top-to-bottom gets newest-first history; an agent resuming a run
reads only the Current position and the top section.

Do not summarize or prune old sections to save space. The per-item rows — which
track ran, what shipped, which commit — are the record that makes replacing
PLAN.md lossless.

## Relationship to [[plan-md]]

PROGRESS.md does not replace [[plan-md|PLAN.md]] — it annotates it. PLAN.md is the source
of truth for what to do; PROGRESS.md is the source of truth for what happened.

- PLAN.md `status:` field is also updated in place by the agent — it mirrors
  PROGRESS.md but is the field other agents read to find their resume point.
- If PLAN.md and PROGRESS.md disagree, trust PROGRESS.md — it was written
  after the work, not before.

---

## Lifecycle

| Phase | Action |
|---|---|
| Before a run | Does not exist yet — the agent creates it |
| During a run | Agent appends/updates rows; do not edit |
| After a run | Read to find blocked items; decide whether to requeue, split, or drop them |
| When the round is complete | Nothing. The ledger stays; the next round appends a new section above it (see "Multiple rounds") |

**PROGRESS.md is permanent and append-only.** It is never deleted, never split
into `PROGRESS-v3-done.md`, and never reset when a new [[plan-md|PLAN.md]]
replaces the old one. It is the only place the project's full history lives —
which is exactly what makes replacing PLAN.md safe.
