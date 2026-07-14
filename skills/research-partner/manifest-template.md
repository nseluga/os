# Research Manifest — <project name>

<!--
Copy this file to <project-repo>/docs/research-manifest.md and fill it in.
It lives in the PROJECT repo (not os) so its paths stay relative and it
travels with the code. Add one pointer line to the project's os README:
"Research manifest: <repo>/docs/research-manifest.md".

Both /research-partner and /research-review require this file and stop to
ask before working without it.
-->

## Architecture file
<!-- The single canonical architecture/design spec for this project, if one
     exists (usually in ~/os/knowledge/library/<area>/). Read at the start of
     every /research-partner session alongside the decision log and notebook
     — it's what "the plan" means when the partner references it. Omit this
     section if the project has no standalone architecture doc. -->
- `<path>` — <what it governs>

## Authority documents
<!-- Other canonical specs (handoff docs, framing docs, etc.) beyond the
     architecture file above. Repo-relative or absolute paths, one per line,
     with a one-phrase note on what each governs. -->
- `<path>` — <what it governs>

## Frozen rules
<!-- The project's non-negotiables. Violating one is automatically Tier 1
     (BLOCK) under research-standards §2. Copy them here verbatim or link the
     authority-doc section that holds them. -->
1. <rule>

## Decision log
<!-- Append-only, format per research-standards §4. -->
- Path: `docs/decision-log.md`

## Lab notebook
<!-- One entry per session, format per research-standards §5. -->
- Path: `docs/lab-notebook.md`

## Library area
<!-- Where processed reference notes live; cited library-first per
     research-standards §3. New findings get added here. -->
- Path: `~/os/knowledge/library/<area>/`

## Domain sanity questions
<!-- The checklist-category-6 questions for this domain: who has to believe a
     result for it to be credible, and what would they ask? -->
- <question>

## Review bar
<!-- What "methodologically sound" means here: the exemplar papers or
     standards /research-review should treat as the bar. -->
- <exemplars / standards>
