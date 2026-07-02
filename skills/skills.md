---
name: skill-name-in-kebab-case
description: One sentence — what it does + when to use it. This is the ONLY text Claude sees when deciding whether to invoke the skill, so lead with trigger conditions ("Use when the user...").
---

# <Skill Title>

<!--
TEMPLATE — copy this file to start a new skill.

  cp skills.md <skill-name>/SKILL.md

Then fill in every section and delete these comments. Rules that make a
skill discoverable and useful:

- The folder name, the `name:` field, and the invocation all must match.
- `description:` is a router prompt, not documentation. Put the trigger
  ("Use when...", "...or when the user mentions X") first. Be specific about
  the words/situations that should fire it.
- Keep the body imperative and short. It's instructions to a model, not prose
  for a human. Ordered steps beat paragraphs.
-->

## When to use

- Trigger phrases: "...", "..."
- Situations: <what state the user/repo is in when this applies>
- Do NOT use when: <the near-miss cases this should not fire on>

## What it does

One-paragraph summary of the outcome this skill produces.

## Steps

1. <first action — usually gather/inspect before changing anything>
2. <...>
3. <verify the result and report back>

## Inputs / arguments

- `$ARGUMENTS` — <what the user can pass and how it's interpreted>

## Examples

- Input: `<what the user says>` → <what the skill does>

## Notes & gotchas

- <edge cases, things to avoid, dependencies on other skills>
