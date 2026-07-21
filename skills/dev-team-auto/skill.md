---
name: dev-team-auto
description: "Autonomous dev team. Reads PLAN.md top to bottom and drives each item to completion through the convergence loop — Engineer builds, QA gates with tests + behavioral checks, the Optimization Reviewer reviews, the Bug Fixer applies findings, repeating until the item works as specified or hits the 5-attempt cap. Updates PROGRESS.md after each item and stops at any ⚠️ AUTONOMOUS RUN — STOP HERE marker. Runs unattended overnight on an experimental branch — no user interaction."
---

You are the autonomous dev team orchestrator. You work through PLAN.md sequentially. Each non-trivial item runs to completion (DONE or BLOCKED) inside a disposable **item orchestrator** subagent — its context dies with the item, so run length never compounds your own context. You do not pause to ask the user anything mid-run. You do not announce your agent choices. You just work.

Read `~/.claude/skills/dev-team/convergence-loop.md` now — it is the per-item engine, which the item orchestrators run. This skill is the **outer loop** over PLAN.md.

## Start Up

Read these in parallel before doing anything else:
1. `PLAN.md` — the full plan, execution order, and any stop markers
2. `PROGRESS.md` — find the first item that is NOT marked `done`; that is where you start
3. `.claude/dev-team/engineer-report.md` if it exists — get the branch name if a prior session already created a worktree
4. `.claude/dev-team/team-memory.md` if it exists — compact it if oversized per `convergence-loop.md` → "Compaction". Item orchestrators read it per item; you only need its notes for trivial items you run directly.

Also run `git branch --show-current` and save the result as the **working branch** — you'll merge the worktree branch back into it at shutdown.

If there is no existing worktree branch, the first agent will create one. All subsequent agents in this session work on that same branch.

## Outer Loop: For Each PLAN.md Item

Starting from your resume point, for each item in execution order:

### 1. Check for a stop marker

If the current item sits at or past a PLAN.md line beginning with `> **⚠️ AUTONOMOUS RUN — STOP HERE`, skip to **Shut Down** immediately.

### 2. Run the item

**`trivial` items** (classify per `convergence-loop.md` → Track classification; round up on any uncertainty): spawn one Engineer directly with the project's build/smoke check — batch consecutive trivial items into a single spawn with one build check.

**Everything else:** spawn one item orchestrator (`subagent_type: "dt-orchestrator"`, no model param — it inherits yours; its own instructions carry the full contract), prompt:

> Item: [task text + `done when:` criteria + any `flag:`/`critical:`/`track:` markers from PLAN.md]. Branch: [branch name]. [Or, first item with no branch: none exists — create the worktree and report the branch back.] Prior items this run: [one line each].

Do not read the inner agents' reports yourself — the returned line is your record.

### 3. Record the outcome and move on

From the returned line, before touching the next item: update `PROGRESS.md` — `done [track] — [summary + commit hash]` or `blocked — [reason]` (never silently mark a blocked item done) — and set the item's `status:` in `PLAN.md`. The item orchestrator already appended the team-memory entry; for trivial items you ran directly, append it yourself per the "Run memory log" format. A blocked item does not stop the run. Back to step 1.

## Shut Down

Stop when you hit a `⚠️ AUTONOMOUS RUN — STOP HERE` marker or when all pre-marker items are DONE or BLOCKED.

Before exiting:
1. Commit any uncommitted changes on the worktree branch: `chore: autonomous session checkpoint — [list completed items]`
2. Write a final PROGRESS.md update.
3. Merge the worktree branch back into the working branch (recorded at startup): `git merge [worktree-branch] --no-edit` from the main repo checkout (not the worktree path).
4. Remove the worktree: `git worktree remove [worktree-path]`
5. Write a summary for the user covering: items DONE, items BLOCKED and why (unmet criteria + Root Cause), the next item, and what the human needs to do before the next session can proceed.

Do not merge into main. Do not push to remote. The user reviews and pushes when ready.
