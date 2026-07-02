# Code-Level Standards

Applied on every review. Every finding must cite the section and bullet violated.

---

## Architecture

- **Single Responsibility**: each module/function does one thing. If you need "and" to describe it, split it.
- **Separation of Concerns**: data access, business logic, and presentation live in separate layers. Business logic must not build SQL. Routes must not contain data transformation.
- **Dependency Inversion**: high-level modules depend on abstractions (interfaces, injected deps), not concrete implementations.
- **Deep Modules**: hide complexity behind simple interfaces. A function that takes 6+ params is a leaky module.
- **No Circular Dependencies**: if A imports B and B imports A, the boundary is wrong.
- **Encapsulation**: internal state is not exposed. Callers get what they need, not the whole object.

---

## Safety & Security

- **Validate at Boundaries**: validate all input at system entry points (HTTP handlers, CLI args, external API responses). Never validate mid-stack.
- **Parameterized Queries Only**: no string-interpolated SQL, ever. f-strings or concatenation in queries = SQL injection.
- **Auth Before Data**: authorization checks run before any data is accessed or modified, never after.
- **Least Privilege**: functions and modules receive only the data and permissions they need.
- **No Secrets in Code**: credentials, keys, and tokens go in environment variables only. Never hardcoded.
- **Sanitize User Content**: any user-supplied string rendered in a UI must be escaped or sanitized (XSS prevention).
- **Safe Defaults**: features default to the more restrictive behavior. Opt-in to permissive, not opt-in to safe.

---

## Efficiency

- **No N+1 Queries**: never query inside a loop. Batch DB calls before the loop, pass results in.
- **O(1) Lookups**: if membership is checked repeatedly, convert to a set or dict before the loop.
- **Hoist Invariants**: anything producing the same result on every iteration belongs outside the loop.
- **Close Resources**: DB connections, file handles, and sockets are closed in `finally` blocks or context managers.
- **Lazy Where Appropriate**: don't fetch or compute data until it's needed. Don't load unbounded rows to display a few.

---

## Reliability

- **Fail Fast**: validate preconditions at the top of a function and return/raise early.
- **Handle Errors at Boundaries**: catch exceptions where you can do something meaningful. Don't catch-and-swallow mid-stack.
- **Log with Context**: error logs include enough information to reproduce the issue (relevant IDs, inputs, state).
- **Idempotent Writes**: writes that may be retried produce the same result whether run once or many times.
- **Don't Assume Success**: check return values and status codes. None is not the expected value.
- **Explicit Over Implicit**: explicit error returns or typed exceptions over silent failures or magic return values.

---

## Scalability

- **Stateless Services**: no server-side session state. State lives in the client or the DB.
- **No Global Mutable State**: module-level variables that change at runtime are a concurrency hazard.
- **Paginate Unbounded Results**: any endpoint or query returning unbounded rows must have limit/offset or cursor.
- **Defer Expensive Work**: don't do slow operations (external API calls, large computations) synchronously in a request handler.
- **Connection Pooling**: don't open a new DB connection per request. Use a pool.

---

## Code Quality

- **Names Describe Intent**: `get_accepted_bets_for_player` not `query2`. No abbreviations unless universally known (`id`, `url`, `db`).
- **No Magic Values**: named constants for any number, string, or boolean that isn't self-evident.
- **Function Length**: functions exceeding ~30 lines are likely doing too much. Extract.
- **No Commented-Out Code**: dead code is deleted, not commented. Git history preserves it.
- **Flat Over Nested**: prefer early returns over deeply nested if/else. Three levels of nesting is a smell.
- **Boolean Parameters are a Smell**: `process(user, True)` tells the caller nothing. Prefer separate functions or an enum.
- **No Redundant Comments**: don't describe what the code does. Only comment the non-obvious *why*.

---

## Testability

- **Pure Functions Where Possible**: same input always produces same output, no side effects.
- **Inject Dependencies**: don't hardcode DB connections, clocks, or external services. Pass them in.
- **Seams at Every Boundary**: every external system (DB, API, filesystem, time) has a seam where a test can intercept.
- **Test Behavior, Not Implementation**: tests assert on outputs and observable state, not internal function calls.
