# Audit: Patio repo (/workspace/patio) vs portfolio writeup (/home/user/portfolio/src/content/projects/patio.mdx)

## What the project actually does

Patio is a **social betting app for backyard drinking games** (Caps, Pong, Beerball, Campus Golf) played among friends — not a sports-betting platform. Players wager a virtual currency called "caps" (new accounts start with 500; +100 refresh after 7 days inactive, `backend/auth.py`). Two bet modes:

- **PvP bets**: a player posts an Over/Under line on a game stat; another player accepts; both submit game stats afterward and the bet settles only when both submissions match (honor-system dual confirmation, `compute_status_message`/`check_stats_match` in `backend/app.py`).
- **CPU/House bets**: admin-only endpoints (`/cpu/create_*`, gated on `player_id == 0`) generate statistically informed lines from real friends' historical performance, biased ~4% in the house's favor.

**Actual stack** (per README.md, CLAUDE.md, and code): React 19 CRA frontend (React Router 7, Axios, Context API, localStorage tokens) + **Python Flask backend** with raw psycopg2 (no ORM) + Supabase Postgres. JWT auth (HS256) with pbkdf2:sha256 password hashing. Deploy target: Vercel (frontend) + Render (backend, `Procfile`).

**Scale** (measured): ~6,150 LOC total across `src/` + `backend/` (largest file `backend/app.py` at 1,499 lines). Backend: 17 routes in `app.py` + 3 auth routes (`/register`, `/login`, `/me`) + 1 dead unregistered blueprint route. Frontend: 6 real pages (PvP, CPU/House, Ongoing, Leaderboard, Profile, Login/Register) + a 17-line Messages stub + 1 shared component (BottomNav) + 3 util modules. One test file — CRA boilerplate only.

**State of completeness**: pre-launch MVP. `PROGRESS.md` (verified 2026-07-01) states: "No stage of PLAN.md has been started yet — the repo is still at its pre-refactor baseline." `PLAN.md` (34KB) is a rigorous self-audit + roadmap: mobile-first pivot to React Native/Expo with App Store launch as the end goal, gated on known security and money-correctness bugs. Git history is a **single commit dated 2026-07-02** ("updated to include react native conversion") — no verifiable development timeline. `server.js` (39 lines) is an orphaned Socket.IO chat demo that PLAN item M.4/X.2 slates for deletion; it is not part of the product.

## Real findings/results (what's actually implemented and verifiable)

**Working and real:**
- JWT auth flow: register/login with pbkdf2:sha256 hashing, token interceptor in `src/api.js`, auth guard in `src/App.js`.
- Full PvP bet lifecycle: create (`/create_bet`) → browse (`/pvp_bets`) → accept with balance deduction (`/accept_bet/<id>`) → dual stat submission → payout of 2x wager on confirmed match (`/submit_stats/<id>`).
- CPU bet lifecycle: 6 line-generation endpoints (`/cpu/create_{caps,pong,beerball}_{shots,score}_bet`), acceptance tracking via `cpu_acceptances` table.
- Statistical line-generation engine (see next section) — genuinely the most sophisticated code in the repo.
- Rolling stat pipeline: `backend/stats_utils.py` maintains `player_stat_aggregates` (mean, std, mean_last_5, win_rate, n_games per player/game/stat/team_size) as bets resolve.
- Parameterized SQL throughout (psycopg2 `%s` placeholders) — the writeup's injection-safety claim is roughly true.
- Deployment scaffolding: `Procfile`, `.env.example`, Render/Vercel instructions.

