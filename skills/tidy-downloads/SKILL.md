---
name: tidy-downloads
description: Intelligently sort a messy folder (default ~/Downloads) into meaningful subfolders. Claude skims the actual files, infers natural groupings, proposes a plan, then executes it through a safe move script that never deletes or overwrites and logs every move for one-command undo. Use when the user wants to clean up / organize Downloads (or another folder) and says things like "tidy my downloads", "organize this folder", "/tidy-downloads".
---

# Tidy Downloads — smart, reversible folder sorting

Sort a messy folder into meaningful subfolders using judgment about *what each
file actually is*, not just its extension. Claude does the thinking; a vetted
script does the moving. The script **never deletes, never overwrites**, and
records every move so any run can be undone with one command.

Default target is `~/Downloads`. If the user names another folder, use that as
`BASE` — but confirm first for anything outside Downloads/Desktop (higher stakes).

`SB="$HOME/os/skills/tidy-downloads/scripts"` — the three scripts live there.

## Procedure

### 1. Scan
Run `bash "$SB/scan.sh" [BASE]` to get a TSV inventory
(`name  type  ext  size_bytes  mtime_iso`). It already skips dotfiles,
in-progress downloads, bundles' internals, and the tool's own `_sorted`/`.tidy-undo`
dirs. Do **not** manually `ls` and start moving things — always work from the scan.

### 2. Understand what's there
Read the inventory. For files whose purpose is ambiguous from the name, look
closer before deciding — e.g. `head` a text/csv, check a PDF's name/size, note
screenshot naming patterns (`Screenshot 2026-...`), installers (`.dmg`, `.pkg`),
archives, media. **Find natural groupings from the actual contents** — this is the
point of using Claude instead of a dumb extension-sorter. Look for clusters:
recurring project names, course codes, a burst of screenshots, invoices/receipts,
resumes, datasets, installers already run.

Reuse folders that already exist in BASE rather than inventing near-duplicates
(if `Invoices/` exists, don't create `Receipts/`).

### 3. Propose a plan — and stop for approval
Present the proposed groupings to the user as a short table: destination folder,
which files go there, and a one-line rationale per group. Call out anything you're
unsure about and leave genuinely ambiguous files in place (don't force a home).
**Wait for the user to approve or adjust before moving anything.** This is a
direct-move tool — approval is the checkpoint that makes that safe.

### 4. Execute safely
Write the approved plan to a TSV — one line per file, `source_name<TAB>dest_subfolder`
(name only, no path; dest is a subfolder of BASE). Put it at
`"$BASE/.tidy-undo/plan-$(date +%s).tsv"`, then run:

```
bash "$SB/safe_move.sh" <plan.tsv> [BASE]
```

It creates destination folders, renames on collision (` (2)`, ` (3)`…) instead of
overwriting, skips missing/in-progress/protected entries, and writes an undo log
to `BASE/.tidy-undo/<timestamp>.tsv`. Report the moved/skipped counts and the log
path back to the user.

### 5. Offer undo
Tell the user they can reverse the entire run with:

```
bash "$SB/undo.sh"            # undoes the most recent run
bash "$SB/undo.sh <log.tsv>"  # undoes a specific run
```

## Hard rules
- **Never delete, never overwrite.** All moves go through `safe_move.sh`. Never
  call `rm`, and never `mv` files yourself outside the script.
- **Never recurse into bundles** (`.app`, `.rtfd`, `.bundle`, etc.) — treat each
  as a single item.
- **Never touch in-progress downloads** (`.crdownload`, `.part`, `.download`).
- **Approval gate is mandatory** for the first run and any time the plan touches
  something outside a clearly-safe category. When in doubt, leave it where it is.
- Keep the taxonomy shallow (one level of subfolders) unless the user asks for more.

## Making it recurring (optional)
This is intentionally a manual, present-while-it-runs tool — the safe default for
LLM-driven file moves. If the user later wants it scheduled, wrap the *approved,
stable* command in a macOS `launchd` job (local; won't run while the Mac is off or
asleep, and needs Full Disk Access granted to the runner for `~/Downloads`). Do
not schedule the approval-gated interactive flow.
