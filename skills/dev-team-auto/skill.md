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
4. `.claude/dev-team/team-memory.md` if it exists — the project-specific cross-run log; factor its `Remember next run:` notes into your track and approach choices (flaky suites, build flags, dead-end approaches to avoid, etc.)
5. `~/.claude/memory/dev-team-learnings.md` if it exists — the project-independent dev-team process lessons in the os repo; apply them to your track/model/approach choices for any repo

Also run `git branch --show-current` and save the result as the **working branch** — you'll merge the worktree branch back into it at shutdown.

If there is no existing worktree branch, the first Engineer agent will create one. All subsequent agents in this session work on that same branch.

## Outer Loop: For Each PLAN.md Item

Starting from your resume point, for each item in execution order:

### 1. Check for a stop marker

Before running any agent, check whether PLAN.md contains a line beginning with `> **⚠️ AUTONOMOUS RUN — STOP HERE`. If the current item sits at or past that marker, skip to **Shut Down** immediately.

### 2. Pick the track and agents for the item

First decide **how much of the team runs** (rigor), then which *optional* agents join.

**Rigor:** classify the item and run the matching path per the **Track classification (shared)** section in `convergence-loop.md`. This run is unattended, so round *up* on any uncertainty — an under-gated change ships overnight with no human to catch it. For `light` items, QA's gate mode is `tests+behavioral`.

**Optional agents (compose with any track above `trivial`):**
- **Multi-file `full`-track item, or any unfamiliar area** → run `dt-analyze` once before the loop for a shared map. This is the **default** for multi-file items — its `analyze-report.md` is injected into every agent so none of them re-explore the codebase (see `convergence-loop.md` → Spawn template). Skip it only for single-file items.
- **Frontend visual polish, interaction states, accessibility, UX** → run the loop with `dt-ui` as the builder instead of `dt-engineer`
- **New user-facing feature (backend + frontend)** → inside the loop, run `dt-ui` after the item first reaches a passing correctness gate, before the final review pass
- **Everything else** (features, structural changes, security/auth/money/data-path work, cleanup, test scaffolding) → `dt-engineer` as the builder

Model and effort per agent follow the **Model & effort selection (shared)** table in `convergence-loop.md` (Sonnet default; full-track engineer high-effort; QA medium; review high-effort — Opus on the engineer, fixer, and review for `flag:` items).

### 3. Run the convergence loop for the item

Run the loop from `convergence-loop.md`, with:
- **gate mode: `tests+behavioral`** — QA writes and runs tests AND exercises the running path (hit the endpoint / render the surface), plus a **live smoke pass** against a real server + real dev DB (not mocks) for any item touching routes/models/migrations/serialization. This run is unattended with no human to catch a mocked-green/live-broken gap, so the un-mocked smoke pass is required.
- **branch:** the shared session worktree (first agent creates it; pass the branch name to every later agent)
- **MAX_ATTEMPTS: 5**

Each attempt: **Engineer** builds (or **Bug Fixer** patches on later attempts) → **QA** runs tests + behavioral checks and emits `VERDICT` → if FAIL, loop back to a fix (or re-Engineer on a design-level failure); if PASS, the **Optimization Reviewer** reviews → if Critical/Important findings, Bug Fixer applies them and loop back → item is DONE when QA is PASS and review is clean, or BLOCKED at 5 attempts.

The Optimization Reviewer runs on every item once its correctness gate is green — no item is marked DONE without a clean review.

Spawn each agent sequentially using the **Spawn template (shared)** in `convergence-loop.md`, with **Gate mode: `tests+behavioral`** for QA. Draw the task text from the item's `task:` field and `done when:` criteria in PLAN.md. That section also covers routing on each report and passing the branch name forward.

### 4. Record the outcome and move on

When the loop ends for the item, record its outcome as **one action with two writes** — do both before touching the next item, never batch them to shutdown:

1. **Write the outcome:**
   - **DONE** (QA PASS + clean review, or a passing build/smoke check for a `trivial` item): update `PROGRESS.md` — flip the item's row to `done [track] — [one-line summary + commit hash]`, recording which track ran so the rigor is auditable. Update the item's `status:` in `PLAN.md` from `not started` to `done`.
   - **BLOCKED** (5 attempts exhausted, or a non-convergent loop): update `PROGRESS.md` — mark the item `blocked — [last QA VERDICT, unmet done-when criteria, last Root Cause hint]`. Set `status: blocked` in `PLAN.md`. Do **not** silently mark it done. A blocked item does not stop the run.
2. **In the same step, append the team-memory entry.** Immediately after the PROGRESS.md write — same item, before moving on — append one entry to `.claude/dev-team/team-memory.md` in the `convergence-loop.md` ("Run memory log") format: what happened, what worked, what failed, what to remember next run. Every item, every track, DONE or BLOCKED. Append only; create the file with a `# Dev-team memory log` header if it doesn't exist. This is what lets the next overnight run learn from this one — and it only happens if it rides on the PROGRESS.md write above, so treat the two as inseparable. If the item surfaced a **project-independent** lesson (generalizes to any repo), also append it to the global os memory at `~/.claude/memory/dev-team-learnings.md` per the "Two destinations" rule in `convergence-loop.md` — be conservative; most items won't.
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
