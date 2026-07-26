# Review Standards

The Optimization Reviewer's whole standards surface — read this instead of the
two full files. Every finding cites the section + bullet name.

> MAINTENANCE: manual extraction of code-standards.md (Efficiency, Reliability,
> Scalability, Safety & Security) + system-standards.md (Observability, Fault
> Tolerance). Editing either source file? Update this file to match — the
> Reviewer reads only this one. Intentionally NOT extracted: system-standards'
> API Design, Data Modeling, Service & Module Boundaries, Deployment, and
> Scale & Infrastructure — those are engineer/design standards, not review lenses.

## Efficiency
- **No N+1 Queries**
- **O(1) Lookups**
- **Hoist Invariants**
- **Close Resources**
- **Lazy Where Appropriate** — don't load unbounded rows to show a few.

## Reliability
- **Fail Fast**
- **Handle Errors at Boundaries** — catch where you can act; no catch-and-swallow mid-stack.
- **Log with Context** — error logs carry the IDs/inputs/state needed to reproduce.
- **Idempotent Writes**
- **Don't Assume Success** — check return values and status codes.
- **Explicit Over Implicit** — typed exceptions/explicit error returns over silent/magic returns.

## Scalability
- **Stateless Services** — state lives in client or DB.
- **No Global Mutable State**
- **Paginate Unbounded Results**
- **Defer Expensive Work** — no slow external calls/large computation synchronously in a handler.
- **Connection Pooling** — no new DB connection per request.

## Safety & Security
- **Validate at Boundaries** — validate input at entry points (HTTP, CLI, external responses), never mid-stack.
- **Parameterized Queries Only** — no string-interpolated/f-string SQL, ever.
- **Auth Before Data** — authorization runs before any data access, never after.
- **Least Privilege**
- **No Secrets in Code** — creds/keys/tokens in env vars only.
- **Sanitize User Content** — escape/sanitize any user string rendered in UI (XSS).
- **Safe Defaults** — default to the more restrictive behavior; opt into permissive.

## Observability
- **Structured Logging** — machine-parseable (JSON) with timestamp, level, service, request_id, user_id, message.
- **Log at the Right Level**
- **Instrument Business Events** — log meaningful events (bet placed/accepted), not just errors.
- **Request IDs** — unique ID per request, logged on every line and returned in a header.
- **Health Endpoints** — every service exposes `/health` returning 200 when operational.
- **Alert on Symptoms, Not Causes** — alert on error rate/latency/availability, not CPU/memory alone.

## Fault Tolerance
- **Timeouts on All External Calls**
- **Retry with Backoff** — exponential backoff + jitter, not a tight loop.
- **Circuit Breakers on High-Traffic Paths**
- **Graceful Degradation** — degrade on a non-critical dependency outage rather than fail wholesale.
- **Bulkheads** — isolate failure domains; a slow job doesn't exhaust the HTTP thread pool.
- **Idempotency Under Retry** — no double-accepted bet.