**Not implemented / known-broken (documented in the repo's own PLAN.md/PROGRESS.md):**
- No WebSockets in the product (no socket client in `package.json`; `server.js` is disconnected demo code). No real-time anything.
- No external odds API, no sports data, no polling/caching/delta-push pipeline.
- No rate limiting, no optimistic locking or version fields, no dead-letter queue, no audit/ledger table, no odds-snapshot table (schema in `backend/models.py` + CLAUDE.md: players, bets, cpu_acceptances, bettable_players, bettable_player_stats, player_stat_aggregates).
- Known money bugs (PLAN 5.2/5.3): CPU settlement path **double-pays** (`amount*2` re-credited on every matching re-submission); ties credit nobody and both wagers vanish; `cleanup_bets` deletes expired bets without refunding.
- Known security holes (PLAN Stage 0): `/cleanup_bets` is unauthenticated and destructive; `/submit_stats` trusts client-supplied `playerId` (verified at `app.py:632-633`); `/create_bet` trusts client-supplied `posterId`; hardcoded JWT secret fallback `"your-secret-key"` in `config.py`; `/me` is broken (doesn't strip `Bearer ` prefix, selects nonexistent columns); `print()`s leak JWT payloads; Flask debug mode on.
- Balance updates are check-then-act (SELECT balance, then UPDATE) — race conditions acknowledged in PLAN 5.1.
- No analytics, no user-count instrumentation, no performance benchmarks anywhere in the repo.

## Strongest visualizations/dashboards/artifacts (paths + descriptions)

- **`backend/caps_bet_generation.py`, `backend/pong_bet_generation.py`, `backend/beerball_bet_generation.py`** (~760 LOC) — the standout subsystem: house line generation using scipy/numpy. Recency-weighted player means (`adjust()` blends `mean` and `mean_last_5`), harmonic-mean team strength, a game-length "opportunity factor" from team balance ratio, composite strength (score + shots + win_rate), and lines set at the 0.47/0.53 percentile of a fitted normal distribution to bake in a ~4% house edge, then snapped to x.5 to eliminate pushes.
- **`backend/stats_utils.py`** (231 LOC) — rolling aggregate updater feeding the odds engine; the closed loop (bets resolve → stats recorded → aggregates updated → future lines sharpen) is a genuinely nice design.
- **`backend/app.py` settlement logic** (`check_stats_match`, `compute_status_message`, `/submit_stats`) — the honor-system dual-confirmation state machine.
- **`PLAN.md` + `PROGRESS.md`** — a serious, itemized security/correctness audit and staged App Store launch plan; strong evidence of engineering judgment and honesty (usable as a portfolio artifact in itself).
- **`src/assets/images/`** (betcard.png, back1.png, lb.png, etc.) — custom UI art assets; note these are design assets, **not screenshots**. The repo contains no screenshots.
- **Live URL**: `patio.nateseluga.com` could not be verified from this sandbox (proxy blocked); README/Procfile show a real Render+Vercel deploy setup but with placeholder env values only. Treat the live URL as unverified.

## Inaccuracies & gaps in current writeup (itemized: writeup claim → repo reality)

1. **"Sports Betting Platform" / "live odds integration" (title, summary)** → Social betting on backyard drinking games among friends with virtual currency; no sports, no live odds, no real money.
2. **"Node.js backend" (metrics + Architecture section)** → Backend is Python Flask + raw psycopg2. The only Node server file is a 39-line orphaned Socket.IO chat demo (`server.js`) slated for deletion in PLAN M.4.
3. **"Users Tracked: 100+ beta testers" / "100+ beta testers over 2 months"** → No evidence anywhere; no analytics code; PLAN.md targets a *first* App Store launch, implying no public user base.
4. **"Development Time: 4 months"** → Unverifiable; git history is one squashed commit dated 2026-07-02.
5. **Frontmatter date 2024-08-20** → All repo activity (commit, PLAN, PROGRESS) is dated 2026-07.
6. **"Real-time odds updates via WebSocket," WebSocket server, delta publishing, polling fallback, heartbeats** → None exist in the product; no socket client dependency in `package.json`.
7. **"Polling external odds API every few seconds (e.g., ESPN...)"** → No external API integration at all; lines are generated from friends' game-stat aggregates.
8. **Components "BetSlip, OddsBoard, AccountDashboard, BetHistory"** → None exist. Actual pages: PvP, CPU, Ongoing, Leaderboard, Profile.
9. **"ten-plus sports and hundreds of events"** → Three games with generation engines (Caps, Pong, Beerball); Campus Golf exists only as a schema enum value.
10. **"Rate-limiting... token-bucket approach"** → No rate limiting anywhere in the backend.
11. **"Optimistic locking on balance updates (version field)"** → No version field; balance updates are non-atomic check-then-act, with race conditions explicitly flagged in PLAN 5.1.
12. **"Dead-letter queue for failed bet executions"** → Does not exist.
13. **"Audit table to track balance changes," "balance ledgers," "odds snapshots"** → No such tables in the schema.
14. **"Bet placement... median 40ms, p99 120ms"; "odds latency <500ms"; "DB p99 <50ms"; "1.2s page load, Lighthouse 88"** → No benchmarks, load tests, or Lighthouse reports exist in the repo. All numbers are unsupported.
15. **"No lost transactions even under concurrent load" / "Zero reported balance discrepancies"** → Directly contradicted by the repo's own PLAN 5.2/5.3: caps silently vanish on ties and expiry, and the CPU settlement path double-pays on repeated submissions.
16. **"95% successful bet placement," "median session 15 minutes," "improved conversion by 20%"** → No instrumentation exists to have measured any of these.
17. **"Logging and error tracking for debugging production issues"** → Reality is `print()` statements that leak JWT payloads and raw auth headers (PLAN 0.7), with Flask debug mode enabled.
18. **"Input validation... to prevent abuse"** → Several endpoints trust client-supplied identity (`playerId`, `posterId`) and `/cleanup_bets` is unauthenticated-destructive (PLAN 0.1/0.5).
19. **"PostgreSQL... indexes on frequently-queried columns"** → `models.py` creates tables with no explicit indexes beyond PK/unique constraints.
20. **Live URL "patio.nateseluga.com (beta access available)"** → Unverified; deploy config exists but only with placeholder values.

**Real strengths the writeup fails to mention:**
- The **statistical odds engine** — the genuinely impressive part: scipy-based line generation with recency weighting, harmonic-mean team strength, normal-percentile biasing for a ~4% house edge, and push-proof half-point lines.
- The **self-improving stats pipeline**: bet settlements feed rolling per-player aggregates that sharpen future house lines.
- The **honor-system settlement design**: dual independent stat submission with match confirmation — a thoughtful trust mechanism for a refereeless social product.
- The **original product concept**: a novel niche (betting caps on backyard games with friends) that is far more memorable than a generic sportsbook clone.
- The **engineering self-audit**: PLAN.md's itemized security/money-correctness findings and staged React Native → App Store roadmap demonstrate real senior-level judgment.
- Solo end-to-end ownership: schema, API, auth, odds math, UI, and deploy config all by one person.

## Recommended framing for rewrite (2-3 sentences a rewrite should be built around)

Patio is a solo-built, full-stack social betting app (React + Flask + Postgres) where friends wager virtual "caps" on backyard games, with the centerpiece being a scipy-powered house-odds engine that generates Over/Under lines from rolling per-player stat aggregates, biased ~4% in the house's favor and sharpened automatically as results feed back in. It is honestly framed as a working pre-launch MVP mid-pivot to a React Native iOS app, backed by a rigorous self-audit (PLAN.md) that catalogs the security and settlement-correctness work gating an App Store release. The story to tell is original product design, applied probability/statistics, and clear-eyed engineering judgment — not fabricated production metrics.
