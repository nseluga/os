# improve-system change log

Append-only. One line per applied change.

[2026-08-03] AUTO malformed-output-file — removed the orphaned Content block left in review.md by the 2026-07-27 run that died on ENOTFOUND; its CI half is verbatim in reference-bcns-ci-setup.md, its git-workflow half is re-proposed as a review item
[2026-08-03] APPLIED skill-edit — wrapped improve-system-weekly.sh's claude call in flock -n to prevent concurrent-run clobbering
[2026-08-03] APPLIED memory-edit — compacted dev-team-learnings.md 5,086→1,294 words (PROCESS bullets only); moved 25 CODE-DEFECT bullets verbatim into dt-review's review-standards.md "Known Failure Patterns" section
[2026-08-03] APPLIED skill-edit — moved design skill's direction-setting verbs (shape/critique/init/craft) into a new "Derive the direction first" section before "Wide net, then narrow"
[2026-08-03] APPLIED link-fix — added per-skill vendored entries (3 higgsfield skills + prototype) to skills/INDEX.md
[2026-08-03] APPLIED knowledge-restructure — credited find-skills (vercel-labs/skills) and git-guardrails-claude-code (mattpocock/skills) in THIRD_PARTY.md; moved their INDEX.md entries into the vendored section
