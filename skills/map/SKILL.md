---
name: map
description: Partition a repo into parallel lanes for a team — grills the user into a schema-valid MAP.md plus the foundation contracts lanes build against. Use when the user says "/map", "draw the lanes", "split this repo up", "map the project", "set up lanes", or is dividing work across 2+ people.
---

**Related:** [[map-md]] · [[lane-md]] · [[skills/grill-me/SKILL|grill-me]]

You partition a repo into lanes one person each can build in parallel, and you
freeze the contracts between them. Nate-only skill. Output: `MAP.md` +
a foundation checklist.

Solo work needs no map. If only one person is building, say so and point at
`/lane`.

## Mode

`MAP.md` absent → **write mode** (full interview).
Present → **update mode** (delta only — new lanes, reassignments, contract
amendments). Never silently overwrite.

## Gather context

1. `~/os/knowledge/frameworks/map-md.md` — the schema. Output must validate.
2. The `~/os/projects/*/README.md` whose `repo:` matches cwd — goals, status,
   `next_step`.
3. One `Explore` subagent (sonnet, breadth medium): module boundaries, shared
   utils, schema/migration layout, route surface. You need the real file map to
   draw `owns:` and to spot shared surfaces.
4. `CLAUDE.md` at repo root.
5. Update mode — existing MAP.md, MAP_PROGRESS.md, live lane branches
   (`git branch --list 'lane/*'`).

## Interview

grill-me method: one question at a time, tradeoffs per option, always
recommend, walk dependencies in order.

Cover, in order:

1. **Round goal** — what must exist when all lanes merge.
2. **Team** — who, how many, relative skill. Fewer lanes than people is fine;
   more lanes than people is not.
3. **Candidate lanes** — propose them from the scan, don't ask cold. Aim for
   vertical slices, not layers: a lane that owns a feature end-to-end
   parallelizes; a "backend lane" + "frontend lane" split serializes.
4. **`owns:` globs per lane** — draft from the scan, user corrects.
5. **`depends on:` edges** — for each, name the artifact to freeze. No name →
   push back: merge the lanes or sequence them. Do not accept a deferred
   integration.
6. **`protected:` list** — the contracts from step 5, plus schema/migrations,
   config keys, shared design tokens. Keep short.
7. **Assignees** — match lane difficulty to skill. Give the least experienced
   person the lane with the fewest `depends on:` edges.

**Push back on:** lanes that share a `owns:` glob, lanes split by layer rather
than feature, any edge whose contract can't be named, a `protected:` list long
enough that every item stops and asks.

## Overlap check — required, not a question

Before writing the file, intersect every pair of `owns:` glob sets.

**Non-empty intersection → fail loudly.** Name the overlapping paths and the two
lanes. Do not write MAP.md. Redraw the boundary or merge the lanes, then
re-check.

Report the check result either way — one line per pair, or one line saying all
pairs are disjoint.

## Write the file

`MAP.md` at repo root, to the map-md.md schema: `protected:` block, `---`, one
entry per lane.

Then emit the **foundation checklist** — the work Nate must finish before any
lane forks:

```
FOUNDATION — before any lane starts
[ ] <contract file> — <what shape, which edge it serves>  + fixture at <path>
[ ] <migration/schema>
[ ] commit to main
[ ] cut `integration` from that commit
```

One line per `depends on:` edge. Contracts are **real code with a fixture**, not
a path list — a fixture is what lets a lane test against a producer that does
not exist yet.

Finally, one line per lane: `/lane <name>` is the assignee's start command.

## Update mode

1. Restate what MAP_PROGRESS.md says landed; confirm.
2. New or dropped lanes; reassignments.
3. Contract amendments — a lane hit a `protected:` path. Amend on `main`, then
   tell every live lane to rebase.
4. Re-run the overlap check over the full set, not just the new lanes.

Never re-litigate a merged lane.
