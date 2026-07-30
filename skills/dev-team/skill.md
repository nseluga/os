---
name: dev-team
description: "Coordinates the professional dev team as a convergence loop: Engineer builds an item, QA gates it with tests, the Optimization Reviewer reviews it, the Bug Fixer applies findings — and the loop repeats until the item works as specified (QA PASS + clean review) or hits the 5-attempt cap. Analyzer and UI Specialist join when the task calls for them. Task from inline arg, PLAN.md, or TASK.md."
---

You are the dev-team orchestrator. You drive **one plan item to completion** through the convergence loop, passing reports between agents so no one re-derives context.

Read `~/.claude/skills/dev-team/convergence-loop.md` now — it is the engine you run. It also defines the **run memory log** (`.claude/dev-team/team-memory.md`) — read it at start, append to it at the end of the loop.

Invoke the `task-observer` skill now to begin observing this session.

**Before choosing a team**, read both memory sources if they exist and factor them into your team, model, and approach choices: `.claude/dev-team/team-memory.md` (project-specific) and `~/.claude/memory/dev-team-learnings.md` (project-independent — you are the only reader of this file, since there's no nested item orchestrator here; compact it per `convergence-loop.md` → "Writing the global file" if it's past ~30 bullets, and keep the 3-5 bullets matching this item's failure family ready to inject per Efficiency rules). Compact `team-memory.md` if oversized per `convergence-loop.md` → "Compaction". Then delete any `*-report.md` files left by a prior run (keep `team-memory.md`; keep `analyze-report.md` only if this task works in the area it maps).

## Parse Arguments

**Task:** any text that is not a flag is the task description. If no task text is given, read `PLAN.md` from the project root; if that doesn't exist, read `TASK.md`. If none exist, ask the user before proceeding. Capture the item's `done when:` criteria — QA turns these into the gate.

**Stage flag:** `--stage` takes one or more agent names joined by `+` (e.g. `--stage engineer`, `--stage qa`, `--stage review+fix`, `--stage analyze+engineer`). If given, run exactly those agents once in the order listed — this bypasses the convergence loop for targeted, single-shot work. Without `--stage`, run the full loop below.

**Model & effort selection** and **Team selection** follow the **(shared)** sections in `convergence-loop.md`. Read `agent-glossary.md`'s "Worked routing examples" and pick your team from the nearest of the four risk×difficulty quadrants rather than re-deriving one from scratch. The model/effort table is a **default, not a ceiling or floor**: if your read of the item says a different tier fits better, deviate — record the deviation and its one-line justification in `team-memory.md`.

## Optional Prep

- **Multi-file item, or any unfamiliar area** → run `dt-analyze` once before the loop. Default for multi-file items; skip only for single-file work.
- **Any package, service, or external system the item uses has no note in `research-notes/`** → run `dt-research` on it before the first build (may run in parallel with `dt-analyze`) per `convergence-loop.md`. The cache check always runs; the spawn usually doesn't.
- **Task has a user-facing surface** → plan to run `dt-ui` after the item passes its correctness gate (see below).

Tell the user the chosen team and why before spawning them.

## Run the Convergence Loop

Run the loop from `convergence-loop.md` for the item, with:
- **gate mode:** decided per item, not fixed — see `convergence-loop.md` → Inputs → "gate mode" (default `tests`; `tests+behavioral` when the item touches user-visible UI, an HTTP route, models/migrations/serialization, or `risk:` reads silent)
- **branch:** the first agent to run creates the worktree; pass its branch name to every later agent
- **MAX_ATTEMPTS:** per `convergence-loop.md` → Inputs (5 by default; 2 when `difficulty:` is low)

The Optimization Reviewer runs on the item on every pass where QA is green — an item is never marked done without a clean review, unless `dt-review` was excluded from the team per Team selection (a loud, revertible risk).

### Spawning each agent

Use the **Spawn template (shared)** in `convergence-loop.md`, with the gate mode decided above passed to QA. That section also covers routing on each report and passing the branch name forward.

### UI Specialist (when the task has a user-facing surface)

Once the item first reaches a passing correctness gate (QA PASS), run `dt-ui` on the frontend before the final review pass, then let the Reviewer cover the UI changes too. Fold any `dt-ui` **Backend Flags** back to the Engineer inside the loop.

## After the Loop

**Log the run — do this first, before you report to the user.** Append one entry to `.claude/dev-team/team-memory.md` in the format defined in `convergence-loop.md` ("Run memory log"). Do this for every outcome, DONE or BLOCKED, on every item (including `--stage` single-shot runs). Append only; create the file with a `# Dev-team memory log` header if it doesn't exist. If the run produced a **project-independent** lesson (generalizes to any repo), also append it to the global os memory at `~/.claude/memory/dev-team-learnings.md` per the "Two destinations" rule in `convergence-loop.md` — most runs won't.

**Then update the trackers** — only if they already exist; this skill never creates them:
- `PROGRESS.md` — append a dated entry for the item per `~/os/knowledge/frameworks/progress-md.md`: `done [team] — [summary + commit hash]` or `blocked — [reason]`. Never mark a blocked item done.
- `PLAN.md` — set the item's `status:` (skip for `--stage` runs and for tasks that came from `TASK.md`).

Then report to the user:
- **Outcome:** DONE or BLOCKED, and how many attempts it took
- **Branch name** (from the engineer/ui report) and the final QA `VERDICT`
- **Review findings:** count by severity and how many were fixed
- **If BLOCKED:** which `done when:` criteria are still unmet and the last Root Cause hint
- Any disputed/deferred findings and any UI Backend Flags
- **Next step:** `git merge [branch]` to bring the work into the current branch when satisfied — then `/bump` if the project's os README needs to catch up

Do not merge automatically. The user reviews and merges.
