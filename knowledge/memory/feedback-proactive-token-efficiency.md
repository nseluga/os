---
name: feedback-proactive-token-efficiency
description: Nate wants token-efficient habits applied automatically, without being reminded each session
metadata:
  type: feedback
---

Nate cares about token efficiency and wants Claude to apply the efficiency playbook proactively — he should not have to ask for it each time. Audited his sessions and prescribed these habits, then asked to encode them so they happen automatically.

The habits, in his priority order:
- Use `Read`/`Grep` for viewing and searching files; reserve `Bash` for commands that actually run (git, tests, builds). His transcripts showed ~277 `cat`/`head`/`grep`-in-Bash substitutions.
- Don't re-read a file already in context unless it changed (he had files read 3–4×).
- Right-size the model: Sonnet by default, Opus only for reasoning/architecture/debugging, Haiku for lookups.
- Batch independent reads/greps into one turn instead of serial round-trips.
- Delegate noisy multi-file search to a subagent and keep only the findings.

**Why:** He explicitly optimizes for keeping effectiveness (~90–95%) while cutting token spend, and doesn't want to repeat the guidance.

**How to apply:** Default to these without narrating them. He values honest tradeoffs [[feedback-surface-tradeoffs-proactively]], so when an efficiency choice costs effectiveness, say so rather than silently optimizing.
