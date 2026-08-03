# LANE_PROGRESS.md Reference

LANE_PROGRESS.md is the running ledger for an autonomous session. It tracks what
happened to each LANE.md item — done, blocked, or not yet reached — so that a
run can be resumed, audited, and handed off without reading the full transcript.

---

## Who writes it

**`/dev-team-auto`** — writes a row the moment each item resolves (DONE or
BLOCKED), before touching the next item. The two writes (LANE_PROGRESS.md row +
team-memory entry) are treated as one atomic action.

**`/dev-team` (interactive)** — writes a row **only if the file already exists**;
it never creates one. Otherwise it reports results in the conversation.

**`/merge-lane`** — archives a lane's LANE_PROGRESS.md to `progress/<lane>.md`
on `integration`, and updates that lane's row in MAP_PROGRESS.md.

You never hand-edit LANE_PROGRESS.md mid-run. Read it to check status; let the agent
write to it.

---

## When you need one

LANE_PROGRESS.md is created automatically by the agent on first item completion — you
do not create it yourself. It exists as long as a LANE.md is active.

Read it when:
- Checking what an overnight run accomplished before the agent has reported back
- Deciding whether to resume a partial run (find the first non-`done` row)
- Auditing which track ran on each item (rigor is recorded per row)
- Handing a BLOCKED item to a human for diagnosis

---

## Format

A Markdown table with one row per LANE.md item, in the same order as LANE.md.

```markdown
# Progress

| Item | Status |
|------|--------|
| <task or page> | <status string> |
```

### The preamble (recommended)

A LANE_PROGRESS.md should open with a short preamble the agent maintains alongside
the rows — the same "lean orientation, don't duplicate" rule as LANE.md:

- An **H1 title**.
- A one-line **what-this-is** note, including the reconciliation rule: *LANE.md
  is the contract; this tracks where we are in it — if they disagree, LANE.md
  wins for scope.*
- A **Current position** pointer — `Status` / `Next` / `Blockers` / `Last
  updated` — that names the resume point explicitly. dev-team-auto resumes at
  the first item not marked `done`; this pointer makes that unambiguous and
  human-auditable without reading every row.

The agent updates the Current-position pointer in the **same atomic write** as
each item's row (alongside the PROGRESS row + team-memory entry), so the pointer
never lags the rows. Then the per-item table follows as below.

### dev-team-auto row conventions

Rows are a log for the user to read, not a technical record — plain English,
one sentence, no jargon (no track names, commit hashes, VERDICT labels).
Technical detail belongs in the commit message, not here.

**Done:**
```
done — [one plain sentence: what changed, in user-facing terms]
```
Example:
```
done — Requests to /api/submit are now rate-limited.
```

**Blocked:**
```
blocked — [one plain sentence: what's stuck and why, no internals]
```
Example:
```
blocked — Couldn't add last_login_at; it doesn't get set when someone logs in via Google.
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

## Example LANE_PROGRESS.md — dev-team-auto

```markdown
# Progress

| Item | Status |
|------|--------|
| Add rate limiting to /api/submit | done — Requests to /api/submit are now rate-limited. |
| Replace inline SQL in UserRepository | done — Database queries are safe from SQL injection. |
| Add last_login_at column to users table | blocked — Couldn't add last_login_at; it doesn't get set when someone logs in via Google. |
```

---

## Multiple rounds

A project outlives any one LANE.md. When a round finishes and a new plan
replaces it, **the ledger is not reset** — the new round's table is added above
the previous one, and the Current-position pointer is rewritten to describe the
new round. Older sections stay untouched forever.

```markdown
# Project — Progress

## Current position          <- rewritten each round; describes the newest only
## v4 — the brain shell      <- newest round, one row per LANE.md item
## v3 — the os dashboard     <- prior round, left exactly as it was
## v2 archive (stages 0–7)   <- older still
```

Name each section for the round, and note the ship date on completed ones. A
reader scanning top-to-bottom gets newest-first history; an agent resuming a run
reads only the Current position and the top section.

Do not summarize or prune old sections to save space. The per-item rows — which
track ran, what shipped, which commit — are the record that makes replacing
LANE.md lossless.

## Relationship to [[lane-md]]

LANE_PROGRESS.md does not replace [[lane-md|LANE.md]] — it annotates it. LANE.md is the source
of truth for what to do; LANE_PROGRESS.md is the source of truth for what happened.

- LANE.md `status:` field is also updated in place by the agent — it mirrors
  LANE_PROGRESS.md but is the field other agents read to find their resume point.
- **On disagreement:** LANE.md wins for **scope** (what is in this round);
  LANE_PROGRESS.md wins for **state** (what actually happened), since it was
  written after the work. These never conflict — they answer different questions.

---

## Two layers (team rounds)

When `MAP.md` exists, progress mirrors the plan layers. Nothing appends between
them — different granularities.

| | Plan | Progress | Written by | Lives on |
|---|---|---|---|---|
| Map | `MAP.md` | `MAP_PROGRESS.md` — one row per **lane** | `/merge-lane` | `integration` |
| Lane | `LANE.md` | `LANE_PROGRESS.md` — one row per **item** | `/dev-team-auto` | `lane/<name>` |

**Archive rule.** `LANE_PROGRESS.md` never merges to `integration` at root —
every lane writes that path and they would conflict on every merge.
`/merge-lane` moves it to `progress/<lane>.md`, appending if the file exists.

MAP_PROGRESS.md needs no locking: it is written only during a merge, and merges
are serialized.

Schema for MAP_PROGRESS.md is in [[map-md]].

---

## Lifecycle

| Phase | Action |
|---|---|
| Before a run | Does not exist yet — the agent creates it |
| During a run | Agent appends/updates rows; do not edit |
| After a run | Read to find blocked items; decide whether to requeue, split, or drop them |
| When the round is complete | Nothing. The ledger stays; the next round appends a new section above it (see "Multiple rounds") |

**LANE_PROGRESS.md is permanent and append-only.** It is never deleted, never split
into `PROGRESS-v3-done.md`, and never reset when a new [[lane-md|LANE.md]]
replaces the old one. It is the only place the project's full history lives —
which is exactly what makes replacing LANE.md safe.
