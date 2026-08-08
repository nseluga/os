---
name: explain
description: Re-explain Claude's last response in ASD-STE100 Simplified Technical English, using Nate's own os vocabulary (skill, hook, subagent, LANE.md, dev-team, worktree, memory file) as the defined names for things instead of paraphrasing them away. Use when the user says "/explain", "explain that simply", "say that in plain English", "ASD-STE me that", or otherwise asks for the prior response restated more simply.
---

# Explain

Rewrite Claude's immediately preceding response — never new research or new claims — under two rules at once.

## Rules

1. Apply ASD-STE100. One idea per sentence, ~20 words max, active voice, present tense, the same word for the same concept every time.
2. Keep Nate's os terms as the defined names for things: skill, subagent, hook, LANE.md, MAP.md, dev-team, worktree, memory file, `~/os`. Define each on its first use in one short clause. Nate is building fluency on these terms (per `user-learning-claude-code` memory) — a generic paraphrase costs him the word he needs, even when it reads simpler.

## Examples

- Wrong (paraphrases the term away): "This adds a background task that runs by itself when something happens."
- Right (keeps the term, glosses it once): "This adds a hook. A hook is a script the harness runs on its own at one event."
- Wrong: "A small helper process did the file search for you."
- Right: "A subagent did the file search. A subagent is a separate Claude instance you dispatch for one task."

## Process

1. List each claim in the prior response.
2. Rewrite each claim as one short, active sentence.
3. Check every sentence: under ~20 words, and no concept has two different names.
4. Build a visualization per the criteria below and publish it with `Artifact` (load `artifact-diagramming` first). Skip only if no rule below finds a fit.
5. Output the rewrite, then the artifact link — no meta-commentary about the rewrite or the diagram itself.

## Visualization criteria

Weigh these against the content each time — don't pick a diagram type first. Apply whichever fits, more than one if more than one fits, none if none do:

- **Hardest-to-say fact** — find the one thing prose fumbles (hidden order, race, threshold) and draw only that.
- **Wrong picture already in their head** — if a plausible wrong mental model exists, draw it crossed out next to the real shape.
- **Boundary, not the typical case** — draw the transition/edge, skip the normal behavior on either side.
- **Branch point** — if the content hinges on a condition, draw the fork once: input, test, the two outcomes.

## Do not use when

The user is asking for new information, new work, or an answer to a new question — not a restatement of what Claude already said.
