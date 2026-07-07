# System-Level Standards

Applied when the engineer report signals large scope: new endpoints, schema changes, new modules, cross-layer changes, or new external deps. Every finding cites the section + bullet name.

## API Design
- **RESTful Conventions** — resources are nouns, verbs express action (`POST /bets`, not `GET /createBet`).
- **Consistent Error Contract** — all endpoints return errors in one shape (status + error field).
- **Backward Compatibility** — adding response fields is safe; removing/renaming is breaking → version it.
- **Versioning Strategy** — version from the start (`/v1/`); retrofitting is painful.
- **Pagination on Collections** — list endpoints must paginate; returning all records is never the default.
- **Idempotency Keys** — mutating endpoints over unreliable networks support idempotency keys.
- **Status Codes are Semantic** — 200/201/400/401/403/404/500 mean what they mean; no 200 + `{"error"}`.

## Data Modeling
- **Normalize Until It Hurts, Then Denormalize** — denormalize only on a measured query problem.
- **Index for Access Patterns** — index every FK and every WHERE column of a frequent query.
- **Migration Safety** — remove code first, deploy, then drop the column in a follow-up migration.
- **No Nullable FKs Without a Reason** — a nullable FK means "optional"; make that intentional.
- **Timestamps on Everything** — real-world-entity tables get `created_at`/`updated_at`.
- **Schema as Contract** — schema changes require coordination, not unilateral edits.
- **Avoid EAV Patterns** — use JSONB or a proper schema, not key/value rows.

## Service & Module Boundaries
- **Cohesion Over Convenience** — group by domain concept; things that change for different reasons split.
- **Explicit Public Interface** — defined public surface; callers depend on it, not internals.
- **Avoid Shared Mutable State Across Boundaries** — no coupling via shared table/global; use calls/events.
- **Don't Reach Across Layers** — frontend doesn't know DB schema; DB layer doesn't know HTTP shapes.
- **Services Should Own Their Data** — two services on one table = one service with two entry points.

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

## Deployment & Operational Safety
- **Zero-Downtime Deploys** — expand → migrate → contract across separate deploys.
- **Feature Flags for Risky Rollouts** — core-flow features behind a flag, disableable without a rollout.
- **Rollback Plan** — every deploy has a rollback path; irreversible migration = red flag.
- **Config vs Code** — env-specific URLs/thresholds/limits in config/env vars, not code.
- **Graceful Shutdown** — handle SIGTERM by finishing in-flight requests before exit.
