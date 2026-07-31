---
name: feedback-reference-file-density
description: "Files an agent reads per-item (convergence-loop.md, agent defs) carry rules only — no rationale prose; check net word count after editing them"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7f662ac0-14a8-42ba-b258-8163781f1e42
  modified: 2026-07-31T22:54:12.554Z
---

In files that get re-read on every item or every spawn — `convergence-loop.md`,
`agent-glossary.md`, the `dt-*` agent definitions — write the rule, not the
argument for it. Nate cut a token-efficiency edit of mine for exactly this:
"we dont need all the verbose explanation of why we are making these decisions."

**Why:** these files are a recurring per-item input cost. Explanatory prose that
reads well once is paid for on every item of every run. A 300-word rationale
block in `convergence-loop.md` is charged ~10× in a 10-item autonomous run.

**How to apply:** after editing any per-item reference file, run `wc -w` and
compare to the original — if a token-efficiency change grew the file, it hasn't
netted out yet. Keep one clause of "why" only where it changes a routing call
(e.g. "a false PASS is the failure the gate exists to prevent"). Put the mechanic
in exactly one section and route to it from elsewhere in a line, rather than
restating it. When a rule genuinely needs length, the fix is splitting the file
so each reader loads only what it executes — not compressing the conditionals,
which are what keep teams small.

Related: [[feedback-proactive-token-efficiency]] · [[dev-team-learnings]]
