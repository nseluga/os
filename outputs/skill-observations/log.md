# Skill Observation Log

Observations captured during task-oriented work.

**Status key:** OPEN = not yet actioned | ACTIONED (YYYY-MM-DD) = skill updated/created | DECLINED (YYYY-MM-DD) = user decided not to pursue — resolved statuses always carry their resolution date

---

## 2026-07-24

### Observation 1: dev-team-auto needs an environment preflight before spawning agents

**Status:** ACTIONED (2026-08-08)
**Date:** 2026-07-24
**Session context:** dev-team-auto pass-3 run on a client repo
**Skill:** dev-team-auto
**Type:** open-source
**Phase/Area:** Start Up section

**Issue:** Before the first agent spawned, the session hit two environment blockers that would have burned agent attempts as phantom QA failures: (1) a pnpm upgrade made the repo's pnpm-workspace.yaml invalid (install failed repo-wide), and (2) a stale next-server from a prior automated session was squatting on the test port, so live-smoke tests polled the wrong server/DB and failed reproducibly. A manual baseline run (install + build + full suite) caught both; team-memory's recorded flake note would otherwise have misattributed the failures.

**Suggested improvement:** Add an explicit preflight step to dev-team-auto Start Up: install deps, build, run the full suite against the recorded baseline, and check test ports for stale listeners — resolve any mismatch BEFORE item 1. Record the verified baseline in the first orchestrator prompt.

**Principle:** An unattended multi-agent run should verify the recorded environment baseline itself before delegating; agents inherit environment breakage as false test failures and burn attempts on it.

### Observation 2: Worktree-based runs must sync uncommitted tracker edits from the launch checkout

**Status:** ACTIONED (2026-08-08)
**Date:** 2026-07-24
**Session context:** dev-team-auto pass-3; session isolated into a fresh git worktree
**Skill:** dev-team-auto
**Type:** open-source
**Phase/Area:** Start Up / worktree creation

