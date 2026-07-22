# Review Standards

The sections the Optimization Reviewer applies, extracted from `code-standards.md`
(Efficiency, Reliability, Scalability, Safety & Security) and `system-standards.md`
(Observability, Fault Tolerance). This is the reviewer's whole standards surface —
read this instead of the two full files. Every finding cites the section + bullet name.

> MAINTENANCE: manual extraction of code-standards.md (Efficiency, Reliability,
> Scalability, Safety & Security) + system-standards.md (Observability, Fault
> Tolerance). Editing either source file? Update this file to match — the
> Reviewer reads only this one.

## Efficiency
- **No N+1 Queries** — never query inside a loop; batch before, pass results in.
- **O(1) Lookups** — repeated membership checks use a set/dict, not a list scan.
- **Hoist Invariants** — move loop-invariant work outside the loop.
- **Close Resources** — connections/handles/sockets closed in finally/context managers.
- **Lazy Where Appropriate** — don't fetch/compute until needed; don't load unbounded rows to show a few.

## Reliability
- **Fail Fast** — validate preconditions at the top; return/raise early.
- **Handle Errors at Boundaries** — catch where you can act; no catch-and-swallow mid-stack.
- **Log with Context** — error logs carry the IDs/inputs/state needed to reproduce.
- **Idempotent Writes** — retried writes produce the same result once or many times.
- **Don't Assume Success** — check return values and status codes; None isn't the expected value.
- **Explicit Over Implicit** — typed exceptions/explicit error returns over silent/magic returns.

## Scalability
- **Stateless Services** — no server-side session state; state lives in client or DB.
- **No Global Mutable State** — runtime-changing module vars are a concurrency hazard.
- **Paginate Unbounded Results** — any list-returning endpoint/query has limit/offset or cursor.
- **Defer Expensive Work** — no slow external calls/large computation synchronously in a handler.
- **Connection Pooling** — no new DB connection per request.

## Safety & Security
- **Validate at Boundaries** — validate input at entry points (HTTP, CLI, external responses), never mid-stack.
- **Parameterized Queries Only** — no string-interpolated/f-string SQL, ever.
- **Auth Before Data** — authorization runs before any data access, never after.
- **Least Privilege** — modules get only the data/permissions they need.
- **No Secrets in Code** — creds/keys/tokens in env vars only.
- **Sanitize User Content** — escape/sanitize any user string rendered in UI (XSS).
- **Safe Defaults** — default to the more restrictive behavior; opt into permissive.

## Observability
- **Structured Logging** — machine-parseable (JSON) with timestamp, level, service, request_id, user_id, message.
- **Log at the Right Level** — DEBUG/INFO/WARN/ERROR used for their intended purpose.
- **Instrument Business Events** — log meaningful events (bet placed/accepted), not just errors.
- **Request IDs** — unique ID per request, logged on every line and returned in a header.
- **Health Endpoints** — every service exposes `/health` returning 200 when operational.
- **Alert on Symptoms, Not Causes** — alert on error rate/latency/availability, not CPU/memory alone.

## Fault Tolerance
- **Timeouts on All External Calls** — every DB/API/downstream call has an explicit timeout.
- **Retry with Backoff** — retry transient failures with exponential backoff + jitter, not a tight loop.
- **Circuit Breakers on High-Traffic Paths** — open the circuit on a failing dependency; fail fast, cool down.
- **Graceful Degradation** — degrade on a non-critical dependency outage rather than fail wholesale.
- **Bulkheads** — isolate failure domains; a slow job doesn't exhaust the HTTP thread pool.
- **Idempotency Under Retry** — any retriable operation is idempotent (no double-accepted bet).
