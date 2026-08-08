---
name: feedback-surface-tradeoffs-proactively
description: "Recommending a CLAUDE.md rule, hook, or config/settings.json change — volunteer tradeoffs/drawbacks/downsides unprompted; user asked \"are there any drawbacks?\" before approving a CLAUDE.md + hook recommendation."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b6c8cfb8-4271-4741-aa9a-6b404592d0b3
  modified: 2026-08-08T17:16:20.415Z
---

When recommending any configuration change (CLAUDE.md rules, hooks, settings, skills), include the tradeoffs in the same message — don't wait to be asked.

**Why:** User asked "are there any drawbacks to adding in both of those features?" before approving the efficiency rules + hook approach. This is a good instinct; I should anticipate it rather than surface tradeoffs only on request.

**How to apply:** After any recommendation involving a file change or system configuration, add a brief "tradeoffs" note covering: what could misfire, what legitimate use cases might be blocked, and the maintenance cost. Keep it short — one sentence per risk is enough.
