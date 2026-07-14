# Memory Index

- [User profile](user-profile.md) — Nate Seluga, junior CS at Harvey Mudd (Class of 2027), targeting software/ML engineering, data science, or MLB analytics roles
- [Explain concepts plainly](feedback-explain-concepts-plainly.md) — Lead with plain English when introducing Claude Code workflow concepts; user asked "what do these mean?" after a rules cheat sheet
- [Surface tradeoffs proactively](feedback-surface-tradeoffs-proactively.md) — Include risks/tradeoffs with any config recommendation; user had to ask "are there drawbacks?" before I volunteered them
- [Recommendations with model/effort](feedback_recommendations_with_model_effort.md) — When presenting options, include model + effort + token reasoning to help Nate make informed calls on whether to pursue an approach
- [User is learning Claude Code tooling](user-learning-claude-code.md) — Peer-level on the codebase, but building fluency on hooks/skills/agents/memory — explain those as new unless shown otherwise
- [Library notes format](feedback-library-notes-format.md) — one file per document, never a combined NOTES.md; never write stubs before reading the source
- [Proactive token efficiency](feedback-proactive-token-efficiency.md) — apply the efficiency playbook (Read-over-Bash, no re-reads, right-sized models, batching, delegation) automatically, without being reminded
- [Portfolio style guide](reference-portfolio-style-guide.md) — `~/os/knowledge/library/style_reference/Project_Writeup.pdf`; specific/evidence-driven voice, no marketing language — read before any portfolio writing
- [Tool-building efficiency principle](feedback_tool_building_efficiency.md) — Tier by need, gate on explicit signals, cheap models for mechanical/read-only only; reasoning roles need Sonnet+. Proactive fan-out only beats reactive when wrong-first-approach cost > fan-out cost.
- [Dev-team process learnings](dev-team-learnings.md) — Generalizable /dev-team + /dev-team-auto lessons: regex position assumptions, EMPTY_MANUAL mutation, mutex scope, color sweep test hygiene, focus ring contrast, word-boundary matching, shared readManual() pattern; `--bare` kills Skill tool; headless tasks must be pure unit tests
- [os-evals standards](project-os-evals-standards.md) — Two-sided check validation gate, exit code convention (1=fail, 2=infra), and 2026-07-09 eval result verdict
- [Offer README updates post-session](feedback-project-readme-updates.md) — after a meaningful change, offer to update the project's os README to the `projects/_TEMPLATE.md` shape; daily synthesis cloud routine retired 2026-07-11
- [Claude-in-Chrome limits](reference-claude-in-chrome-limits.md) — extension only sees tabs in its own window (drag tabs in); `file://` URLs blocked (use python3 http.server instead)
