---
name: brief
description: Morning briefing after an autonomous run — reads artifacts from dev-team, dev-team-auto, or layout-loop and presents a structured changelog + ranked next steps. Use when the user says "/brief", "brief me", "what happened overnight", "what did the team do", or "catch me up".
---

# Brief

Read what an autonomous run produced while you were away. Leads with what changed, closes with what to do next. Designed to answer "what happened?" in under a minute and "what do I do now?" in one ranked list.

## Step 1 — Find the run

Check for recent artifacts in this order:

| Tool | Artifact |
|------|----------|
| dev-team / dev-team-auto | `.claude/dev-team/team-memory.md` (most recent entry) + `PROGRESS.md` if it exists |
| layout-loop | `.claude/layout-loop/report.md` or any `layout-loop-report*.md` in the project root |

**If one artifact is clearly most recent:** proceed with it.

**If multiple artifacts exist from different tools (multi-run night):** list what was found with their modification times and ask "Which run do you want briefed — or all of them?" Then run a brief per selection, in chronological order.

**If no artifact is found:** say so and stop. Don't hallucinate a report.

## Step 2 — Read the artifact(s)

Read the full artifact. For team-memory.md, read only the most recent run entry (entries are separated by `---` or timestamp headers).

## Step 3 — Produce the briefing

### For dev-team / dev-team-auto runs

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

---

### For layout-loop runs

**Header**
```
BRIEF — layout-loop · <date> · <branch-name>
Pages: N completed · N stopped early
```

**Per page — before/after screenshots**
Display the baseline and final screenshots inline for each page. If the environment cannot render images, output the file paths instead:
```
Page: <route>
Before: <path-to-baseline>
After:  <path-to-final>
Stopping condition: <converged | diminishing returns | iteration cap>
```

**Change log**
One bullet per iteration pass across all pages:
- `<page> pass N: <what changed and why>`

**Flagged decisions** — only for taste forks or structural variants:
```
⚑ <decision>
<2–4 lines: what the fork was, which direction was taken, the alternative, why the choice was made>
```
Skip for minor adjustments (spacing tweaks, color values) — the changelog bullet covers those.

**Failures**
If any page hit graceful-failure, one bullet per page with the reason.

---

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
| Flagged decision / taste fork | Detail block always |

## Notes

- Never summarize a blocked run as "mostly successful." If an item is blocked, the outcome is blocked.
- For layout-loop: if screenshots are missing or the report has no baseline, note it explicitly — don't describe visual changes in text alone.
- `/brief` reads and reports only. It does not merge, push, or re-trigger runs. The NEXT list is a recommendation; the user acts on it.
- If the run produced a project-independent lesson worth saving (visible in the team-memory.md "Remember next run" note), flag it at the end: "Worth saving to os memory: <one line>."
