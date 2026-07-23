---
name: improve-system
description: Audit and improve the ~/os system — memory, skills, and knowledge. Use when the user says "/improve-system", "audit the system", "clean up my os", "improve my setup", or "run a system pass". Two-phase: first applies any checkbox-approved items from the prior review, then does a fresh audit and sorts findings into auto-approve (applied immediately), needs sign-off (written to outputs/review.md), and more context required (written to outputs/needs-context.md).
---

# Improve System

Two-phase skill: apply prior approved changes, then audit the full ~/os system and sort findings into three action buckets.

## When to use

- Trigger phrases: "/improve-system", "audit the system", "clean up my os", "improve my setup", "system pass", "improve system"
- Situations: periodically (weekly/monthly), after a big sprint where new patterns emerged, when memory feels stale or skills feel bloated
- Do NOT use when: the user just wants to sync memory from sessions (use `/sync-claude-sessions` instead) or wants a targeted skill edit

---

## Phase 1 — Apply approved changes from prior review

**Run this phase every time, before the audit.**

### 1.1 — Check for prior review file

```bash
ls ~/os/outputs/review.md 2>/dev/null
```

If the file does not exist or is empty: skip to Phase 2.

### 1.2 — Read review.md and extract checked items

Read `~/os/outputs/review.md`. Find every item matching `- [x]` (checked checkbox). Ignore `- [ ]` items.

For each checked item, extract:
- **Type** field (new-skill | memory-edit | skill-edit | knowledge-restructure | memory-delete | link-fix)
- **Action** field (exact file path and operation)
- **Content** block (the new content or edit to apply)

### 1.3 — Apply each checked item

Apply changes in this order: deletes first, then edits, then creates. For each:

- **link-fix / memory-delete**: remove or correct the entry in MEMORY.md or delete the file
- **memory-edit**: edit the named memory file with the content from the Content block
- **skill-edit**: edit the named file under `~/os/skills/`
- **new-skill**: create `~/os/skills/<name>/SKILL.md` with the provided content
- **knowledge-restructure**: apply the structural change described

After each applied item, append a line to `~/os/outputs/change-log.md`:

```
[YYYY-MM-DD] APPLIED <Type> — <brief title from the item>
```

### 1.4 — Archive applied items from review.md

After applying all checked items: rewrite `~/os/outputs/review.md` keeping only the unchecked `- [ ]` items (the ones the user skipped). Add a header line:

```markdown
<!-- Last applied: YYYY-MM-DD — N items applied, M remaining -->
```

If all items were checked, write an empty review.md (just the header line).

---

## Phase 2 — Audit

Gather signal from five sources in parallel, then synthesize findings.

### 2.1 — Gather signal

Read all of the following:

**Memory:**
- `~/os/knowledge/memory/MEMORY.md` (the index)
- All `.md` files under `~/os/knowledge/memory/` (the fact files)

**Skills:**
- `ls ~/os/skills/` to get all skill folders
- For each skill, read its `SKILL.md`

**Recent sessions (last 7 days or last 10 sessions, whichever is larger):**
```bash
ls -lt ~/.claude/chat-histories/ | head -20
```
Read the most recent 10 session files from `~/.claude/chat-histories/`. Extract patterns, repeated manual tasks, and friction signals.

