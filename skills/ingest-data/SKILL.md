---
name: ingest-data
description: Use when the user wants to process, sort, or triage files in knowledge/raw — distributes content to me/, frameworks/, audience/, library/, memory/, or a project index, then clears raw/. Triggers: "/ingest-data", "process my raw inbox", "sort raw", "triage knowledge/raw".
---

# ingest-data

**Related:** [[sources]]

Triage everything in `~/os/knowledge/raw/` and distribute it to the right destination. Leave raw/ empty (or containing only its README).

## When to use

- Trigger phrases: `/ingest-data`, "process my raw inbox", "sort raw", "triage knowledge/raw", "clean up raw"
- Situations: User has dropped files/notes into raw/ and wants them organized
- Do NOT use when: user wants to add a single specific memory (use memory tools directly)

## What it does

Reads every file in `knowledge/raw/` (skip README.md), classifies each by content, moves or merges it into the correct destination, then reports what went where.

## Destinations

| Content type | Where it goes |
|---|---|
| Facts about Nate — bio, preferences, goals, roles | `knowledge/me/README.md` (append/merge) |
| Reusable mental models, methods, decision frameworks | New file in `knowledge/frameworks/` |
| Notes on people/orgs Nate writes or builds for | `knowledge/audience/README.md` (append/merge) |
| Reference docs, specs, external material to keep | `knowledge/library/` (one file per doc) |
| Design reference images — Dribbble shots, screenshots of UI/sites/apps valued for how they look | **Leave in `knowledge/raw/`** — the one exception to clearing raw; see Notes |
| Persistent facts/preferences for Claude to recall | New memory file + MEMORY.md index line (follow memory format from CLAUDE.md) |
| Project-specific notes | Matching `projects/<name>/README.md` frontmatter or body |
| Clearly ephemeral / already stale | Delete with a note |

## Steps

1. **Inventory** — list all files in `~/os/knowledge/raw/` (skip README.md). If empty, report and stop.
2. **Read each file** in full.
3. **Classify** — pick the single best destination from the table above. When content spans two destinations, split it (e.g. a note that's half personal bio, half a framework gets written to both).
4. **Write/merge to destination** — for append targets (me/README.md, audience/README.md) integrate cleanly; don't duplicate existing content. For new files, pick a short descriptive name.
5. **Delete the raw file** after successful placement.
6. **Report** — one line per file: `<filename> → <destination>` (or `→ deleted`).

## Inputs / arguments

- `$ARGUMENTS` — optional filename(s) to process only specific files; omit to process everything in raw/

## Notes & gotchas

- Never delete `raw/README.md`
- If a file's destination is genuinely ambiguous, place it in `knowledge/library/` with a note and flag it to the user
- Memory writes must follow the two-step format (fact file + MEMORY.md index line) from CLAUDE.md
- Check for existing content before appending — don't duplicate facts already in me/README.md or audience/README.md
- For project routing, match against the `repo:` or `name:` field in `projects/*/README.md`
- Design reference images STAY in `raw/` until a clustering session files them into `library/inspiration/<look>/`. Do not move, rename, or delete them. They are the sole exception to "leave raw/ empty" — report them as awaiting clustering.
- Image files in `raw/` are gitignored (`.gitignore`: `knowledge/raw/**/*.png` etc.) because they are third-party work and this repo is public. Never remove those rules.
- Don't sort design images into `styles/<name>/` yourself — naming a style is a judgment call Nate makes against the whole corpus in a clustering/extraction session, not a per-file classification
- If an image's source URL is known, preserve it: append `<filename> — <url>` to `knowledge/raw/sources.md` (the style README schema requires a source URL per exemplar, and the URL is unrecoverable later)
