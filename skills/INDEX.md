# skills/

One folder per skill. Each `SKILL.md`'s `description:` frontmatter is the canonical router text; this README is a human-browsable index. `skills.md` at this level is the template for new skills (see CLAUDE.md "Authoring a new skill").

## Dev team

- `design` — Interactive design skill: five drafts side by side, narrow to one, then tweak it live in the browser. Prompts with real reference images from `knowledge/library/inspiration/`; Impeccable's detector is the anti-slop floor. Ships `tweaks.js`, the in-page control panel.
- `dev-team` — Coordinates the dev team convergence loop for one plan item
- `dev-team-auto` — Autonomous dev team drives PLAN.md items through convergence loop
- `dt-analyze` — Code Analyzer maps the codebase before other agents work
- `dt-engineer` — Engineer owns large-scale design and implements in worktree
- `dt-fix` — Bug Fixer applies reviewer findings and QA failures
- `dt-qa` — QA/Tester writes and runs the gating tests, emits PASS/FAIL
- `dt-research` — Researcher cache-first web research on current tools and frameworks
- `dt-review` — Optimization Reviewer efficiency, scalability, reliability, security findings
- `dt-ui` — UI Specialist frontend layout, hierarchy, responsiveness, accessibility

## Planning & review

- `plan-md` — Grill the user into a schema-valid PLAN.md for dev-team execution
- `grill-me` — A relentless interview to sharpen a plan or design
- `research-partner` — Build-time research partner standup ritual, methods pushback
- `research-review` — Skeptical peer review of completed research work
- `ml-engineer` — ML engineering partner for technique selection and training code
- `storm-research` — 5-lens (practitioner/academic/skeptic/economist/historian) verified HTML research briefing

## os maintenance

- `improve-system` — Audit and improve the ~/os system memory, skills, knowledge
- `ai-usage-optimizer` — Audit how well Nate uses AI systems and prescribe leverage
- `ingest-data` — Triage files in knowledge/raw into their destinations
- `sync-claude-sessions` — Sync learnings from recent chat histories into memory
- `bump` — End-of-session closer: bump the project's os README, offer session memory
- `brief` — Morning briefing after an autonomous run changelog and next steps
- `task-observer` — Monitors task execution for skill-improvement opportunities
- `handoff` — Compact the current conversation into a handoff document
- `teach` — Teach the user a new skill or concept

## Git & shipping

- `branch` — Create a new git branch from main and enter an isolated worktree
- `ship` — Stage, commit, push, and open a PR in one command
- `resolving-merge-conflicts` — Resolve an in-progress git merge/rebase conflict
- `git-guardrails-claude-code` — Hooks that block dangerous git commands before execution

## Apps & clients

- `new-client-repo` — Create a new bcns client repo from the template
- `leads` — Find, score, and track bcns sales leads in the Master Client List sheet
- `career-advisor` — Senior career advisor reviewing portfolio sites and writeups

## Utilities

- `find-skills` — Discover and install agent skills
- `tidy-downloads` — Sort a messy folder into meaningful subfolders

## Installed elsewhere — not in this repo

Third-party tooling is installed, never vendored: this repo is **public**, and a
committed copy forks a package we don't maintain. Both reinstall from their source.

| Tool | Installs as | Lives at | Why not here |
|---|---|---|---|
| **Impeccable** | plugin | `~/.claude/plugins/cache/impeccable/impeccable/<ver>/` | Plugins aren't symlinked into `~/os`, so it never lands here. Ships 4 agents + a `hooks.json` a plain skill folder can't. |
| **Higgsfield** | skills | `skills/higgsfield-*/` — **gitignored** | `~/.claude/skills` symlinks to `skills/`, so these land physically in this repo by accident of the symlink. Marketplace-managed and versioned; committing them forks them. |

Both are consumed by the `design` skill — see `skills/design/SKILL.md` for how.
Impeccable's `hooks.json` is active **plugin-wide**: it runs `detect.mjs` on every
`Edit`/`Write` and a deep pass at `Stop`, in every repo, whether or not `design` is running.
