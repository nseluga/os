---
name: brief
description: Morning briefing after an autonomous run — reads artifacts from dev-team or dev-team-auto and presents a structured changelog + ranked next steps. Use when the user says "/brief", "brief me", "what happened overnight", "what did the team do", or "catch me up".
---

# Brief

Read what an autonomous run produced while you were away. Leads with what changed, closes with what to do next. Designed to answer "what happened?" in under a minute and "what do I do now?" in one ranked list.

## Step 1 — Find the run

Check for a recent artifact: `.claude/dev-team/team-memory.md` (most recent entry) + `LANE_PROGRESS.md` if it exists.

**If no artifact is found:** say so and stop. Don't hallucinate a report.

## Step 2 — Read the artifact(s)

Read the full artifact. For team-memory.md, read only the most recent run entry (entries are separated by `---` or timestamp headers).

## Step 3 — Produce the briefing

**Header**
```
BRIEF — dev-team[-auto] · <date> · <branch-name>
Outcome: DONE (N items) / BLOCKED (N/M items)
```

**What ran**
One bullet per plan item:
- `✓ <item name>` — for completed items
- `✗ <item name> — BLOCKED` — for blocked items
- `~ <item name> — deferred/disputed` — for anything unresolved

**Detail blocks** — only for items that touched security, scalability, efficiency, or reliability:
```
⚠ <item name>
<2–4 lines: what the decision was, why it matters, what was chosen and why>
```
Skip this block entirely for routine features and bug fixes — the bullet is enough.

**Review findings** (if a review ran)
```
Review: N critical · N important · N minor
Fixed: N  |  Deferred: N  |  Disputed: N
```
If any deferred or disputed findings exist, list them as bullets with a one-line reason each.

**Blockers** (if any items are BLOCKED)
For each blocked item — always use the detail block format regardless of category:
```
✗ <item name>
<2–4 lines: what criterion was unmet, root cause hint from the log, what's needed to unblock>
```

## Step 4 — NEXT

Always end with a ranked action list. One line per action, with a parenthetical reason:

```
NEXT:
1. git merge <branch>  (QA clean, review clean — ready to ship)
2. <specific fix needed>  (unblocks item N)
3. <thing to eyeball>  (flagged decision — needs your call before merging)
```

Order: merge-ready items first, fixes second, judgment calls third. If nothing is merge-ready, say so explicitly on line 1.

## Detail level rules

| Change type | Format |
|-------------|--------|
| Routine feature, bug fix, style change | Bullet only |
| Security, scalability, efficiency, reliability | Detail block (2–4 lines) |
| Blocker | Detail block always |

## Notes

- Never summarize a blocked run as "mostly successful." If an item is blocked, the outcome is blocked.
- `/brief` reads and reports only. It does not merge, push, or re-trigger runs. The NEXT list is a recommendation; the user acts on it.
- If the run produced a project-independent lesson worth saving (visible in the team-memory.md "Remember next run" note), flag it at the end: "Worth saving to os memory: <one line>."
