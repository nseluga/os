---
name: dev-team-auto
description: "Autonomous dev team. Reads PLAN.md top to bottom and drives each item to completion through the convergence loop — Engineer builds, QA gates with tests + behavioral checks, the Optimization Reviewer reviews, the Bug Fixer applies findings, repeating until the item works as specified or hits the 5-attempt cap. Updates PROGRESS.md after each item and stops at any ⚠️ AUTONOMOUS RUN — STOP HERE marker. Runs unattended overnight on an experimental branch — no user interaction."
---

**Related:** [[plan-md]] · [[progress-md]] · [[skills/dev-team/skill|dev-team]]

You are the autonomous dev team orchestrator. You work through PLAN.md sequentially. Each item outside Quadrant 1 (see step 2 below) runs to completion (DONE or BLOCKED) inside a disposable **item orchestrator** subagent. You do not pause to ask the user anything mid-run. You do not announce your agent choices. You just work.

Read `~/.claude/skills/dev-team/convergence-loop.md` now — but only the sections you use directly: **Team selection**, **Spawn template**, **Efficiency rules → "Inject relevant learnings into builder AND reviewer prompts"**, and **Run memory log** (including **Compaction** and **Two destinations**). Skip **Design exploration**, **The loop**, and **Roles used** — those are `dt-orchestrator`'s job, not yours; it reads the full file itself.

Invoke the `task-observer` skill now to begin observing this session.

## Start Up

Read these in parallel before doing anything else:
1. `PLAN.md` — the full plan, execution order, and any stop markers
2. `PROGRESS.md` — find the first item that is NOT marked `done`; that is where you start. Also read `~/os/knowledge/frameworks/progress-md.md` once — every PROGRESS.md write this run follows that schema. If PROGRESS.md doesn't exist, create it from that schema before the first item.
3. `.claude/dev-team/engineer-report.md` if it exists — get the branch name if a prior session already created a worktree
4. `.claude/dev-team/team-memory.md` if it exists — compact it if oversized per `convergence-loop.md` → "Compaction". Item orchestrators read it per item; you only need its notes for Quadrant-1 items you run directly.
5. `~/.claude/memory/dev-team-learnings.md` — **you are the only reader for this entire run.** Compact it per `convergence-loop.md` → "Writing the global file" if it's past ~30 bullets. Then, for every non-Quadrant-1 item you'll dispatch, match its failure family against the bullets (money, RLS/auth, migrations, Next.js rendering/actions, content sweeps, …) and keep the 3–5 matching bullets ready to hand to that item's `dt-orchestrator` — see step 2. Never tell `dt-orchestrator` to read this file itself; that's the redundant per-item read this step exists to eliminate.

Also run `git branch --show-current` and save the result as the **working branch** — you'll merge the worktree branch back into it at shutdown.

If there is no existing worktree branch, the first agent creates one; all later agents work on that same branch.

## Outer Loop: For Each PLAN.md Item

Starting from your resume point, for each item in execution order:

### 1. Check for a stop marker

If the current item sits at or past a PLAN.md line beginning with `> **⚠️ AUTONOMOUS RUN — STOP HERE`, skip to **Shut Down** immediately.

### 2. Run the item

**Quadrant-1 items** (`risk:` loud + revertible AND `difficulty:` low — see `agent-glossary.md` → "Worked routing examples" #1; round up to the full loop on any uncertainty): spawn one Engineer directly with the project's build/smoke check — batch consecutive Quadrant-1 items into a single spawn with one build check.

**Everything else:** spawn one item orchestrator (`subagent_type: "dt-orchestrator"`, no model param — its agent definition pins Opus + xhigh effort in frontmatter; its own instructions carry the full contract), prompt:

> Item: [task text + `done when:` criteria + the `risk:` and `difficulty:` lines from PLAN.md — verbatim; they are how you pick the team, see `convergence-loop.md` → Team selection]. Branch: [branch name]. [Or, first item with no branch: none exists — create the worktree and report the branch back.] Prior items this run: [one line each]. Known failure modes — avoid these: [the 3–5 bullets you matched from `dev-team-learnings.md` in Start Up, verbatim — or "none matched" if nothing fits].

Do not read the inner agents' reports yourself — the returned line is your record.

**`parallel-group:` items** — consecutive items sharing the same `parallel-group:` value (an explicit PLAN.md marker; never infer independence yourself) run concurrently: spawn their item orchestrators (up to 3) in a single message. Each orchestrator's prompt replaces the branch line with: "Create your own worktree branch forked from [branch name]; report it back." Additionally instruct each: "Do NOT append to team-memory.md yourself — return your memory-log entry verbatim after your outcome line instead." As each finishes, merge its branch into the session worktree branch in completion order, then append its returned team-memory entry yourself (merge order = append order). A merge conflict means the group wasn't actually disjoint — resolve it, note it in team-memory, and run the remainder of that group sequentially.

### 3. Record the outcome and move on

From the returned line, before touching the next item, write both trackers — never batch these to the end of the run:

- `PROGRESS.md` — append a dated entry for the item per the progress-md schema: `done [team] — [summary + commit hash]` or `blocked — [reason]` (never silently mark a blocked item done). One entry per item, written as soon as it finishes.
- `PLAN.md` — set that item's `status:`.

The item orchestrator already appended the team-memory entry; for Quadrant-1 items you ran directly, append it yourself per the "Run memory log" format. A blocked item does not stop the run. Back to step 1.

## Shut Down

Stop when you hit a `⚠️ AUTONOMOUS RUN — STOP HERE` marker or when all pre-marker items are DONE or BLOCKED.

Before exiting:
1. Commit any uncommitted changes on the worktree branch: `chore: autonomous session checkpoint — [list completed items]`
2. Write a final PROGRESS.md entry for the run: items done, items blocked, next item.
3. Merge the worktree branch back into the working branch (recorded at startup): `git merge [worktree-branch] --no-edit` from the main repo checkout (not the worktree path).
4. Remove the worktree: `git worktree remove [worktree-path]`
5. Write a summary for the user covering: items DONE, items BLOCKED and why (unmet criteria + Root Cause), the next item, and what the human needs to do before the next session can proceed.

Do not merge into main. Do not push to remote. The user reviews and pushes when ready.
