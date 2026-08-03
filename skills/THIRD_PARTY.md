# Third-party skills

Not written by Nate. Kept here (tracked, not gitignored) for reproducibility, credited below.
Deliberately not referenced from any `SKILL.md` — this file is for humans browsing the repo, not for Claude to load.

| Skill | Source | Notes |
|---|---|---|
| `higgsfield-generate` | Higgsfield marketplace plugin | Installed via the Higgsfield Claude Code marketplace. |
| `higgsfield-marketplace-cards` | Higgsfield marketplace plugin | Installed via the Higgsfield Claude Code marketplace. |
| `higgsfield-product-photoshoot` | Higgsfield marketplace plugin | Installed via the Higgsfield Claude Code marketplace. |
| `prototype` | [mattpocock/skills](https://github.com/mattpocock/skills) | Vendored via `npx skills add mattpocock/skills --skill=prototype`. |
| `humanizer` | [blader/humanizer](https://github.com/blader/humanizer) (MIT) | Full SKILL.md copied by hand, not vendored via a tool; Voice Calibration section extended to default to `style_reference/`. |
| `find-skills` | [vercel-labs/skills](https://github.com/vercel-labs/skills) | Discovery/installer front-end for the `npx skills` CLI and the open agent-skills ecosystem. |
| `git-guardrails-claude-code` | [mattpocock/skills](https://github.com/mattpocock/skills) | One-time `PreToolUse` hook installer blocking destructive git commands (push, reset --hard, clean -f, branch -D, checkout .). |
