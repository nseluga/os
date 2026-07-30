---
name: leads
description: Find, score, and track bcns sales leads in the Master Client List sheet. Use when the user says "/leads", "/leads 40", "find leads", "find me some businesses", "log a call", "update a lead", "who haven't we called", "how are leads converting", or wants the client-list spreadsheet read, scored, or added to.
---

# Leads

**Related:** [[reference-gcp-auth-bcns]] · [[knowledge/audience/bcns-clients|bcns-clients]] (who qualifies as a fit)

Finds local businesses via Places, tracks them through the funnel, and scores
them only once history says what actually closes. bcns builds websites, apps,
and internal tools — the buying signal is not assumed. The scripts do IO and
arithmetic only.

## Setup

```sh
cd ~/os/skills/leads && set -a && . ./.env && set +a
V=~/os/skills/leads/.venv/bin/python
```

`.env` is gitignored (sheet id, SA emails, monthly cap). This repo is public —
never write those values into a tracked file or into chat.

## Interpreting the request

The user speaks in territories and vibes ("local businesses in southern CT",
"who needs a site around here"). Places needs a **category Google recognises**
and a **place Google can geocode**. Translate before searching — never pass a
vague phrase through.

This is not optional politeness: `"local business in the southern ct area"` was
tested and returned business consultants in Brooklyn and the Bronx. Zero usable
leads, one wasted call.

1. **Expand the region into named towns.** "southern CT" → Milford, Stratford,
   Shelton, Orange, West Haven, Fairfield, Bridgeport… Use real municipalities.
2. **Expand the vibe into trades.** Default set, unless the user names others:
   roofers, plumbers, HVAC, electricians, landscapers, painters, auto detailing,
   general contractors.
3. **Build the query grid** — one `"<trade> in <town> <ST>"` per pair.
4. **Show the plan before spending.** Number of queries, estimated API calls
   (≈1 per 20 requested), month-to-date budget before and projected after. Then
   confirm. Do not silently burn 40 calls because someone said "find me leads".
5. Run the grid, appending after each query so a failure mid-sweep doesn't lose
   completed work. `append` dedupes across queries automatically.

Skip straight to searching only when the user already gave a concrete trade and
town ("find me roofers in Milford").

## `/leads [N]` — find N leads

Default N is 20. Run in order; do not skip step 1.

1. **`$V sheets.py stats $BCNS_SHEET`** — conversion history. This is what makes
   scoring improve over time. Read `by_type`, `by_city`, `by_review_band`,
   `by_has_website`, `by_source_query`. **Ignore any segment with
   `enough_data: false`** — it is one or two rows and means nothing yet.
2. **`$V places.py budget`** — stop and tell the user if remaining < N/20.
3. **`$V sheets.py ids $BCNS_SHEET`** — what's already known.
4. **Pick the query from evidence.** If a segment converts well and has
   `enough_data: true`, search that trade/town next. With no history yet, ask
   which trades and towns to target — do not invent a territory.
5. **`$V places.py search "<trade> in <town> <state>" --count N`** — pages at 20
   per API call, re-checking the budget between pages.
6. **Record what you observe in `notes`** — current web presence, apparent size,
   software they already pay for. Leave `lead_score` blank unless step 1 gave
   you a segment to cite (see Scoring).
7. **`$V sheets.py append $BCNS_SHEET`** — drops any `place_id` already present.
8. Report: how many added, how many skipped as duplicates, the new budget, and
   what you observed — not a ranking, unless stats earned one.

Queries are literal Google Maps searches. `"plumbers in Providence RI"` works;
`"businesses that need websites"` returns nothing useful — Google has no concept
of who needs anything, only what a business *is* and *where*.

## Scoring

bcns builds websites, apps, and software tools for small businesses. What
predicts a close is **not yet known** — so there is no rubric, on purpose.

**Leave `lead_score` and `score_reason` blank** unless `stats` gives you a
segment with `enough_data: true`. A `win_rate` of `null` means nobody in that
segment has been called — unknown, not bad. Guessing a score
from intuition creates numbers that look like evidence, get compared against
outcomes later, and quietly measure nothing but the guess.

Once a segment has real signal, score from it and cite it:

- `lead_score` — 1–10, derived from the segment's `win_rate` relative to others
- `score_reason` — the segment and the number, e.g.
  `"8 — 200+ review band is 4/11 won vs 1/20 overall"`

Never write a `score_reason` that doesn't name a segment and a count. If you
can't cite one, the score shouldn't exist yet.

**Record observations in `notes` instead.** Facts are always safe to collect and
are what later becomes signal: business size, what their current web presence
is, whether they already run booking/ordering software, anything suggesting they
buy tools. Observations in `notes`, judgments in `lead_score` — and only when
earned.

## Working the funnel

```sh
# every contact attempt — bumps call_count, stamps the date
$V sheets.py log $BCNS_SHEET <place_id> --status reached \
    --contact_name "Dana" --outcome "interested, call back Tuesday"

# stage changes that weren't a call
$V sheets.py update $BCNS_SHEET <place_id> \
    '{"status":"won","deal_value":"2400","close_date":"2026-07-30"}'
```

`status`: `new → attempted → reached → consult_scheduled → consult_done → won`,
or `lost` / `dead`. Use `log` for anything that was a contact attempt — it is the
only thing that increments `call_count`. Use `update` for everything else.

Rows are found by `place_id`, never row number.

## Reading

- `$V sheets.py stats $BCNS_SHEET` — funnel rates by segment
- `$V sheets.py read $BCNS_SHEET` — all rows, for filtering ("who haven't we
  called", "who's due a follow-up", "which consults never closed")
- `$V sheets.py ids $BCNS_SHEET` — place_ids only; cheap, use before searching

## Columns

Identity from Places: `place_id business_name type city phone website
has_website rating review_count`
Judgment: `lead_score score_reason`
Funnel: `status call_count last_contact contact_name last_outcome consult_date
close_date deal_value`
Provenance: `source_query date_added notes`

Appending a column is safe. Reordering or renaming one shifts every existing
row — don't.

## Notes & gotchas

- **The budget is enforced, not advised.** `places.py search` reads real usage
  from Cloud Monitoring and refuses past `BCNS_PLACES_MONTHLY_CAP` (950 of the
  1,000 free Enterprise calls/month), re-checking between pages. It fails closed:
  if usage can't be read, it doesn't spend. A 300/day quota backstops the 1–4 min
  Monitoring lag.
- **Self-improvement is `stats`, nothing more.** No model, no stored weights —
  conversion is recomputed from the sheet every run, so it cannot go stale. It
  only works if outcomes get logged. A lead called but never logged is invisible
  to it.
- Auth is OAuth + service-account impersonation. **No API key and no key file
  exist** — don't create either. If auth breaks:
  `gcloud auth application-default login` (never with `--scopes`; blocked).
- Field masks in `places.py` are deliberately narrow. Requesting `*` would
  upgrade every call to the priciest SKU for no benefit.
- `city` is parsed from a formatted address and assumes US format.
- `sheets.py init` refuses to rewrite headers when data rows exist unless
  `--force`.
