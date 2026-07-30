#!/usr/bin/env python3
"""Places discovery with a hard month-to-date budget guard.

Auth is OAuth (ADC) -- Places API (New) accepts bearer tokens, so no API key
exists to leak or restrict.

The monthly ceiling is enforced by asking Google how many calls we've actually
made this month (Cloud Monitoring), not by a local tally. A local counter only
knows about one machine; both owners share this project.

    python places.py budget
    python places.py search "plumbers in Providence RI" | python sheets.py append $BCNS_SHEET
"""
import argparse
import datetime as dt
import json
import os
import sys

import google.auth
from google.auth.transport.requests import AuthorizedSession

PROJECT = os.environ.get("BCNS_PROJECT", "bcns-leads")
CAP = int(os.environ.get("BCNS_PLACES_MONTHLY_CAP", "950"))

# Only the fields the sheet actually stores. Requesting '*' silently upgrades
# every call to the priciest SKU.
FIELD_MASK = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.primaryTypeDisplayName",
    "places.nationalPhoneNumber",
    "places.websiteUri",
    "places.rating",
    "places.userRatingCount",
])


def _session():
    creds, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"])
    return AuthorizedSession(creds)


def month_to_date(session):
    """Calls made against Places so far this month, per Google's own metering."""
    now = dt.datetime.now(dt.timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    r = session.get(
        f"https://monitoring.googleapis.com/v3/projects/{PROJECT}/timeSeries",
        params={
            "filter": ('metric.type="serviceruntime.googleapis.com/api/request_count" '
                       'AND resource.labels.service="places.googleapis.com"'),
            "interval.startTime": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "interval.endTime": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "aggregation.alignmentPeriod": "86400s",
            "aggregation.perSeriesAligner": "ALIGN_SUM",
            "aggregation.crossSeriesReducer": "REDUCE_SUM",
        },
        headers={"x-goog-user-project": PROJECT},
    )
    if r.status_code != 200:
        # Fail closed: if we cannot read usage, we do not spend.
        sys.exit(f"cannot read usage ({r.status_code}): {r.text[:300]}")
    total = 0
    for series in r.json().get("timeSeries", []):
        for pt in series.get("points", []):
            v = pt.get("value", {})
            total += int(v.get("int64Value") or v.get("doubleValue") or 0)
    return total


def cmd_budget(args):
    used = month_to_date(_session())
    print(json.dumps({"used_this_month": used, "cap": CAP,
                      "remaining": max(0, CAP - used)}, indent=2))


def cmd_search(args):
    s = _session()
    used = month_to_date(s)
    if used >= CAP:
        sys.exit(f"monthly Places cap reached: {used}/{CAP}. Resets on the 1st.")

    today = dt.date.today().isoformat()
    rows, token, calls = [], None, 0

    # Places returns <=20 per call; pull pages until we have `count` or run out.
    # Budget is re-checked each iteration so a big --count can't blow past the
    # cap mid-loop.
    while len(rows) < args.count:
        if used + calls >= CAP:
            print(f"# stopped at monthly cap ({used + calls}/{CAP})", file=sys.stderr)
            break
        body = {"textQuery": args.query,
                "maxResultCount": min(20, args.count - len(rows))}
        if token:
            body["pageToken"] = token
        r = s.post(
            "https://places.googleapis.com/v1/places:searchText",
            headers={"X-Goog-FieldMask": FIELD_MASK + ",nextPageToken",
                     "x-goog-user-project": PROJECT},
            json=body,
        )
        calls += 1
        if r.status_code != 200:
            sys.exit(f"places error ({r.status_code}): {r.text[:400]}")
        payload = r.json()
        page = payload.get("places", [])

        for p in page:
            site = p.get("websiteUri", "")
            # "935 Smithfield Ave, Lincoln, RI 02865, USA" -> "Lincoln"
            parts = [x.strip() for x in p.get("formattedAddress", "").split(",")]
            city = parts[-3] if len(parts) >= 3 else ""
            rows.append({
                "place_id": p.get("id", ""),
                "business_name": p.get("displayName", {}).get("text", ""),
                "type": p.get("primaryTypeDisplayName", {}).get("text", ""),
                "city": city,
                "phone": p.get("nationalPhoneNumber", ""),
                "website": site,
                "has_website": "yes" if site else "no",
                "rating": p.get("rating", ""),
                "review_count": p.get("userRatingCount", ""),
                # lead_score / score_reason stay blank -- Claude fills them with
                # judgment after reading the row. No scoring rules live here.
                "lead_score": "",
                "score_reason": "",
                "status": "new",
                "call_count": 0,
                "last_contact": "",
                "contact_name": "",
                "last_outcome": "",
                "consult_date": "",
                "close_date": "",
                "deal_value": "",
                "source_query": args.query,
                "date_added": today,
                "notes": "",
            })

        token = payload.get("nextPageToken")
        if not token or not page:
            break

    json.dump(rows[:args.count], sys.stdout, indent=2)
    print(f"\n# {len(rows)} results in {calls} call(s) | "
          f"month-to-date was {used}/{CAP}, now ~{used + calls}/{CAP}",
          file=sys.stderr)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("budget", help="month-to-date Places usage vs cap").set_defaults(fn=cmd_budget)

    s = sub.add_parser("search", help="text search, blocked if over monthly cap")
    s.add_argument("query")
    s.add_argument("--count", type=int, default=20,
                   help="how many leads to return; pages at 20 per API call")
    s.set_defaults(fn=cmd_search)

    args = p.parse_args()
    args.fn(args)
