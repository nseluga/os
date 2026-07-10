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
under `library/` *except* markdown (`.md` files) and `.gitkeep`. That means:

- Drop a PDF here and it just works locally — git ignores it, no risk of
  pushing a copyrighted paper to a public repo.
- The folder **structure** and your **notes** (`.md` files) still get
  committed, so the shape of your library and why-it's-here context is
  versioned.
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

Group by topic. One folder per subject. Each paper gets its own `.md` notes
file named to match the PDF (`author-year-topic.md`).

```
library/
├── _inbox/                                   # unsorted drops — triage into a topic folder
├── style_reference/                          # Nate's voice and writing style (see README.md inside)
│   ├── README.md                                  # how to use this folder — read first
│   ├── Project_Writeup.pdf                        # local-only (gitignored); structural/rhythm ref
│   ├── seluga-project-writeup.md                  # notes: style standards, evidence-driven voice
│   ├── Seluga Final Paper.pdf                     # local-only (gitignored); rhythm + transitions ref
│   ├── seluga-final-paper.md                      # notes: sentence rhythm, word choices, structure
│   └── seluga-personal-[description].*            # voice calibration examples (add as available)
└── baseball-research/
    ├── alcorn-2018-batter-pitcher2vec.pdf         # local-only (gitignored)
    ├── alcorn-2018-batter-pitcher2vec.md          # committed: questions, model, insights
    ├── heaton-2022-player-form-embeddings.pdf
    ├── heaton-2022-player-form-embeddings.md
    ├── heaton-2023-contextual-event-embeddings.pdf
    ├── heaton-2023-contextual-event-embeddings.md
    ├── melville-2023-game-theory-pitch-sequencing.pdf
    ├── melville-2023-game-theory-pitch-sequencing.md
    ├── melville-2024-fielder-positioning.pdf
    ├── melville-2024-fielder-positioning.md
    ├── anon-2025-ai-manager-strategies.pdf
    ├── anon-2025-ai-manager-strategies.md
    ├── anon-2025-transformer-pitch-outcome.pdf
    └── anon-2025-transformer-pitch-outcome.md
```

Naming: `author-year-topic.pdf` / `.md` (e.g. `heaton-2022-player-form-embeddings.pdf`)
keeps files sortable and citable. Keep the original title as the H1 of the notes file.

Each notes file follows the same structure: questions answered, models used,
methodology notes, baseball insights, and a "why it's on the shelf" section
pointing at specific reuse value. Notes cross-link with `[[slug]]` wikilinks.

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
   specific reuse value. That file *does* get committed.
3. Update this README's layout tree to include the new entry.
4. `git add` picks up only the markdown; the documents stay local.