**Knowledge root:**
- `ls ~/os/knowledge/` to see the structure
- `ls ~/os/knowledge/me/` and `ls ~/os/knowledge/frameworks/` and `ls ~/os/knowledge/library/` (directory listings only, don't read every file)

**Change log:**
- `~/os/outputs/change-log.md` if it exists (to avoid re-proposing already-applied items)

### 2.2 — Identify findings

Look for ALL of the following. For each finding, note its type, evidence, and proposed action.

| Finding type | What to look for |
|---|---|
| **Broken MEMORY.md link** | An entry in MEMORY.md pointing to a `.md` file that doesn't exist under `~/os/knowledge/memory/` |
| **Stale memory** | A memory file whose content references dates, statuses, or facts that have clearly expired (e.g., project status says "in progress" from 6+ months ago) |
| **Contradiction** | Two memory files that assert conflicting facts about the same topic |
| **Coverage gap** | A topic that came up 3+ times in recent sessions but has no memory file |
| **Skill friction** | A skill invoked but user had to clarify scope, a skill that repeatedly fails to match its trigger, or steps in a skill that are always manually overridden |
| **Repeated manual task** | Something done manually in 2+ sessions that has no skill — grep the session histories for repeated command patterns or repeated multi-step explanations |
| **Token waste pattern** | Re-reading the same file multiple times in a session, large file reads where grep would do, parallel work that was sequential, anything you'd flag under the proactive token efficiency memory |
| **Skill bloat** | A skill with steps that are never reached, or a skill that duplicates another |
| **Empty/stub skill** | A skill folder missing a SKILL.md, or a SKILL.md with only the template placeholder text |
| **Dead knowledge file** | A file in `knowledge/` that is empty, a stub, or clearly superseded |

### 2.3 — Sort findings into three buckets

**Bucket A — Auto-approve (apply in this run, log to change-log.md):**

Only items that are ALL of the following:
- Zero ambiguity about what to change
- No content authored by the user that could be accidentally overwritten
- Mechanical fix (not a judgment call)
- Reversible (the original content is in git or can be trivially reconstructed)

Examples that qualify: removing a broken MEMORY.md index line (file verified to not exist), fixing a typo in a link path, deleting a genuinely empty file (0 bytes or only whitespace).

Examples that do NOT qualify: changing the meaning of a memory entry, resolving a contradiction, editing a skill.

Apply auto-approve items immediately. For each, append to `~/os/outputs/change-log.md`:
```
[YYYY-MM-DD] AUTO <finding type> — <what was done>
```

**Bucket B — Needs sign-off (write to outputs/review.md, do not apply):**

- Skill edits or rewrites
- New skill candidates
- Memory file rewrites or significant edits
- Contradiction resolutions (propose the resolution, don't apply it)
- Structural knowledge changes
- Stale memory updates where the correct new value is known

Write to `~/os/outputs/review.md` appending a new section for this run:

```markdown
## System Audit — YYYY-MM-DD

<!-- Check the box next to each item you approve. Run /improve-system again to apply checked items. -->

- [ ] **<Type in CAPS>: <brief title>**
  **Type:** <new-skill | memory-edit | skill-edit | knowledge-restructure | memory-delete | link-fix>
  **Action:** <exact file path and operation — e.g., "edit ~/os/knowledge/memory/user-profile.md lines 3-5">
  **Rationale:** <one sentence on why this improves the system>
  **Content:**
  ```
  <full new content for creates; unified diff for edits; "DELETE" for deletes>
  ```

```

Each item must be self-contained: the Content block must contain everything needed to apply the change without re-reading or re-deriving anything.

**Bucket C — More context required (write to outputs/needs-context.md, do not apply):**

- Ambiguous patterns you can't resolve alone (could be intentional or a bug)
- Contradictions where you don't know which version is correct
- Potential skill candidates where scope/trigger is unclear
- Any finding where guessing wrong costs more than asking

Append to `~/os/outputs/needs-context.md`:

```markdown
## Questions from system audit — YYYY-MM-DD

**Q: <specific question>**
Context: <what you observed that prompted this>
Options: <if there are clear choices, list them>

---
```

---

## Phase 3 — Report

After both phases complete, report to the user:

```
System pass complete — YYYY-MM-DD

Phase 1 (applied from prior review): N items applied / M skipped
Phase 2 (this audit):
  Auto-applied: N fixes  → change-log.md
  Needs sign-off: N items → outputs/review.md
  More context: N questions → outputs/needs-context.md

Auto-applied: [list each item in one line]
Review needed: [list titles only, one line each]
Questions: [list question headlines only]
```

If outputs/review.md has items: "Run /improve-system again after checking boxes in ~/os/outputs/review.md."
If outputs/needs-context.md has items: "Answer questions in ~/os/outputs/needs-context.md, then re-run."

---

## Notes & gotchas

- **Never** touch `~/os/skills/` or `~/os/knowledge/` for a Bucket B item without a `[x]` checkbox from the user. The Phase 1 apply step is the only gate.
- Bucket A is conservative. When in doubt, demote to Bucket B. A false positive in auto-apply is worse than an extra checkbox.
- The Content block in review.md must be complete and literal — Phase 1 applies it mechanically without re-reading source files.
- For `memory-edit` items, include the full new file content (not a partial patch) so Phase 1 can do a clean write.
- For `new-skill` items, include the full SKILL.md content including frontmatter.
- If `~/os/outputs/` does not exist, create it before writing any output files.
- `change-log.md` is append-only — never rewrite it, only append.
- The skill reads session histories for signal but does NOT write to memory files directly. Memory changes go through Bucket B (needs sign-off).
- When scanning sessions, focus on patterns across multiple sessions, not one-off moments.
