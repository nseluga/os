---
name: tool-building-efficiency-without-sacrifice
description: "Design principle for building Claude Code skills and agents — tier by actual need, gate expansions on explicit signals, cheap models for mechanical work, expensive models only where reasoning quality matters."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 90dec3f5-acd8-43d9-af86-3ce0e6bea0b6
---

When building or improving skills, agents, or orchestration tools, apply this efficiency-without-sacrifice principle:

**Tier by actual need, not by worst case.** Default to the cheap/fast path; escalate only when a concrete signal justifies it. Never apply the heavy treatment uniformly just because some items warrant it.

**Cheap models belong on mechanical work only.** Fan-out with Haiku/cheap models for read-only, mechanical tasks (search, grep, trace, gather). QA, engineering, design, and reasoning roles require Sonnet+; cheap models produce shallow output that degrades effectiveness there.

**Gate expansions on explicit, narrow signals.** Broader triggers (content heuristics, size proxies) fire too often and add cost without proportional gain. Prefer explicit author intent (like `flag:`) or unambiguous structural signals over fuzzy inference.

**Proactive fan-out only where it's cheaper than reactive.** The convergence loop's reactive alt-branch fork already handles design failures. Front-loading parallel exploration only pays off where the cost of a wrong first approach exceeds the fan-out cost — i.e., genuinely uncertain architecture on high-risk items, not every full-track item.

**Align selection criteria with the review stage.** When picking a winning design/approach, use the same axes the Optimization Reviewer uses (efficiency, reliability, scalability) so the chosen path is already optimized for the quality gate it will face.

**Why:** Emerged from assessing whether dt-analyze, dt-engineer, dt-qa, and dt-fix should adopt parallel cheap-model subagents. The analysis showed this is the right move only for the read-only analysis role and only for large/unfamiliar areas; everywhere else it multiplies cost without improving outcomes.

**How to apply:** Before adding any fan-out, subagent team, or model escalation to a skill: (1) identify whether the work is read-only/mechanical or reasoning-heavy, (2) confirm the trigger is narrow and explicit rather than broad/inferred, (3) verify the expansion can't be deferred until failure is proven.
