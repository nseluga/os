# memory/ — index

Claude Code's managed memory: one fact per file, auto-loaded via
`autoMemoryDirectory`. This file explains the folder for navigation;
**`MEMORY.md` is the canonical per-memory index** (auto-loaded every session,
one line per fact) — look there to find a specific memory, never here.

## Structure

- `MEMORY.md` — the auto-loaded index: one line per memory file
- Fact files, named by type prefix:
  - `user-*` — who Nate is (role, expertise, preferences)
  - `feedback-*` — corrections and confirmed approaches, with why + how to apply
  - `project-*` — ongoing work, goals, constraints not derivable from code
  - `reference-*` — pointers to external resources
- Files carry frontmatter (`name`, `description`, `metadata.type`) and link to
  related memories with `[[wikilinks]]`

Maintenance: every memory write/delete updates MEMORY.md in the same turn
(rule lives in the harness memory instructions, not here).
