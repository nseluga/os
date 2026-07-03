# library — reference source material (local-only)

Documents Claude should **read closely** to accomplish a task: research
articles, papers, specs, PDFs, long-form reading — anything worth citing or
understanding in depth rather than just remembering a one-line fact about.

This is *optional context*. Nothing here loads automatically. It gets pulled in
only when a task explicitly points at it (or when the topic obviously matches).
Think of it as a bookshelf, not a briefing.

## ⚠️ These documents are NOT committed to git

This repo is **public**, and reading material is often copyrighted. So the
actual document files live **local-only**: `.gitignore` excludes everything
under `library/` *except* markdown (`README.md`, `NOTES.md`) and `.gitkeep`.
That means:

- Drop a PDF here and it just works locally — git ignores it, no risk of
  pushing a copyrighted paper to a public repo.
- The folder **structure** and your **notes** (`NOTES.md`) still get committed,
  so the shape of your library and why-it's-here context is versioned.
- Trade-off: the files themselves are **not backed up by GitHub** and **don't
  travel** to other clones or cloud agents. Make sure they're covered by Time
  Machine / iCloud if they matter. (If you ever want them versioned + backed up,
  make the repo private and delete the `knowledge/library` rules in
  `../../.gitignore`.)

## How it relates to the rest of `knowledge/`

- **`library/`** (here) — full source documents to read on demand. Nouns you
  study. Files local-only; notes committed.
- **`memory/`** — distilled one-line facts Claude manages automatically.
- **`me/`, `frameworks/`, `audience/`** — hand-written durable notes.
- **`raw/`** — unprocessed inbox for *notes/dumps* to triage.

If you extract a durable takeaway from a document here, write it into `memory/`
or `frameworks/` (those are committed) and leave the source file in place for
re-reading.

## Layout

Group by topic. One folder per subject; drop the file(s) in, optionally with a
`NOTES.md` capturing what matters and why you keep it.

```
library/
├── _inbox/                     # unsorted drops — triage into a topic folder
├── pitching-biomechanics/
│   ├── fleisig-2009-kinetics.pdf   # local-only (gitignored)
│   └── NOTES.md                    # committed: summary, why it's here, key pages
└── shot-value-models/
    └── some-paper.pdf              # local-only (gitignored)
```

Naming: `author-year-topic.pdf` (e.g. `fleisig-2009-kinetics.pdf`) keeps files
sortable and citable. Keep the original title in `NOTES.md` if you rename.

## How to reference it in a task

Just point at the path:

> "Read `knowledge/library/pitching-biomechanics/fleisig-2009-kinetics.pdf`
> before working on the injury-risk features."

Claude Code's Read tool opens PDFs directly (paged), so no conversion needed.

## Adding a document

1. Drop the file in `_inbox/` (or straight into a topic folder if you know it).
   It's ignored by git automatically — nothing to configure.
2. Optionally add/append a `NOTES.md` with a one-line why-it's-here. That file
   *does* get committed, so it's your public-safe index of what's on the shelf.
3. `git add` picks up only the markdown/structure; the documents stay local.
