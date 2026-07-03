# library — reference source material

Documents Claude should **read closely** to accomplish a task: research
articles, papers, specs, PDFs, long-form reading — anything worth citing or
understanding in depth rather than just remembering a one-line fact about.

This is *optional context*. Nothing here loads automatically. It gets pulled in
only when a task explicitly points at it (or when the topic obviously matches).
Think of it as a bookshelf, not a briefing.

## How it relates to the rest of `knowledge/`

- **`library/`** (here) — full source documents to read on demand. Nouns you
  study.
- **`memory/`** — distilled one-line facts Claude manages automatically.
- **`me/`, `frameworks/`, `audience/`** — hand-written durable notes.
- **`raw/`** — unprocessed inbox for *notes/dumps* to triage.

If you find yourself extracting a durable takeaway from a document here, write
the takeaway into `memory/` or `frameworks/` and leave the source PDF in place
for re-reading.

## Layout

Group by topic. One folder per subject; drop the file(s) in, optionally with a
`NOTES.md` capturing what matters and why you keep it.

```
library/
├── _inbox/                     # unsorted drops — triage into a topic folder
├── pitching-biomechanics/
│   ├── fleisig-2009-kinetics.pdf
│   └── NOTES.md                # optional: summary, why it's here, key pages
└── shot-value-models/
    └── some-paper.pdf
```

Naming: `author-year-topic.pdf` (e.g. `fleisig-2009-kinetics.pdf`) keeps files
sortable and citable. Keep the original title in `NOTES.md` if you rename.

## How to reference it in a task

Just point at the path:

> "Read `knowledge/library/pitching-biomechanics/fleisig-2009-kinetics.pdf`
> before working on the injury-risk features."

Claude Code's Read tool opens PDFs directly (paged), so no conversion needed.

## Adding a document

1. Drop the PDF in `_inbox/` (or straight into a topic folder if you know it).
2. Optionally add/append `NOTES.md` with a one-line why-it's-here.
3. `git add` + commit. Commit binaries like any other file.

## Size & Git LFS (upgrade path)

Plain Git is fine for a growing collection of articles — a few hundred small-to-
medium PDFs is nothing. The only cost case is **repeatedly replacing large
files**, since Git keeps every version in full.

If this library ever gets heavy (many big PDFs, or files you revise often),
switch it to **Git LFS** so the repo stays lean:

```
brew install git-lfs
cd ~/os && git lfs install
git lfs track "knowledge/library/**/*.pdf"
git add .gitattributes && git commit -m "track library PDFs with LFS"
```

Existing PDFs already committed can be migrated with `git lfs migrate import`.
Not needed today — noted so future-you knows the lever exists.
