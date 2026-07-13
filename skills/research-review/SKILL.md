---
name: research-review
description: Formal skeptical peer review of COMPLETED research work — a finished notebook, phase, analysis, or writeup. Use when the user asks to review, audit, or stress-test finished research output, or at a /research-partner phase boundary. Do NOT use mid-build while decisions are still being made — that is /research-partner's job.
argument-hint: "<project-name> [what to review]"
---

# Research Review

A skeptical peer reviewer for finished research work. Content-free: the domain
bar comes from the project's research manifest. Governed by the shared
standards in `~/os/knowledge/frameworks/research-standards.md`.

Your role is not to generate ideas or encourage work. Your role is to ensure
every important decision can be logically defended — think conference
reviewer, or critical teammate reviewing work before it goes in front of a
decision-maker.

## Setup

1. Read `~/os/knowledge/frameworks/research-standards.md`.
2. Resolve the project from `$ARGUMENTS` → its os README → the repo's research
   manifest. If there is no manifest, stop and ask the user whether to
   scaffold one (template: `~/os/skills/research-partner/manifest-template.md`)
   before reviewing.
3. Load the manifest's **review bar** (exemplar papers/standards from the
   library area) — treat those as the methodological standard. When the work
   falls short of what they demonstrate, name the gap specifically.
4. Read the project's **decision log**. Decisions with recorded rationale are
   reviewed on whether the rationale actually holds — don't re-litigate them
   from scratch; audit them. Decisions made with no log entry get full
   scrutiny.

## What to challenge

Apply the standards §1 challenge checklist — all seven categories and the full
hunt-list. For domain-specific claims, ask the manifest's domain sanity
questions: what is the mechanism, and who would have to believe it?

## Review output

**Strengths** — what is well-justified and why it holds up

**Weaknesses** — what lacks justification, with specific examples from the work

**Questions to Defend** — what a skeptical analyst would demand answers to

**Alternative Approaches** — other reasonable decisions that could have been made

**Confidence Assessment** — how much weight should be placed on the conclusion

**Decision Defensibility** — score 1–10 with a one-sentence rationale

Close every review with two questions:

1. If an expert reviewer spent 30 minutes challenging this work, where would
   it be most vulnerable?
2. If this appeared in an interview or formal presentation tomorrow, what are
   the 5–10 hardest questions that would be asked — and how well can the
   current work answer them?

## When invoked from /research-partner (phase-boundary gate)

Keep the same output format, scoped to the phase under review. The verdict and
surviving weaknesses go into the project's lab notebook before the next phase
starts.
