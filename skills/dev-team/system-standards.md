# System-Level Standards

Applied when the engineer report signals large scope: new endpoints, schema changes, new modules, cross-layer changes, or new external dependencies. Every finding must cite the section and bullet violated.

---

## API Design

- **RESTful Conventions**: resources are nouns, HTTP verbs express the action. `POST /bets` not `GET /createBet`.
- **Consistent Error Contract**: all endpoints return errors in the same shape (status code + error field). Never mix formats.
- **Backward Compatibility**: adding fields to a response is safe. Removing or renaming fields is a breaking change and requires a versioned endpoint.
- **Versioning Strategy**: version APIs from the start (`/v1/`). Introducing versioning retroactively is painful.
- **Pagination on Collections**: any endpoint returning a list must support pagination. Returning all records is never the right default.
- **Idempotency Keys**: mutating endpoints called over unreliable networks (mobile clients) should support idempotency keys to prevent double-writes.
- **Status Codes are Semantic**: 200 means success, 201 means created, 400 means caller error, 401 means unauthenticated, 403 means unauthorized, 404 means not found, 500 means server error. Don't return 200 with `{"error": "..."}`.

---

## Data Modeling

- **Normalize Until It Hurts, Then Denormalize**: start normalized. Denormalize only when a specific query performance problem is measured, not anticipated.
- **Index for Access Patterns**: every foreign key and every column appearing in a WHERE clause of a frequent query needs an index. Missing indexes on join columns are a scalability time bomb.
- **Migration Safety**: never drop a column or table in the same migration that removes the code using it. Remove code first, deploy, then drop the column in a follow-up migration.
- **No Nullable Foreign Keys Without a Reason**: a nullable FK means "this relationship is optional" — make sure that's intentional and documented.
- **Timestamps on Everything**: every table that represents a real-world entity should have `created_at` and `updated_at`. You will need them.
- **Schema as Contract**: the DB schema is a shared contract between services and the application. Changes require coordination, not unilateral edits.
- **Avoid EAV Patterns**: entity-attribute-value tables (key/value pairs as rows) are a last resort. Use JSONB columns or a proper schema instead.

---

## Service & Module Boundaries

- **Cohesion Over Convenience**: modules should be cohesive around a domain concept, not around what was easy to group. If two things change for different reasons, they belong in different modules.
- **Explicit Public Interface**: every module has a defined public surface. Internal helpers are not public. Callers depend on the interface, not the internals.
- **Avoid Shared Mutable State Across Boundaries**: two modules communicating through a shared DB table or global variable is a hidden coupling. Prefer explicit function calls or events.
- **Don't Reach Across Layers**: the frontend must not know about DB schema details. The DB layer must not know about HTTP response shapes. Each layer talks only to its immediate neighbor.
- **Services Should Own Their Data**: if two services read and write the same table, you don't have two services, you have one service with two entry points.

---

## Observability

- **Structured Logging**: log in a machine-parseable format (JSON). Include a consistent set of fields: timestamp, level, service, request_id, user_id, message.
- **Log at the Right Level**: DEBUG for internal state during development, INFO for normal business events, WARN for recoverable unexpected states, ERROR for failures requiring attention.
- **Instrument Business Events**: don't just log errors. Log meaningful business events (bet placed, bet accepted, caps awarded) — these are the signals that tell you the system is working.
- **Request IDs**: every inbound request should get a unique ID that is logged with every log line and returned in the response header. Essential for tracing issues across logs.
- **Health Endpoints**: every service exposes a `/health` endpoint that returns 200 if the service is operational. Checked by load balancers and monitoring.
- **Alert on Symptoms, Not Causes**: alert on error rate, latency, and availability — not on CPU or memory alone. Users don't care about CPU.

---

## Fault Tolerance

- **Timeouts on All External Calls**: every call to a DB, external API, or downstream service must have an explicit timeout. No call should be able to hang indefinitely.
- **Retry with Backoff**: transient failures (network blips, rate limits) should be retried with exponential backoff and jitter. Don't retry immediately in a tight loop.
- **Circuit Breakers on High-Traffic Paths**: if a dependency is failing, stop hammering it. Open the circuit, fail fast, and try again after a cooldown.
- **Graceful Degradation**: when a non-critical dependency is down, the system should degrade gracefully rather than fail completely. A leaderboard being stale is better than the whole app being down.
- **Bulkheads**: isolate failure domains. A slow background job should not exhaust the thread pool serving HTTP requests.
- **Idempotency Under Retry**: any operation that may be retried must be idempotent. A bet that gets submitted twice must not be accepted twice.

---

## Deployment & Operational Safety

- **Zero-Downtime Deploys**: DB migrations and code changes must be deployable without taking the app down. This usually means: expand (add new column/code), migrate data, then contract (remove old column/code) across separate deploys.
- **Feature Flags for Risky Rollouts**: new features that touch core flows should be behind a flag so they can be disabled without a rollout.
- **Rollback Plan**: every deploy has a defined rollback path. If a migration is irreversible, that's a red flag that needs to be resolved before shipping.
- **Config vs Code**: environment-specific configuration (URLs, thresholds, limits) belongs in config/env vars, not in code. Changing a threshold should not require a deploy.
- **Graceful Shutdown**: services handle SIGTERM by finishing in-flight requests before exiting. Killing a process mid-request is not graceful.
