# raw/ — index

Inbox for unprocessed material: dumps, clippings, snippets, half-formed notes.
Capture first, sort later — items get triaged into `me/`, `frameworks/`,
`audience/`, `library/`, or a project, or deleted. Don't rely on anything
here being organized or final.

Processing: run `/ingest-data` to triage everything into its destination and
clear the folder. Contents are transient — no per-file index is kept
(deliberate exception to the CLAUDE.md index-maintenance rule).

**Exception — design reference images.** Image files here (`*.png/jpg/gif/webp/mp4`) are
design references awaiting a clustering session; `/ingest-data` leaves them in place rather
than filing them, because naming a style is a judgment call made against the whole corpus.
They are **gitignored** (this repo is public and they are third-party work). `sources.md`
maps each file to its source URL and IS tracked. Both get cleared once the extraction
session files them into `library/design-language/styles/<name>/`.
