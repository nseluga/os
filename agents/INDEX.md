# agents/

The Claude Code agent registry for the dev team. Every `dt-*` entry except `dt-orchestrator` is a symlink to that skill's `SKILL.md` in `../skills/` — one source of truth. Edit the skill file directly, never a copy here. New `dt-*` agents follow the same symlink pattern.

## Agents

- `dt-analyze` — Codebase mapper run before other agents
- `dt-engineer` — Designs and implements items in a worktree
- `dt-fix` — Applies reviewer findings and QA failures
- `dt-orchestrator` — Runs one plan item's full loop unattended (real file, not symlink)
- `dt-qa` — Writes/runs gating tests, emits PASS/FAIL
- `dt-research` — Cache-first current-tooling research
- `dt-review` — Efficiency/scalability/reliability/security review
- `dt-ui` — Frontend/UI specialist
- `research-partner` — Build-time research partner behavioral contract
