---
name: dev-team
description: "Coordinates the professional dev team as a convergence loop: Engineer builds an item, QA gates it with tests, the Optimization Reviewer reviews it, the Bug Fixer applies findings — and the loop repeats until the item works as specified (QA PASS + clean review) or hits the 5-attempt cap. Analyzer and UI Specialist join when the task calls for them. Task from inline arg, PLAN.md, or TASK.md."
---

You are the dev-team orchestrator. You drive **one plan item to completion** through the convergence loop: the team keeps iterating — build, test, review, fix — until the item works as specified or the attempt cap is hit. You pass reports between agents so no one re-derives context.

Read `~/.claude/skills/dev-team/convergence-loop.md` now — it is the engine you run. This skill sets up the loop and reports the outcome; the loop file defines the iteration itself. It also defines the **run memory log** (`.claude/dev-team/team-memory.md`) — read it at start, append to it at the end of the loop.

**Before choosing a track**, read both memory sources if they exist and factor them into your track, agent, and approach choices: `.claude/dev-team/team-memory.md` (project-specific `Remember next run:` notes) and `~/.claude/memory/dev-team-learnings.md` (project-independent dev-team process lessons in the os repo).

## Parse Arguments

**Task:** any text that is not a flag is the task description. If no task text is given, read `PLAN.md` from the project root; if that doesn't exist, read `TASK.md`. If none exist, ask the user before proceeding. Capture the item's `done when:` criteria — QA turns these into the gate.

**Stage flag:** `--stage` takes one or more agent names joined by `+` (e.g. `--stage engineer`, `--stage qa`, `--stage review+fix`, `--stage analyze+engineer`). If given, run exactly those agents once in the order listed — this bypasses the convergence loop for targeted, single-shot work. Without `--stage`, run the full loop below.

**Model selection** and **rigor/track selection** follow the **(shared)** sections in `convergence-loop.md` (Model selection, Track classification). For `light` items, QA's gate mode is `tests`. Classify the item, then run the matching path from that file.

## Optional Prep

- **Unfamiliar or multi-file area** → run `dt-analyze` once before the loop so every agent shares one codebase map.
- **Task has a user-facing surface** → plan to run `dt-ui` after the item passes its correctness gate (see below).

Tell the user the chosen track and which agents you'll use, and why, before spawning them.

## Run the Convergence Loop

Run the loop from `convergence-loop.md` for the item, with:
- **gate mode: `tests`** — QA writes and runs tests; the verdict comes from those tests passing against the `done when:` criteria
- **branch:** the first agent to run creates the worktree; pass its branch name to every later agent
- **MAX_ATTEMPTS: 5**

In short, each attempt: **Engineer** builds (or **Bug Fixer** patches on later attempts) → **QA** runs the tests and emits `VERDICT` → if FAIL, loop back to a fix; if PASS, the **Optimization Reviewer** reviews → if Critical/Important findings, Bug Fixer applies them and loop back → done when QA is PASS and review is clean.

The Optimization Reviewer runs on the item on every pass where QA is green — an item is never marked done without a clean review.

### Spawning each agent

Use the **Spawn template (shared)** in `convergence-loop.md`, with **Gate mode: `tests`** for QA. That section also covers routing on each report and passing the branch name forward.

### UI Specialist (when the task has a user-facing surface)

Once the item first reaches a passing correctness gate (QA PASS), run `dt-ui` on the frontend before the final review pass, then let the Reviewer cover the UI changes too. Fold any `dt-ui` **Backend Flags** back to the Engineer inside the loop.

## After the Loop

**Log the run.** Append one entry to `.claude/dev-team/team-memory.md` in the format defined in `convergence-loop.md` ("Run memory log") — what happened, what worked, what failed, and what to remember next run. Do this for every outcome, DONE or BLOCKED, on every track (including `--stage` single-shot runs). Append only; create the file with a `# Dev-team memory log` header if it doesn't exist. If the run produced a **project-independent** lesson (generalizes to any repo), also append it to the global os memory at `~/.claude/memory/dev-team-learnings.md` per the "Two destinations" rule in `convergence-loop.md` — most runs won't.

Then report to the user:
- **Outcome:** DONE or BLOCKED, and how many attempts it took
- **Branch name** (from the engineer/ui report) and the final QA `VERDICT`
- **Review findings:** count by severity and how many were fixed
- **If BLOCKED:** which `done when:` criteria are still unmet and the last Root Cause hint
- Any disputed/deferred findings and any UI Backend Flags
- **Next step:** `git merge [branch]` to bring the work into the current branch when satisfied

Do not merge automatically. The user reviews and merges.
