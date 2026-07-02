---
name: feedback-surface-tradeoffs-proactively
description: Always include tradeoffs when recommending a configuration change — user asked "are there any drawbacks?" before approving a CLAUDE.md + hook recommendation.
metadata:
  type: feedback
---

When recommending any configuration change (CLAUDE.md rules, hooks, settings, skills), include the tradeoffs in the same message — don't wait to be asked.

**Why:** User asked "are there any drawbacks to adding in both of those features?" before approving the efficiency rules + hook approach. This is a good instinct; I should anticipate it rather than surface tradeoffs only on request.

**How to apply:** After any recommendation involving a file change or system configuration, add a brief "tradeoffs" note covering: what could misfire, what legitimate use cases might be blocked, and the maintenance cost. Keep it short — one sentence per risk is enough.
