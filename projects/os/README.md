---
name: os
status: active
priority: high
last_active: 2026-07-11
next_step: "Ongoing — continuous improvement of knowledge, skills, and tooling"
repo: ~/os
github: https://github.com/nseluga/os
summary: "Personal operating system — knowledge, skills, and project index; the source of truth for Claude Code's global skills and memory."
tags: [meta, tooling]
---

**Related:** [os-evals](../os-evals/README.md) measures which layers of this setup earn their keep via ablation.

## Where it stands

The always-on meta repo — global skills, memory, knowledge, and this project index all live here and load automatically. Continuously improved; no phase boundary. The canonical shape for every file in `projects/*/README.md` is defined in [`projects/_TEMPLATE.md`](../_TEMPLATE.md).

## Key files

- **projects/_TEMPLATE.md** — project README template/reference.
- **knowledge/memory/MEMORY.md** — memory index.
- **skills/** — global skills (symlinked to `~/.claude/skills`).
