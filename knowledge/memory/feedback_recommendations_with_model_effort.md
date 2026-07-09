---
name: feedback_recommendations_with_model_effort
description: When giving options with tradeoffs, include model and effort recommendations with brief reasoning
metadata:
  type: feedback
---

When presenting options or recommendations to the user (especially in exploratory contexts like "what could we do about X?" or "how should we approach this?"), always include:

1. **Model recommendation** — which Claude model makes sense (Haiku for quick reads, Sonnet for balanced work, Opus for complex reasoning/multi-step). Include why.
2. **Effort recommendation** — rough estimate of work involved (quick, medium, high). Include why.
3. **Brief reasoning** — explain the why in terms of **effective and quality task completion and tokens** (not generic praise).

**Why:** Helps Nate make fast, informed decisions about whether to pursue an approach and how to resource it. Knowing the token/cost/speed tradeoff upfront prevents wasted exploration.

**How to apply:** When you find yourself presenting 2-3 options with tradeoffs, add a one-line summary for each that includes model + effort + token reasoning before asking what the user prefers.
