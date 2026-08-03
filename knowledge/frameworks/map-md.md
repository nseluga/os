# MAP.md Reference

Repo-level partition into **lanes** — independently workable areas, one owner
each, one branch each. The Reviewer writes it. Assignees read their entry and run
[[lane-md|/lane]] inside it.

One MAP.md per repo, on `main`. Lane count follows the work, not the headcount —
a solo builder maps the same lanes and works them one at a time. Skip it only
when the round is one indivisible piece of work; write a LANE.md and go.

**Related:** [[lane-md]] annotates one lane · [[progress-md]] tracks both layers.

---

## Format

```markdown
# <Project> — Lane Map

protected:
  - <path or glob>
  - <path or glob>

---

- lane: <short name>
  area: <one line — what this lane covers>
  owns: [ <glob>, <glob> ]
  assignee: <name>
  depends on: <lane> (<what it reads>) | —
```

### `protected:`

Surfaces where a unilateral change breaks another lane **silently**. The only
hard fence at run time.

Include: DB schema + migrations, shared types, API route contracts, config key
names, shared design tokens. Keep it short — every entry is a stop-and-ask.

Agents hitting one **stop and report**. They do not edit it and do not stub
around it.

### `owns:`

Globs, **checked at authoring time only**. Nothing reads them during a run.

Run the overlap check when writing the map: intersect every pair. **Non-empty
intersection → the split is wrong.** Redraw the boundary or merge the two lanes.
Do not ship an overlapping map.

### `depends on:`

Every edge names a frozen artifact, or the lanes are not two lanes:

| Edge | Freeze |
|---|---|
| B reads data A writes | the type + table/migration |
| B calls something A builds | signature or route + error cases |
| both read the same config | the key names |
| neither | nothing |

**Can't name the artifact → it is an unresolved design question.** Merge the two
lanes, or sequence them.

Two forms — they are not interchangeable:

```markdown
depends on: ingest (Lead rows — contract lib/types.ts)   # parallel, frozen
depends on: enrich (sequenced — starts after enrich merges)
```

**Parallel** — the shape is frozen and fixtured; both lanes run at once.
**Sequenced** — the shape isn't pinnable, so there is nothing to build against.
`/lane` refuses to start a sequenced lane until its predecessor's
MAP_PROGRESS.md row reads merged.

`/foundation` decides which. `/map` writes the parallel form by default;
`/foundation` rewrites the edge to sequenced when the interview can't pin the
shape — and that rewrite lands in MAP.md, not just in the conversation.

---

## Foundation pass

Runs before any fork. Reviewer only — never assign it.

1. Draw the map. Run the `owns:` overlap check; fix any intersection.
2. `/foundation` pins every contract's **actual shape** — fields, types,
   nullability, columns, status codes. Can't pin it → sequence those lanes
   instead of freezing a guess.
3. `/foundation` writes those as items in **`FOUNDATION.md` on `main`** — not
   `LANE.md`, which belongs only on lane branches. Each item's `done when:`
   states the shape verbatim and requires **≥1 fixture that validates against
   it**.
4. `/foundation` builds them **inline in the same session**, item by item, and
   shows you each diff. Transcription, not design — the shapes were pinned in
   step 2, so the convergence loop buys nothing. One item escalates to
   `/dev-team` when it needs a backfill over existing rows, touches an
   unfamiliar subsystem, or fails typecheck twice.
5. Same run verifies each fixture validates, sets `protected:` in MAP.md,
   commits `main`, and cuts `integration`.
6. Lane branches fork from `integration`.

The agent transcribes a shape you decided; it never designs one. That is the
whole reason step 2 is an interview and not a delegation.

---

## Amendment path

Agent hits `protected:` → stops, reports → Reviewer amends on `main` → lanes rebase.

Amendments are normal. A round with zero of them froze too much.

---

## Branches

```
main ───────────────────────────────────────►
  └─ integration ─────────────────────────────►
       ├─ lane/<name>  ──●──●──●──┘ PR
       └─ lane/<name>  ─────●──●──┘ PR

  ● = one item (QA PASS + clean review), pushed as it lands
  PR = one open PR per lane; Reviewer merges it per review session
```

- One lane = one branch = one owner. One person may own several lanes; they
  still get separate branches and PRs, merged in dependency order.
- **Assignee:** push after each item; keep **one PR open** into `integration`
  (`/ship`). Never blocked — keep committing while the PR sits.
- **Reviewer:** review and merge that PR **per review session, not per item**
  (`/merge-lane`). A fresh PR opens for work done since.
- Rebase onto `integration` after each merge, or the lane drifts.
- Reviewer promotes `integration` → `main`. Lanes never touch `main`.

Branch protection: require PR review on `main` and `integration`.

---

## MAP_PROGRESS.md

Lives on `integration`. One row per lane. **Written only during a merge** — no
locking needed, merges are serialized.

```markdown
# <Project> — Lane Progress

| Lane | Assignee | Branch | Status |
|------|----------|--------|--------|
| ingest | intern-a | lane/ingest | 3/5 items — last merge a3f92c1 |
| enrich | intern-b | lane/enrich | blocked — vendor API returns no confidence field |
| digest | nate | lane/digest | done — merged 2026-08-04 |
```

Detail lives in `progress/<lane>.md` (archived per merge). This file stays one
line per lane.

---

## Example

```markdown
# LeadPulse — Lane Map

protected:
  - db/schema.sql
  - db/migrations/**
  - lib/types.ts
  - .env.example

---

- lane: ingest
  area: Pull new sheet rows into the DB on a schedule.
  owns: [ src/ingest/**, src/cron/**, tests/ingest/** ]
  assignee: intern-a
  depends on: —

- lane: enrich
  area: Call the enrichment API per lead, retry + rate-limit.
  owns: [ src/enrich/**, tests/enrich/** ]
  assignee: intern-b
  depends on: ingest — Lead rows (lib/types.ts:Lead, fixtures/lead.json)

- lane: dashboard
  area: Web view of runs + failed leads.
  owns: [ src/web/**, tests/web/** ]
  assignee: nate
  depends on: —
```

---

## Lifecycle

| Phase | Action |
|---|---|
| Round start | `/map` → `/foundation` → `/dev-team-auto` → `/foundation` (lock) |
| Lane start | Assignee runs `/lane <name>` — branch + LANE.md |
| Per item | `/dev-team-auto` (or `/dev-team`) → DONE → push, PR open |
| Per review session | Reviewer runs `/merge-lane` on the lane's PR |
| Blocked on protected | Amendment: re-run `/foundation`, lanes rebase |
| Round end | Promote `integration` → `main`; replace MAP.md wholesale |

MAP_PROGRESS.md is append-only across rounds — never reset.
