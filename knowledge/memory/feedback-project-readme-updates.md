---
name: project-readme-updates
description: After a work session lands a meaningful change in a project, offer to update that project's os/projects README (last_active, next_step, status) in the canonical _TEMPLATE.md shape
metadata:
  type: feedback
---

After a work session lands a meaningful change in a project repo, offer to update that project's index at `~/os/projects/<id>/README.md` — bump `last_active`, refresh `next_step`, and adjust `status`/`priority` only if a phase boundary moved. Keep the file in the canonical shape defined by `~/os/projects/_TEMPLATE.md`: machine-parseable YAML frontmatter (read by the project-dashboard) + a lean body (**Where it stands** / **Run · verify** / **Key files**). Detailed history and task lists stay in the repo's local, gitignored `PLAN.md`/`PROGRESS.md` — never the README.

**Why:** The daily "Daily OS Synthesis" cloud routine was retired (disabled) 2026-07-11 — a cloud agent can't see gitignored `PLAN.md`/`PROGRESS.md` or repos that aren't on GitHub, so it couldn't reliably keep the READMEs current. README upkeep is now manual, so Claude offering it after a session is what keeps the project-dashboard accurate.

**How to apply:** Offer, don't auto-write — one line at the end of the turn. Only for significant changes: a shipped feature, resolved blocker, phase boundary, or changed next step. Skip routine WIP and pure exploration. Match the repo against the `repo:` field in each `~/os/projects/*/README.md`.
