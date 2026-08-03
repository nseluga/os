# MAP.md Reference

Repo-level partition into **lanes** — independently workable areas, one owner
each, one branch each. Nate writes it. Teammates read their entry and run
[[lane-md|/lane]] inside it.

One MAP.md per repo, on `main`. Skip it entirely for solo repos — write a
LANE.md and go.

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

---

## Foundation pass

Runs before any fork. Nate only — never assign it.

1. Draw the map. Run the `owns:` overlap check; fix any intersection.
2. For each `depends on:` edge, write the contract as **real code on `main`** —
   migration + schema, shared types, route contract. Not a path list.
3. Ship ≥1 fixture per shape, so a lane can test against a contract whose
   producer does not exist yet.
4. Contract compiles. Commit to `main`. These paths are now `protected:`.
5. Cut `integration` from that commit. Lane branches fork from `integration`.

---

## Amendment path

Agent hits `protected:` → stops, reports → Nate amends on `main` → lanes rebase.

Amendments are normal. A round with zero of them froze too much.

---

## Branches

```
main ───────────────────────────────────────►
  └─ integration ─────────────────────────────►
       ├─ lane/<name>  ──●──●──●──┘
       └─ lane/<name>  ─────●──●──┘   ● = one dev-team-auto item
```

- One lane = one branch = one person.
- Merge to `integration` on **every DONE item**, via `/merge-lane`.
- Rebase onto `integration` after each merge, or the lane drifts.
- Nate promotes `integration` → `main`. Lanes never touch `main`.

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
| Round start | Nate writes MAP.md; runs foundation pass; cuts `integration` |
| Lane start | Assignee runs `/lane <name>` — branch + LANE.md |
| Per item | `/dev-team-auto` → DONE → `/merge-lane` |
| Blocked on protected | Amendment: Nate edits `main`, lanes rebase |
| Round end | Promote `integration` → `main`; replace MAP.md wholesale |

MAP_PROGRESS.md is append-only across rounds — never reset.
