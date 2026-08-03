---
name: map
description: Partition a repo into parallel lanes — grills the user into a schema-valid MAP.md naming every cross-lane dependency. Use when the user says "/map", "draw the lanes", "split this repo up", "map the project", "set up lanes", or is breaking a round of work into separable pieces. Applies solo as well as across a team.
---

**Related:** [[map-md]] · [[lane-md]] · [[skills/foundation/SKILL|foundation]] · [[skills/grill-me/SKILL|grill-me]]

You partition a repo into lanes that can be built in parallel, and you name what
sits between them. Reviewer-only. Output: `MAP.md`.

`/foundation` freezes those contracts next; `/lane` plans one lane after that.

**Lane count follows the work, not the headcount.** Cut lanes where the work
separates. A team runs them at once; solo runs them one at a time — same map
either way. Never collapse a round into one long lane because one person is
building. Skip `/map` only when the round is one indivisible piece of work —
say so and point at `/lane`.

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

Read `~/os/skills/grill-me/SKILL.md` before the first question and conduct the
interview by it: one question at a time, concrete tradeoffs per option, always
recommend, walk dependencies in order, explore the codebase instead of asking
what the code already answers.

Cover, in order:

1. **Round goal** — what must exist when all lanes merge.
2. **Candidate lanes** — propose them from the scan, don't ask cold. Aim for
   vertical slices, not layers: a lane that owns a feature end-to-end
   parallelizes; a "backend lane" + "frontend lane" split serializes.
3. **`owns:` globs per lane** — draft from the scan, user corrects.
4. **`depends on:` edges** — for each, name the artifact to freeze. No name →
   push back: merge the lanes or sequence them. Do not accept a deferred
   integration. Name the artifact only; `/foundation` pins its shape next.
5. **`protected:` list** — the contracts from step 4, plus schema/migrations,
   config keys, shared design tokens. Keep short.
6. **Assignees** — who builds each lane. Match lane difficulty to skill; give
   the least experienced person the lane with the fewest `depends on:` edges.
   Solo → one name on every lane, worked in dependency order.

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

Then hand off to `/foundation`, which pins each contract's shape, writes the
plan that builds them, and cuts `integration`:

```
/foundation     freeze the contracts named by every `depends on:` edge
```

Do not write contracts, a foundation plan, or lane branches here. `/map`
partitions; `/foundation` freezes; `/lane` plans one lane.

## Update mode

1. Restate what MAP_PROGRESS.md says landed; confirm.
2. New or dropped lanes; reassignments.
3. Contract amendments — a lane hit a `protected:` path. Re-run `/foundation`
   to amend, then tell every live lane to rebase.
4. Re-run the overlap check over the full set, not just the new lanes.

Never re-litigate a merged lane.
