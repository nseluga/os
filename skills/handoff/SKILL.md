---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
---

Write a short handoff document so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Scope it to the part of the plan just covered in this conversation, not the whole history. Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs) - reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

Output must be no longer than 30 lines total:
- What was just done (a few bullets)
- Key decisions and why, only where non-obvious - skip anything self-evident from the diff
- Suggested skills for the next agent to invoke
- Next step

If it doesn't fit in 30 lines, cut detail rather than sections.
