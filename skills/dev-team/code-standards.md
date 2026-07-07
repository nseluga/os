# Code-Level Standards

Applied on every review. Every finding must cite the section + bullet name violated.

## Architecture
- **Single Responsibility** — one job per module/function; if you need "and" to describe it, split.
- **Separation of Concerns** — data access, business logic, presentation in separate layers; logic doesn't build SQL, routes don't transform data.
- **Dependency Inversion** — depend on abstractions/injected deps, not concrete implementations.
- **Deep Modules** — hide complexity behind simple interfaces; 6+ params = leaky.
- **No Circular Dependencies** — A↔B imports means the boundary is wrong.
- **Encapsulation** — don't expose internal state; callers get what they need.

## Safety & Security
- **Validate at Boundaries** — validate input at entry points (HTTP, CLI, external responses), never mid-stack.
- **Parameterized Queries Only** — no string-interpolated/f-string SQL, ever.
- **Auth Before Data** — authorization runs before any data access, never after.
- **Least Privilege** — modules get only the data/permissions they need.
- **No Secrets in Code** — creds/keys/tokens in env vars only.
- **Sanitize User Content** — escape/sanitize any user string rendered in UI (XSS).
- **Safe Defaults** — default to the more restrictive behavior; opt into permissive.

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

## Code Quality
- **Names Describe Intent** — `get_accepted_bets_for_player`, not `query2`; no obscure abbreviations.
- **No Magic Values** — named constants for any non-self-evident number/string/bool.
- **Function Length** — >~30 lines likely does too much; extract.
- **No Commented-Out Code** — delete it; git preserves history.
- **Flat Over Nested** — early returns over deep if/else; 3 levels of nesting is a smell.
- **Boolean Parameters are a Smell** — `process(user, True)` says nothing; use separate fns or an enum.
- **No Redundant Comments** — comment the non-obvious *why*, not the *what*.

## Testability
- **Pure Functions Where Possible** — same input → same output, no side effects.
- **Inject Dependencies** — pass in DB/clock/external services; don't hardcode.
- **Seams at Every Boundary** — every external system has a test-interceptable seam.
- **Test Behavior, Not Implementation** — assert on outputs/observable state, not internal calls.
