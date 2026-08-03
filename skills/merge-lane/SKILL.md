---
name: merge-lane
description: Merge a completed lane item into the integration branch — overlap check, merge, archive lane progress, harvest team memory, full suite, update MAP_PROGRESS. Use when the user says "/merge-lane", "merge this lane", "land the lane", or after /dev-team-auto reports DONE on a lane branch.
---

**Related:** [[map-md]] · [[lane-md]] · [[progress-md]]

Nate-only. Runs the five steps that make the collision nets fire. Skipping any
of them is how two green lanes ship a broken combination.

Lane name from arg; if absent, infer from the current branch (`lane/<name>`).

## 0. Preflight

- On `lane/<name>`, working tree clean, at least one item `done` in
  LANE_PROGRESS.md. Otherwise stop.
- `integration` exists. If not, the foundation pass never ran — stop and say so.

## 1. Overlap check

```
git diff --name-only integration...lane/<name>
```

Do the same for every other live lane branch (`git branch --list 'lane/*'`).
Intersect this lane's file list against each.

- Intersection inside `protected:` → **stop.** A lane edited a protected path.
  Escalate as an amendment; do not merge.
- Intersection outside `protected:` → **report the paths and the other lane**,
  then continue. This is the case git stays quiet about when the edits
  auto-merge cleanly.
- Empty → say so in one line.

## 2. Merge

```
git checkout integration && git merge lane/<name> --no-edit
```

Conflict → the lanes were not disjoint. Resolve, then note the overlapping
paths in the merge report so the next round's map fixes the boundary.

## 3. Archive lane progress

Move the lane's `LANE_PROGRESS.md` to `progress/<lane>.md` on `integration`.
Append to it if the file already exists — never overwrite a prior merge's rows.

`LANE_PROGRESS.md` does not survive at root on `integration`. Only
`progress/<lane>.md` does.

## 4. Harvest team memory

Lanes do not write `.claude/dev-team/team-memory.md`. Take the entries the lane
returned and append them here, in merge order, to the canonical file on
`integration`.

Entry format per `~/os/skills/dev-team/convergence-loop.md`.

## 5. Full suite + rollup

Run the repo's full test suite on `integration`.

- **Fail** → this is cross-lane breakage; each lane passed alone. Report which
  lanes are implicated (from step 1's file lists) and stop. Do not update
  MAP_PROGRESS to green.
- **Pass** → update this lane's row in `MAP_PROGRESS.md`: items done, last
  commit, status.

Commit `integration`.

## 6. Report

Five lines:

```
overlap:  <none | paths + other lane>
merge:    <clean | conflicts resolved in N files>
archived: progress/<lane>.md (+N rows)
memory:   N entries appended
suite:    <PASS | FAIL — what broke>
```

Then remind the assignee: **rebase onto `integration`** before the next item, or
the lane drifts.

Do not promote `integration` → `main`. That is a separate, deliberate call.
