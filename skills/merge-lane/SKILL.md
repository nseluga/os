---
name: merge-lane
description: Review a lane's open PR and land it on the integration branch — overlap check, merge, archive lane progress, harvest team memory, full suite, update MAP_PROGRESS. Reviewer-only. Use when the user says "/merge-lane", "review the lane", "land the lane PR", "merge this lane", or sits down to review teammates' work.
---

**Related:** [[map-md]] · [[lane-md]] · [[progress-md]]

Reviewer-only. Runs the steps that make the collision nets fire. Skipping any of
them is how two green lanes ship a broken combination.

**Cadence: per review session, not per item.** One PR per lane stays open while
the assignee works. Review everything in it and merge when convenient; a fresh
PR opens for whatever lands after. Assignees are never blocked — they keep
committing to their lane branch while the PR sits.

Lane name from arg; if absent, list open PRs targeting `integration` and ask.

## 0. Preflight

- `gh auth status` clean.
- `integration` exists. If not, the foundation pass never ran — stop and say so.
- `gh pr list --base integration` → pick the lane's PR.
- `gh pr checkout <n>` — their exact tree, locally.
- At least one item marked `done` in `LANE_PROGRESS.md`. Otherwise stop.

## 1. Review

The step the PR flow exists for. Do it before merging, not after.

- `gh pr diff <n>` for the whole change. The commit list is one commit per item —
  review item by item.
- `LANE_PROGRESS.md` — what each item claims, and any blocked item's root cause.
- CI status. Red → do not merge; comment and stop.

Leave findings as PR comments. Anything needing a `protected:` change is an
amendment: fix it on `main` yourself, then tell live lanes to rebase.

## 2. Overlap check

```
git diff --name-only integration...<lane-branch>
```

Same for every other live lane (`git branch -r --list 'origin/lane/*'`).
Intersect this lane's file list against each.

- Intersection inside `protected:` → **stop.** Escalate as an amendment; do not merge.
- Intersection outside `protected:` → **report the paths and the other lane**, then
  continue. This is the case git stays quiet about when the edits auto-merge cleanly.
- Empty → say so in one line.

## 3. Merge

```
gh pr merge <n> --merge
```

`--merge`, never squash or rebase — the per-item commits are the record
`progress/<lane>.md` and team-memory refer to.

Conflict → the lanes were not disjoint. Resolve, then note the overlapping paths
in the report so the next round's map fixes that boundary.

## 4. Archive lane progress

On `integration`, move the lane's `LANE_PROGRESS.md` to `progress/<lane>.md`.
Append if it already exists — never overwrite a prior session's rows.

`LANE_PROGRESS.md` does not survive at root on `integration`. Only
`progress/<lane>.md` does.

## 5. Harvest team memory

Lanes do not write `.claude/dev-team/team-memory.md`. Take the entries the lane
returned (run summaries / PR body) and append them to the canonical file on
`integration`, in merge order.

Entry format per `~/os/skills/dev-team/convergence-loop.md`.

## 6. Full suite + rollup

Run the repo's full test suite on `integration`.

- **Fail** → cross-lane breakage; each lane passed alone. Name the implicated
  lanes (from step 2's file lists) and stop. Do not mark MAP_PROGRESS green.
- **Pass** → update this lane's row in `MAP_PROGRESS.md`: items done, last
  commit, status.

Commit and push `integration`.

## 7. Report

```
reviewed: N items, N commits
overlap:  <none | paths + other lane>
merge:    <clean | conflicts resolved in N files>
archived: progress/<lane>.md (+N rows)
memory:   N entries appended
suite:    <PASS | FAIL — what broke>
```

Then tell the assignee: **rebase onto `integration`**, and open a fresh PR for
anything done since.

Do not promote `integration` → `main`. Separate, deliberate call.
