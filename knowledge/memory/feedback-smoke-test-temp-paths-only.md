# Smoke-test against temp paths, never real result artifacts

**2026-08-04, hitter-embedding.** Ran `rm -f results/phase_d/sweep_log.csv` to get a
clean slate before smoke-testing a sweep driver. That file was the ledger of nine
completed overnight training runs — hours of compute and the only record of which
configurations had finished. Recovered it only because the per-run logs happened to
survive under `results/phase_d/logs/`; one of the nine columns could not be
reconstructed and is still blank.

## The rule

Before deleting or truncating anything under `results/`, `data/processed/`, `out/`,
or any directory holding completed run output: **don't.** Point the smoke test at a
temp path instead (`--out-dir /tmp/...`, `--data-dir /tmp/...`) and leave the real
artifact untouched.

If a test genuinely must write to the real path, copy the file aside first and say so.

## Why the obvious guard fails

The danger isn't ignorance that the file matters — it's that the destructive command
sits inside a long setup chain where every other step is harmless (`rm -rf /tmp/...`,
`rm -f *.pt` on smoke checkpoints). The real path rides along with the fake ones and
never gets a second look.

So the check is per-path, not per-command: for every path in a cleanup line, ask
whether anything in it was produced by work that would have to be re-run. Ledgers,
result CSVs, trained checkpoints, and built datasets all qualify.

## Related

An interrupted long-running job is cheap to redo; a deleted record of what already
finished is not — it silently causes the work to be redone or, worse, skipped.
