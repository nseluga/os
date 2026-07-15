# PROGRESS.md Reference

PROGRESS.md is the running ledger for an autonomous session. It tracks what
happened to each PLAN.md item — done, blocked, or not yet reached — so that a
run can be resumed, audited, and handed off without reading the full transcript.

---

## Who writes it

**`/dev-team-auto`** — writes a row the moment each item resolves (DONE or
BLOCKED), before touching the next item. The two writes (PROGRESS.md row +
team-memory entry) are treated as one atomic action.

**`/layout-loop`** — writes a row after each page's loop ends, same discipline.

**`/dev-team` (interactive)** — does **not** write PROGRESS.md. It reports
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

### layout-loop row conventions

**Done — converged:**
```
done — converged — [one-line summary of main changes]
```

**Done — diminishing returns:**
```
done — diminishing returns — [what was achieved; what remains]
```

**Done — iteration cap (5 passes):**
```
done — cap reached — [what was achieved; what still needs work]
```

**Blocked — graceful failure:**
```
blocked — graceful failure — [reason: dev server died / screenshots failed]
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

## Example PROGRESS.md — layout-loop

```markdown
# Progress

| Page | Status |
|------|--------|
| / | done — converged — tightened hero whitespace, reduced type scale on subtitle, aligned CTA to grid |
| /projects | done — diminishing returns — card spacing normalized; image crop inconsistency remains (requires content change, out of edit fence) |
| /about | not started |
```

---

## Relationship to PLAN.md

PROGRESS.md does not replace PLAN.md — it annotates it. PLAN.md is the source
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
| When the project is complete | Delete alongside PLAN.md — no reason to keep a fully-resolved ledger in the repo |