**Issue:** The run read PLAN.md from the launch checkout (which had the user's latest UNCOMMITTED plan edits), but the session worktree was created from the last commit — so the worktree's PLAN.md silently lacked acceptance criteria the user had added. Item prompts were correct only because they quoted the launch-checkout read; a later status edit failed to match and exposed the drift mid-run.

**Suggested improvement:** In dev-team-auto Start Up, when entering/creating a worktree, copy (or diff-check) PLAN.md and PROGRESS.md from the launch checkout's working tree into the worktree before item 1, and commit them as the run's contract.

**Principle:** A run that branches from a commit but plans from a working tree has two sources of truth; snapshot the working-tree contract into the branch at startup.

### Observation 3: Autonomous-run memory carries a "known failures" allowance that outlives the failures

**Status:** ACTIONED (2026-08-08)
**Date:** 2026-07-27
**Session context:** /dev-team-auto on project-dashboard; fixed 7 rotting tests, then had to correct team-memory.md before spawning any agent
**Skill:** dev-team-auto (and convergence-loop.md → "Run memory log")
**Type:** open-source
**Phase/Area:** Start Up — reading team-memory.md / Standing notes

**Issue:** `team-memory.md` Standing notes recorded a baseline of "511 pass / 5 fail — pre-existing data drift, do not chase them; do not count them against an item's criterion" plus a deliberately-deferred live bug. The session's first act was to fix both. Had the run spawned agents without correcting the file, every agent would have read a standing instruction to disregard up to 5 failures that no longer existed — converting the allowance into cover for real regressions. The skill's Start Up step says to read team-memory and to compact it when oversized, but nothing prompts the orchestrator to reconcile it against the CURRENT measured state before injecting it into agents.

**Suggested improvement:** In `dev-team-auto` Start Up (and convergence-loop.md → "Run memory log"), add a reconcile step after reading team-memory: re-measure the baseline (run the gate command) and, where the file's recorded baseline or known-bug notes disagree with what you just measured, correct the file BEFORE the first spawn. Specifically flag that "N pre-existing failures — do not chase" allowances and "deliberately deferred bug" notes are the entries most likely to be stale, and that a stale allowance is worse than no allowance because it instructs agents to ignore genuine regressions.

**Principle:** Persisted agent memory that encodes a tolerance ("ignore these N failures") is a standing instruction, not a fact, and it silently outlives the condition that justified it. Any memory that grants permission to disregard a signal must be re-verified against live measurement at the moment it is loaded — expiring tolerances is the reader's job, because the writer cannot know when they stop being true.

## 2026-07-25

### Observation 4: dev-team-auto has no baseline-capture step before the first item

**Status:** ACTIONED (2026-08-08)
**Date:** 2026-07-25
**Session context:** /dev-team-auto run over project-dashboard PLAN.md v3
**Skill:** dev-team-auto (and dev-team/convergence-loop.md)
**Type:** open-source
**Phase/Area:** Start Up

**Issue:** The Start Up section reads PLAN.md, PROGRESS.md, engineer-report.md and team-memory.md, but never runs the test suite before the first item. In this run the repo had 34 failing tests on a clean checkout — 32 because behavioral tests need a server on a port nothing was listening on, and 5 from data drift (tests assert a 6-project fixture against a live tree that now has 12). Every item's `done when:` includes "existing passing tests remain passing", which is unverifiable without knowing what was passing. Without a baseline the first QA agent either wastes attempts chasing pre-existing failures or, worse, "fixes" them by editing assertions to match current reality — silently deleting real coverage.

**Suggested improvement:** Add a Start Up step: run the project's test command once before the first item, record pass/fail counts and the exact names of pre-existing failures, and pass that baseline verbatim into every item orchestrator prompt with an explicit "these are not regressions and must not be 'fixed' by editing assertions" instruction. Persist it in team-memory.md as a Standing note so a resumed run inherits it.

**Principle:** An autonomous run that gates on "existing tests still pass" must measure what passes before it changes anything. An unmeasured baseline turns every pre-existing failure into either a false blocker or an invitation to weaken the test suite.

### Observation 5: dev-team-auto assumes the test command in package.json is the real gate

**Status:** ACTIONED (2026-08-08)
**Date:** 2026-07-25
**Session context:** /dev-team-auto run over project-dashboard PLAN.md v3
**Skill:** dev-team-auto / dev-team convergence-loop.md
**Type:** open-source
**Phase/Area:** Start Up / gate mode

**Issue:** This repo's `npm test` script was stale — `node --test tests/*.test.mjs`, matching exactly one scaffold file — while the actual 338-test suite runs under `npx vitest run`. An agent trusting `npm test` would see a green gate covering ~2% of the suite and mark items DONE on essentially no evidence. The stale script was left behind when the project migrated test runners and nothing forced it to be updated.

**Suggested improvement:** In Start Up, cross-check the declared test script against what the repo actually contains (test file extensions/count vs. what the script globs) and record the verified command in team-memory Standing notes. A one-line sanity check — does the reported test count look like the number of test files on disk — catches this.

**Principle:** A green gate is only evidence if you verified the gate runs the whole suite. Trusting a declared test command without checking its coverage lets a migration leftover silently disable the quality gate for an entire autonomous run.

### Observation 6: Grep-shaped acceptance criteria can be satisfied while missing the actual duplication

**Status:** ACTIONED (2026-08-08)
**Date:** 2026-07-25
**Session context:** /dev-team-auto item 2 — dedupe expandTilde into src/lib/paths.ts
**Skill:** plan-md (criteria authoring) / dev-team convergence-loop.md
**Type:** open-source
**Phase/Area:** `done when:` criteria design

**Issue:** The item's criterion was `grep -r "function expandTilde" src/` returns exactly one definition. The plan named three known copies; the Engineer found six — three declared with that exact signature and three inlined with different shapes that the grep pattern would never have matched. Satisfying the literal criterion would have left half the duplication in place while the gate reported success.

**Suggested improvement:** When a `done when:` criterion is a grep/count assertion, treat it as a floor, not a definition of done — instruct the builder to find instances by behaviour (what the code does) and then confirm the grep, rather than searching for the grep pattern itself. Worth a line in plan-md about phrasing dedupe criteria semantically, and a line in the convergence loop telling builders to widen mechanically-phrased criteria.

**Principle:** A mechanically checkable criterion tests the check, not the intent. When the criterion is a pattern match, the agent must search for the concept and use the pattern only to confirm — otherwise the measure becomes the target.

## 2026-07-26

### Observation 7: A defect family that recurs across items is a standards-file signal, not just a per-item fix

**Status:** ACTIONED (2026-08-08)
**Date:** 2026-07-26
**Session context:** /dev-team-auto run over project-dashboard PLAN.md v3, items 3-5
**Skill:** dev-team-auto / dev-team convergence-loop.md
**Type:** open-source
**Phase/Area:** Run memory log / outer loop

**Issue:** The same defect shape — a lister and an access guard applying different filtering rules, so files excluded from the listing stayed fetchable by direct request — was caught by review on three consecutive items, each time in a different module, each time fixed locally. The third instance was a Critical that exposed ~1000 hidden files. Each item orchestrator saw only its own item, so each rediscovered the family from scratch at full review cost. The eventual fix (one shared predicate consumed by both the lister and the guard, so the two are consistent by construction) was available after the first occurrence.

**Suggested improvement:** Give the outer loop an explicit step: when an item's returned outcome names a defect family already recorded in team-memory from an earlier item this run, inject that family as a named "Known failure modes — avoid these" bullet into the NEXT item's spawn prompt, and promote it to the project's standards file rather than leaving it as a per-item lesson. The convergence loop already has an "inject relevant learnings" rule for the global learnings file — it needs the same reflex for learnings generated *within the current run*.

**Principle:** In a sequential autonomous run, each item's discovered defect family is free intelligence for every later item — but only if the outer loop actively forwards it. Per-item agents have no shared memory, so cross-item pattern recognition is the orchestrator's job, and a family caught three times should become a structural invariant rather than three local patches.

### Observation 8: Probing the live environment before spawning invalidates false premises in the plan text

**Status:** DECLINED (2026-08-08)
**Date:** 2026-07-26
**Session context:** /dev-team-auto run over project-dashboard PLAN.md v3, item 4
**Skill:** dev-team-auto / plan-md
**Type:** open-source
**Phase/Area:** item spawn / `done when:` criteria

**Issue:** Item 4's criteria assumed facts about the real data that were wrong. One criterion required a warning row for a project whose `repo:` path doesn't exist on disk — but every path resolved, so the criterion was not live-reproducible and needed a fixture to test at all. Separately, a chunk of the source folders named their file in different letter case than the criteria implied, which a case-insensitive filesystem hid from a direct read but which an exact-match directory scan would have silently dropped. Both were caught only because the environment was probed before building; either could have produced a confidently green gate over missing behaviour.

**Suggested improvement:** Add a cheap pre-spawn step for items whose criteria assert things about real on-disk data: enumerate the actual data the criteria describe and confirm each asserted case exists. Where a case is not live-reproducible, say so in the spawn prompt and require a fixture. Where the real data is messier than the criteria assume, pass the messiness in explicitly.

**Principle:** Acceptance criteria written from a mental model of the data will encode that model's errors. Probing the real data before building converts unstated assumptions into either verified cases or explicit fixtures — and a criterion that cannot be reproduced against live data is a test-design decision, not a passing test.
