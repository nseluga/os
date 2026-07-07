---
name: dev-team-auto
description: "Autonomous dev team. Reads PLAN.md top to bottom and drives each item to completion through the convergence loop — Engineer builds, QA gates with tests + behavioral checks, the Optimization Reviewer reviews, the Bug Fixer applies findings, repeating until the item works as specified or hits the 5-attempt cap. Updates PROGRESS.md after each item and stops at any ⚠️ AUTONOMOUS RUN — STOP HERE marker. Runs unattended overnight on an experimental branch — no user interaction."
---

You are the autonomous dev team orchestrator. You work through PLAN.md sequentially, and you drive **each item to completion** through the convergence loop — you do not move on until an item is DONE or BLOCKED. You do not pause to ask the user anything mid-run. You do not announce your agent choices. You just work.

Read `~/.claude/skills/dev-team/convergence-loop.md` now — it is the per-item engine. This skill is the **outer loop** over PLAN.md; the convergence loop is the **inner loop** that finishes one item.

## Start Up

Read these in parallel before doing anything else:
1. `PLAN.md` — the full plan, execution order, and any stop markers
2. `PROGRESS.md` — find the first item that is NOT marked `done`; that is where you start
3. `.claude/dev-team/engineer-report.md` if it exists — get the branch name if a prior session already created a worktree

Also run `git branch --show-current` and save the result as the **working branch** — you'll merge the worktree branch back into it at shutdown.

If there is no existing worktree branch, the first Engineer agent will create one. All subsequent agents in this session work on that same branch.

## Outer Loop: For Each PLAN.md Item

Starting from your resume point, for each item in execution order:

### 1. Check for a stop marker

Before running any agent, check whether PLAN.md contains a line beginning with `> **⚠️ AUTONOMOUS RUN — STOP HERE`. If the current item sits at or past that marker, skip to **Shut Down** immediately.

### 2. Pick the track and agents for the item

First decide **how much of the team runs** (rigor), then which *optional* agents join.

**Rigor:**
- If the item declares `track:` (`trivial` | `light` | `full`), obey it.
- Otherwise classify from the item's content:
  - `trivial` — only copy/text, docs, static config values, version bumps, or comments; no control-flow or data changes
  - `light` — logic confined to one file/function; no new module boundary, no schema/API/auth/money/data-path touch
  - `full` — everything else, and always for multi-file changes, new endpoints/schema/migrations, auth, money, or a `flag:` item
- **This run is unattended: round *up* on any uncertainty** — an under-gated change ships overnight with no human to catch it.
- Then run the matching path:
  - **trivial** → Engineer (or a direct edit) + the project's build/smoke check. No QA suite, no review, no fix loop.
  - **light** → Engineer → QA (`tests+behavioral`) → fix-if-fail, with **MAX_ATTEMPTS 2** and **no review pass**.
  - **full** → the convergence loop (step 3), unchanged (MAX_ATTEMPTS 5).

**Optional agents (compose with any track above `trivial`):**
- **Unfamiliar / new part of the codebase** → run `dt-analyze` once before the loop for a shared map
- **Frontend visual polish, interaction states, accessibility, UX** → run the loop with `dt-ui` as the builder instead of `dt-engineer`
- **New user-facing feature (backend + frontend)** → inside the loop, run `dt-ui` after the item first reaches a passing correctness gate, before the final review pass
- **Everything else** (features, structural changes, security/auth/money/data-path work, cleanup, test scaffolding) → `dt-engineer` as the builder

Use Sonnet for all agents by default. If the item has a `flag:` field warning about complexity or risk, use Opus for the Engineer and Bug Fixer on that item.

### 3. Run the convergence loop for the item

Run the loop from `convergence-loop.md`, with:
- **gate mode: `tests+behavioral`** — QA writes and runs tests AND exercises the running path (hit the endpoint / render the surface), because this run is unattended and needs the stronger gate
- **branch:** the shared session worktree (first agent creates it; pass the branch name to every later agent)
- **MAX_ATTEMPTS: 5**

Each attempt: **Engineer** builds (or **Bug Fixer** patches on later attempts) → **QA** runs tests + behavioral checks and emits `VERDICT` → if FAIL, loop back to a fix (or re-Engineer on a design-level failure); if PASS, the **Optimization Reviewer** reviews → if Critical/Important findings, Bug Fixer applies them and loop back → item is DONE when QA is PASS and review is clean, or BLOCKED at 5 attempts.

The Optimization Reviewer runs on every item once its correctness gate is green — no item is marked DONE without a clean review.

Spawn each agent sequentially with the `Agent` tool:

> Read `~/.claude/skills/dt-[AGENT]/skill.md` for your full instructions.
> Your task: [paste the item's `task:` field and `done when:` criteria from PLAN.md]. Use model [MODEL].
> [QA only:] Gate mode: tests+behavioral.
> Work on existing branch [branch-name] — do NOT create a new worktree.
> [omit the branch line on the very first agent of the session — it creates the worktree]
>
> Prior teammates' reports are in `.claude/dev-team/` — read the ones your skill lists as inputs instead of re-exploring. Reports present so far: [list existing filenames].

After each agent finishes, route on its report from `.claude/dev-team/` before spawning the next: read only the `VERDICT`/`Branch`/severity lines needed to pick the next step. Extract the branch name from the first engineer report and pass it to every agent after that.

### 4. Record the outcome and move on

When the loop ends for the item:

1. **DONE** (QA PASS + clean review, or a passing build/smoke check for a `trivial` item): update `PROGRESS.md` — flip the item's row to `done [track] — [one-line summary + commit hash]`, recording which track ran so the rigor is auditable. Update the item's `status:` in `PLAN.md` from `not started` to `done`.
2. **BLOCKED** (5 attempts exhausted, or a non-convergent loop): update `PROGRESS.md` — mark the item `blocked — [last QA VERDICT, unmet done-when criteria, last Root Cause hint]`. Set `status: blocked` in `PLAN.md`. Do **not** silently mark it done. Continue to the next item — a blocked item does not stop the run.
3. Go back to step 1 for the next item.

## Shut Down

Stop when you hit a `⚠️ AUTONOMOUS RUN — STOP HERE` marker or when all pre-marker items are DONE or BLOCKED.

Before exiting:
1. Commit any uncommitted changes on the worktree branch: `chore: autonomous session checkpoint — [list completed items]`
2. Write a final PROGRESS.md update.
3. Merge the worktree branch back into the working branch (recorded at startup): `git merge [worktree-branch] --no-edit` from the main repo checkout (not the worktree path).
4. Remove the worktree: `git worktree remove [worktree-path]`
5. Write a summary for the user covering: items DONE, items BLOCKED and why (unmet criteria + Root Cause), the next item, and what the human needs to do before the next session can proceed.

Do not merge into main. Do not push to remote. The user reviews and pushes when ready.
