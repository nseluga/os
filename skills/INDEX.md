# skills/

One folder per skill. Each `SKILL.md`'s `description:` frontmatter is the canonical router text; this README is a human-browsable index. `skills.md` at this level is the template for new skills (see CLAUDE.md "Authoring a new skill").

## Dev team

- `design` — Interactive design skill: five drafts side by side, narrow to one, then tweak it live in the browser. Prompts with real reference images from `knowledge/library/inspiration/`; Impeccable's detector is the anti-slop floor. Ships `tweaks.js`, the in-page control panel.
- `dev-team` — Coordinates the dev team convergence loop for one plan item
- `dev-team-auto` — Autonomous dev team drives LANE.md items through convergence loop
- `dt-analyze` — Code Analyzer maps the codebase before other agents work
- `dt-engineer` — Engineer owns large-scale design and implements in worktree
- `dt-fix` — Bug Fixer applies reviewer findings and QA failures
- `dt-qa` — QA/Tester writes and runs the gating tests, emits PASS/FAIL
- `dt-research` — Researcher cache-first web research on current tools and frameworks
- `dt-review` — Optimization Reviewer efficiency, scalability, reliability, security findings
- `dt-ui` — UI Specialist frontend layout, hierarchy, responsiveness, accessibility

## Planning & review

- `lane` — Grill the user into a schema-valid LANE.md for dev-team execution (one lane, or a whole solo repo)
- `map` — Partition a repo into parallel lanes for a team; emit MAP.md + the foundation contract checklist
- `merge-lane` — Land a lane item on `integration`: overlap check, merge, archive progress, harvest memory, full suite
- `grill-me` — A relentless interview to sharpen a plan or design
- `research-partner` — Build-time research partner standup ritual, methods pushback
- `research-review` — Skeptical peer review of completed research work
- `ml-engineer` — ML engineering partner for technique selection and training code
- `storm-research` — 5-lens (practitioner/academic/skeptic/economist/historian) verified HTML research briefing

## os maintenance

- `improve-system` — Audit and improve the ~/os system: memory, skills, knowledge, projects, agents, link/index drift
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

## Apps & clients

- `new-client-repo` — Create a new bcns client repo from the template
- `leads` — Find, score, and track bcns sales leads in the Master Client List sheet
- `career-advisor` — Senior career advisor reviewing portfolio sites and writeups

## Utilities

- `tidy-downloads` — Sort a messy folder into meaningful subfolders
- `humanizer` — Strip AI-writing tells from text and match Nate's voice via `style_reference/`

## Installed elsewhere, vendored here

Impeccable stays uninstalled from this repo (a plugin, never symlinked in).
Higgsfield and `prototype` land physically here by accident of the
`~/.claude/skills` symlink; they're now tracked rather than gitignored so the
repo is reproducible as-run, with source credited in `THIRD_PARTY.md` — not
Nate's own work.

| Tool | Installs as | Lives at | Why not authored here |
|---|---|---|---|
| **Impeccable** | plugin | `~/.claude/plugins/cache/impeccable/impeccable/<ver>/` | Plugins aren't symlinked into `~/os`, so it never lands here. Ships 4 agents + a `hooks.json` a plain skill folder can't. |
| **Higgsfield** | skills | `skills/higgsfield-*/` | Marketplace-managed and versioned; reinstall via the Higgsfield marketplace to update. See `THIRD_PARTY.md`. |
| **prototype** (`mattpocock/skills`) | skill | `skills/prototype/` | Vendored via `npx skills add mattpocock/skills --skill=prototype`. Used by `lane`'s justification sweep to settle open design questions before the plan is written. See `THIRD_PARTY.md`. |

Both are consumed by the `design` skill — see `skills/design/SKILL.md` for how.
Impeccable's `hooks.json` is active **plugin-wide**: it runs `detect.mjs` on every
`Edit`/`Write` and a deep pass at `Stop`, in every repo, whether or not `design` is running.

- `higgsfield-generate` — Higgsfield image/video/3D/audio generation (vendored)
- `higgsfield-marketplace-cards` — Marketplace listing images and A+ content modules (vendored)
- `higgsfield-product-photoshoot` — Brand product photography sets (vendored)
- `prototype` — Throwaway prototype to settle a design question (vendored)
- `find-skills` — Discover and install agent skills (vendored, [vercel-labs/skills](https://github.com/vercel-labs/skills))
- `git-guardrails-claude-code` — Hooks that block dangerous git commands before execution (vendored, [mattpocock/skills](https://github.com/mattpocock/skills))
