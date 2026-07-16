---
name: reference-local-automation-not-cloud-schedule
description: Repeatable automation that touches local files/apps cannot use Claude cloud schedules or cowork — must run on-machine via launchd/cron.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7c643605-06a0-427b-9387-a72dc58240d0
---

Claude cloud scheduled routines (`/schedule`, CronCreate) and cowork run in an
Anthropic cloud sandbox with **no access to the local Mac's filesystem**. Any
repeatable job that needs to touch local files, Finder, or local apps must run
**on-machine** — a macOS `launchd` LaunchAgent (or `cron`) invoking the local
`claude` CLI or a script.

Caveats when going local: won't run while the Mac is off/asleep (launchd catches
up once on next wake/login, imperfectly); `~/Downloads`/`~/Desktop`/`~/Documents`
are TCC-protected and need Full Disk Access granted to the runner.

Decision rule: local target ⇒ local scheduler. Cloud schedules are only for work
that lives in the cloud (repos, APIs, web). See [[tidy-downloads]] skill, which
chose manual-run for exactly this reason.
