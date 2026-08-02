---
name: feedback-rederive-inherited-diagnosis
description: "Reproduce and print the actual value before continuing an inherited bisection — a handoff's causal framing is a hypothesis, not a finding"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e355fd73-2d0f-41a2-812d-d8922ddb15d0
  modified: 2026-08-01T22:55:51.702Z
---

When a handoff, prior session, or subagent hands over a failure *with a cause
already named*, treat that cause as an untested hypothesis. Reproduce the
failure first and read its raw output before extending anyone's bisection.

**Why:** 2026-08-01, l2detailz. A handoff framed two failing banner tests as a
Sentry regression and had already burned a bisection on it — Sentry runtime init
removed, `skipOpenTelemetrySetup` tried, `withSentryConfig` queued up next. The
whole search space was wrong. One standalone-server repro with stderr actually
read showed the banner rendering correctly; the test was pinning `sandbox=""`
after commit `55f7f53` deliberately widened it to
`allow-same-origin allow-top-navigation-by-user-activation`. Continuing the
inherited bisection would never have reached the answer, because the answer was
not in the space being bisected.

**How to apply:**
- `assert.ok(x.includes(literal))` yields a boolean and hides the diff. When one
  fails, print the actual value *before* changing any config — that single step
  replaced a multi-round bisection here.
- Child-process stdio piped but never drained is silent failure by construction.
  If a test spawns a server, drain its stderr in the repro.
- Bisecting *what changed recently* assumes the code moved. Also check whether
  the assertion's premise still holds — a test can rot while the code is right.
- An assertion should pin a tunable value in exactly one place. Give value
  ownership to the test that exists for it and have siblings assert *presence*
  (`/<iframe[^>]*\ssandbox=/`), so a deliberate widening breaks one test, not
  scattered ones.

Related: [[dev-team-learnings]] · [[feedback-reason-dont-ratify]]
