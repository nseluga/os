---
name: dev-team-learnings
description: "Generalizable /dev-team + /dev-team-auto process learnings — orchestration, track/model, QA/test, and review patterns that apply across any repo"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7037cedd-2c09-4470-a67b-fc6af17b22bb
---

Cross-project lessons from dev-team runs. Project-specific findings stay in each repo's `.claude/dev-team/team-memory.md`.

- 2026-07-09 When a change adds `<details>/<summary>` elements inside repeating components (cards), pre-existing tests that use first-match regex for `<details>` will silently match the wrong element — **Why:** regex position assumptions break when more elements of the same type are added. **How to apply:** fixture tests involving HTML elements that may appear multiple times (details, button, summary) should match by content (e.g. "Completed" text, aria-label) rather than by DOM position.

- 2026-07-09 `readManual()` must use explicit per-field construction — never `{ ...EMPTY_MANUAL, ...parsed }` — **Why:** shallow spread returns references to the constant's nested objects; callers that mutate those objects (e.g. `manual.hidden_fields[id][field] = true`) poison `EMPTY_MANUAL` for all subsequent calls in the same process, causing hard-to-reproduce state bleed. **How to apply:** always construct `{ field1: {...(parsed.field1 ?? {})}, field2: [...(parsed.field2 ?? [])], ... }` explicitly. Any new field added to the data model must be added to this construction simultaneously.

- 2026-07-09 Expensive I/O (git shell calls via getMergedProjects/getProjects, disk reads) must never run inside a write mutex — **Why:** the lock serializes all concurrent requests for the full duration of the slowest call; a git subprocess can take seconds. **How to apply:** resolve any external data (project list, git log) before `runExclusive`; the mutex should protect only the read-modify-write step on the shared file.

- 2026-07-09 Before a color palette sweep, audit test files for color-anchored assertions (`/text-gray-/`, `/text-blue-/`, etc.) and update them in the same commit as the sweep — **Why:** the sweep will break those assertions, and the fix-as-follow-up burns an extra QA attempt. **How to apply:** run `grep -r 'text-gray-\|text-blue-' tests/` before executing the sweep; patch the assertions alongside the component changes.

- 2026-07-09 `focus-visible:ring-*` on filled colored buttons must use a white ring with offset, not a lighter tint of the button color — **Why:** `ring-indigo-400` on `bg-indigo-600` achieves ~2.4:1 contrast, below the WCAG 3:1 minimum for non-text UI components. **How to apply:** use `focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[button-color]` on any filled-color button.

- 2026-07-09 Keyword-matching functions (autoTag, search, filter) must use word-boundary checks, not bare `indexOf` — **Why:** substring matches cause false positives ("os" matches inside "gross", "ml" inside "email", "ai" inside "said"). **How to apply:** implement `isWordBoundary(text, start, end)` checking `\W` or string edge on both sides of the match; never ship a keyword scanner that uses only `indexOf`.

- 2026-07-09 When composed SSR pages need both getMergedProjects() output AND raw manual data (token_log, notes, etc.), use an optional `manual?` parameter on getMergedProjects() to share a single disk read — **Why:** without this, getMergedProjects() calls readManual() internally while the page also calls it directly, doubling disk I/O per render. **How to apply:** `const manual = await readManual(); const projects = await getMergedProjects(manual);` — one read, zero redundancy.
