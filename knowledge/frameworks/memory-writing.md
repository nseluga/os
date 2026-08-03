# Writing MEMORY.md index lines for the relevance hook

`~/.claude/memory-relevance-hook.py` runs on every prompt and keyword-matches
it against each `MEMORY.md` index line (title + hook text). A match surfaces
the file as a candidate for Claude to `Read`; no match means the fact stays
invisible until Claude happens to open the file some other way. The index
line's phrasing is the only thing standing between a fact and being found.

**Related:** [[lane-md]] and [[progress-md]] are the equivalent
phrasing-schema files for plan/progress work — this is that file for memory.

## The rule

Phrase the hook as **words a real future prompt would use**, not as a
summary of the file's content.

- Bad (content-summary): "When presenting options, include model + effort +
  token reasoning to help Nate make informed calls."
- Good (trigger-shaped): "recommend a model or effort level for a task —
  include reasoning, not just a pick."

The difference: the bad version describes *what the memory says*. The good
version uses the *concrete nouns/verbs a prompt asking for this would
contain* ("recommend", "model", "task") so the hook's plain keyword overlap
actually fires.

## Checklist when writing a hook line

1. Write the line, then ask: what would Nate actually type when this memory
   is relevant? Rephrase toward those words.
2. Prefer concrete terms over abstractions: project names, tool names, task
   verbs ("deploy", "recommend", "review") beat paraphrases ("infrastructure
   changes", "decision support", "config guidance").
3. Keep the one-line budget — this is a phrasing rule, not license to write
   longer lines. `MEMORY.md` is capped at 200 lines / 25KB by Claude Code
   itself; every entry competes for that space.
4. Avoid free-floating generic nouns. A line that lists many topics
   ("regex assumptions, mutex scope, word-boundary matching") leaks common
   words that collide with ordinary dev prompts — two such words are all it
   takes to false-positive. Keep the distinctive anchors (project/tool
   names), scope the rest under them.
5. After adding or editing a line, sanity-check it: add a natural-language
   prompt case to `~/.claude/memory-relevance-hook.test.py` (smoke) or
   `~/.claude/memory-relevance-hook.stress.test.py` (full — every entry,
   rank checks, adversarial negatives) and confirm it matches *and* that the
   negatives still stay silent.

## Why this file exists

Without it, index lines drift toward describing content (natural for a
human skimming) rather than triggering (necessary for the keyword-match
hook). The hook's precision is bounded by phrasing quality, not by the
matching algorithm — loosening the match threshold to compensate for vague
phrasing just reintroduces the noise/token-bloat problem the hook exists to
avoid. Fix the line, not the threshold.
