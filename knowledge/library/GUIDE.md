# library/ — guide (policies & workflow)

Documents Claude should **read closely** to accomplish a task: research
articles, papers, specs, PDFs, long-form reading — anything worth citing or
understanding in depth rather than just remembering a one-line fact about.

This is *optional context*. Nothing here loads automatically. It gets pulled in
only when a task explicitly points at it (or when the topic obviously matches).
Think of it as a bookshelf, not a briefing.

## ⚠️ Nothing here is committed to git except this guide

This repo is **public**, and library contents are personal — reading material
is often copyrighted, and notes are specific to whoever's using this `os`. So
everything under `library/` lives **local-only**: `.gitignore` excludes it all
except this `GUIDE.md`. That means:

- Drop a PDF or write a topic note here and it just works locally — git
  ignores it, no risk of pushing copyrighted or personal material to a public
  repo.
- Trade-off: nothing here is **backed up by GitHub** or **travels** to other
  clones or cloud agents. Make sure it's covered by Time Machine / iCloud if it
  matters. (If you want library contents versioned + backed up, make the repo
  private and delete the `knowledge/library` rules in `../../.gitignore`.)

## How it relates to the rest of `knowledge/`

- **`library/`** (here) — full source documents to read on demand. Nouns you
  study. Local-only, including your notes.
- **`memory/`** — distilled one-line facts Claude manages automatically.
- **`me/`, `frameworks/`, `audience/`** — hand-written durable notes. (`me/`
  and `audience/` are local-only too; `frameworks/` is committed.)
- **`raw/`** — unprocessed inbox for *notes/dumps* to triage.

If you extract a durable takeaway from a document here, write it into `memory/`
or `frameworks/` (those are committed) and leave the source file in place for
re-reading.

Folder contents and layout: see [INDEX.md](INDEX.md).

## How to reference it in a task

Just point at the path:

> "Read `knowledge/library/baseball-research/heaton-2022-player-form-embeddings.pdf`
> before working on the form-embedding features."

The `.md` notes files are designed to be read instead of the PDF when you need
a quick orientation; point at the PDF when you need full detail.

Claude Code's Read tool opens PDFs directly (paged), so no conversion needed.

## Adding a document

1. Drop the file in `_inbox/` (or straight into a topic folder if you know it).
   It's ignored by git automatically — nothing to configure.
2. Add a matching `author-year-topic.md` with: questions answered, model/method
   summary, baseball insights, and a "why it's on the shelf" note pointing at
   specific reuse value. This stays local too — it's your personal shelf.
3. Update the layout tree in `INDEX.md` to include the new entry.
4. Nothing here needs `git add` — the whole folder is ignored except this
   guide.
