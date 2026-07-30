#!/usr/bin/env python3
"""bcns lead sheet IO.

Auth: you log in as yourself, then impersonate a service account that has the
sheet shared with it. No key file exists -- tokens are minted per run.

    gcloud auth application-default login          # no --scopes, they're blocked
    set -a; . ./.env; set +a

Deliberately dumb: this moves rows in and out of Google and aggregates history.
All judgment -- which businesses qualify, what score, what a note means -- lives
in SKILL.md, not here.
"""
import argparse
import datetime as dt
import json
import os
import sys

# Order is the sheet's column order. Appending a new one is safe; reordering or
# renaming is not -- every existing row would shift under it.
COLUMNS = [
    # identity (from Places, never edited by hand)
    "place_id", "business_name", "type", "city", "phone", "website",
    "has_website", "rating", "review_count",
    # judgment (Claude fills these)
    "lead_score", "score_reason",
    # funnel (you fill these as you work the lead)
    "status", "call_count", "last_contact", "contact_name", "last_outcome",
    "consult_date", "close_date", "deal_value",
    # provenance -- what found this lead and when. This is what lets the skill
    # learn which searches actually produce customers.
    "source_query", "date_added", "notes",
]

STATUSES = ["new", "attempted", "reached", "consult_scheduled",
            "consult_done", "won", "lost", "dead"]

STAGE_RANK = {s: i for i, s in enumerate(STATUSES)}
TERMINAL_LOST = {"lost", "dead"}

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def _client():
    import google.auth
    import gspread
    from google.auth import impersonated_credentials

    sa = os.environ.get("BCNS_SA")
    if not sa:
        sys.exit("set BCNS_SA to the service account email to impersonate")
    # Source creds stay at gcloud's default scopes -- Sheets/Drive scopes are
    # blocked on gcloud's shared client ID, so we request them on the
    # impersonated token instead.
    source, _ = google.auth.default()
    creds = impersonated_credentials.Credentials(
        source_credentials=source,
        target_principal=sa,
        target_scopes=SCOPES,
        lifetime=3600,
    )
    return gspread.authorize(creds)


def _tab(sheet_id):
    return _client().open_by_key(sheet_id).sheet1


def _col(name):
    """1-indexed column number for a column name."""
    return COLUMNS.index(name) + 1


def dedupe(existing_ids, incoming):
    """Drop rows whose place_id is already in the sheet, and dupes within the
    incoming batch itself. Order preserved; rows with no place_id pass through."""
    seen = set(existing_ids)
    out = []
    for row in incoming:
        pid = row.get("place_id")
        if pid and pid in seen:
            continue
        if pid:
            seen.add(pid)
        out.append(row)
    return out


def review_band(n):
    """Coarse review-count buckets. Exact counts never repeat, so they can't
    produce a conversion rate worth reading."""
    try:
        n = int(float(n))
    except (TypeError, ValueError):
        return "unknown"
    if n < 10:
        return "0-9"
    if n < 50:
        return "10-49"
    if n < 200:
        return "50-199"
    return "200+"


def segment_stats(rows, key_fn, min_n=3):
    """Funnel rates per segment. Segments below min_n are returned but flagged:
    a 1-for-1 segment is noise, and acting on it is how you chase a pattern that
    was one lucky call."""
    buckets = {}
    for r in rows:
        # Case/whitespace-normalised: Places returns "Plumber" while a
        # hand-typed row says "plumber", and split segments hide real rates.
        k = str(key_fn(r) or "").strip().lower()
        if not k:
            continue
        b = buckets.setdefault(k, {"n": 0, "worked": 0, "reached": 0,
                                   "consults": 0, "won": 0})
        b["n"] += 1
        status = str(r.get("status", "")).strip()
        rank = STAGE_RANK.get(status, -1)
        if rank > STAGE_RANK["new"]:
            b["worked"] += 1
        if status not in TERMINAL_LOST:
            if rank >= STAGE_RANK["reached"]:
                b["reached"] += 1
            if rank >= STAGE_RANK["consult_done"]:
                b["consults"] += 1
        if status == "won":
            b["won"] += 1
    out = []
    for k, b in buckets.items():
        out.append({
            "segment": k, "n": b["n"], "worked": b["worked"],
            "reached": b["reached"], "consults": b["consults"], "won": b["won"],
            # Rate is over WORKED leads, not all leads. Dividing by untouched
            # rows makes every segment look like it fails.
            "win_rate": round(b["won"] / b["worked"], 3) if b["worked"] else None,
            "enough_data": b["worked"] >= min_n,
        })
    return sorted(out, key=lambda x: (-(x["win_rate"] or 0), -x["worked"]))


def cmd_init(args):
    """Write headers into a sheet YOU already own and shared with the SA.

    We don't create the spreadsheet here on purpose: a file created by a service
    account is owned by that service account, lands in a Drive you can't browse,
    and service accounts have no storage quota (storageQuotaExceeded).
    """
    ws = _tab(args.sheet_id)
    existing = ws.get_all_values()
    if len(existing) > 1 and not args.force:
        sys.exit(f"sheet has {len(existing) - 1} data rows; refusing to rewrite "
                 "headers without --force")
    ws.update(values=[COLUMNS], range_name="A1")
    ws.freeze(rows=1)
    print(json.dumps({"headers": COLUMNS, "count": len(COLUMNS)}, indent=2))


def cmd_format(args):
    """Dropdowns, colour rules, widths. Idempotent -- safe to re-run."""
    ss = _client().open_by_key(args.sheet_id)
    ws = ss.sheet1
    gid = ws.id
    n_rows = 2000

    def dropdown(col_name, values):
        return {"setDataValidation": {
            "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": n_rows,
                      "startColumnIndex": _col(col_name) - 1,
                      "endColumnIndex": _col(col_name)},
            "rule": {"condition": {"type": "ONE_OF_LIST",
                                   "values": [{"userEnteredValue": v} for v in values]},
                     "showCustomUi": True, "strict": False}}}

    def status_colour(value, rgb):
        return {"addConditionalFormatRule": {"rule": {
            "ranges": [{"sheetId": gid, "startRowIndex": 1, "endRowIndex": n_rows,
                        "startColumnIndex": _col("status") - 1,
                        "endColumnIndex": _col("status")}],
            "booleanRule": {
                "condition": {"type": "TEXT_EQ",
                              "values": [{"userEnteredValue": value}]},
                "format": {"backgroundColor": rgb}}}, "index": 0}}

    reqs = [
        {"repeatCell": {
            "range": {"sheetId": gid, "startRowIndex": 0, "endRowIndex": 1},
            "cell": {"userEnteredFormat": {
                "textFormat": {"bold": True,
                               "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
                "backgroundColor": {"red": .17, "green": .24, "blue": .31}}},
            "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
        {"updateSheetProperties": {
            "properties": {"sheetId": gid,
                           "gridProperties": {"frozenRowCount": 1,
                                              "frozenColumnCount": 2}},
            "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}},
        dropdown("status", STATUSES),
        dropdown("has_website", ["yes", "no"]),
        {"addConditionalFormatRule": {"rule": {
            "ranges": [{"sheetId": gid, "startRowIndex": 1, "endRowIndex": n_rows,
                        "startColumnIndex": _col("lead_score") - 1,
                        "endColumnIndex": _col("lead_score")}],
            "gradientRule": {
                "minpoint": {"color": {"red": .96, "green": .80, "blue": .80},
                             "type": "NUMBER", "value": "1"},
                "midpoint": {"color": {"red": 1, "green": .95, "blue": .75},
                             "type": "NUMBER", "value": "5"},
                "maxpoint": {"color": {"red": .78, "green": .93, "blue": .79},
                             "type": "NUMBER", "value": "10"}}}, "index": 0}},
        status_colour("won", {"red": .71, "green": .88, "blue": .72}),
        status_colour("consult_scheduled", {"red": .78, "green": .87, "blue": .97}),
        status_colour("consult_done", {"red": .78, "green": .87, "blue": .97}),
        status_colour("reached", {"red": 1, "green": .95, "blue": .70}),
        status_colour("lost", {"red": .88, "green": .88, "blue": .88}),
        status_colour("dead", {"red": .88, "green": .88, "blue": .88}),
        {"repeatCell": {
            "range": {"sheetId": gid, "startRowIndex": 1, "endRowIndex": n_rows,
                      "startColumnIndex": _col("last_contact") - 1,
                      "endColumnIndex": _col("close_date")},
            "cell": {"userEnteredFormat": {
                "numberFormat": {"type": "DATE", "pattern": "yyyy-mm-dd"}}},
            "fields": "userEnteredFormat.numberFormat"}},
        {"autoResizeDimensions": {"dimensions": {
            "sheetId": gid, "dimension": "COLUMNS",
            "startIndex": 0, "endIndex": len(COLUMNS)}}},
    ]
    # Sentence-length columns: autoresize makes these absurdly wide.
    for name, px in [("notes", 320), ("last_outcome", 320),
                     ("score_reason", 260), ("website", 200)]:
        reqs.append({"updateDimensionProperties": {
            "range": {"sheetId": gid, "dimension": "COLUMNS",
                      "startIndex": _col(name) - 1, "endIndex": _col(name)},
            "properties": {"pixelSize": px}, "fields": "pixelSize"}})

    ss.batch_update({"requests": reqs})
    print(json.dumps({"formatted": True, "columns": len(COLUMNS),
                      "dropdowns": ["status", "has_website"]}, indent=2))


def cmd_read(args):
    print(json.dumps(_tab(args.sheet_id).get_all_records(), indent=2))


def cmd_ids(args):
    """Just the place_ids -- cheap dedupe check before spending Places calls."""
    print(json.dumps(
        [v for v in _tab(args.sheet_id).col_values(_col("place_id"))[1:] if v]))


def cmd_append(args):
    rows = json.load(sys.stdin)
    if isinstance(rows, dict):
        rows = [rows]
    ws = _tab(args.sheet_id)
    fresh = dedupe(ws.col_values(_col("place_id"))[1:], rows)
    if not fresh:
        print(json.dumps({"appended": 0, "skipped": len(rows)}))
        return
    ws.append_rows([[r.get(c, "") for c in COLUMNS] for r in fresh],
                   value_input_option="USER_ENTERED")
    print(json.dumps({"appended": len(fresh), "skipped": len(rows) - len(fresh)}))


def _find_row(ws, place_id):
    ids = ws.col_values(_col("place_id"))
    try:
        return ids.index(place_id) + 1
    except ValueError:
        sys.exit(f"place_id not found: {place_id}")


def _write_fields(ws, row, fields):
    import gspread
    ws.batch_update([
        {"range": gspread.utils.rowcol_to_a1(row, _col(k)), "values": [[v]]}
        for k, v in fields.items()
    ], value_input_option="USER_ENTERED")


def cmd_update(args):
    """Set named columns on the row matching a place_id."""
    ws = _tab(args.sheet_id)
    row = _find_row(ws, args.place_id)
    fields = json.loads(args.fields)
    bad = [k for k in fields if k not in COLUMNS]
    if bad:
        sys.exit(f"unknown column(s): {bad}")
    _write_fields(ws, row, fields)
    print(json.dumps({"row": row, "updated": list(fields)}))


def cmd_log(args):
    """Record a contact attempt: bumps call_count, stamps the date, advances
    status. Separate from `update` because call_count is read-modify-write, and
    doing that by hand is how counts silently stop incrementing."""
    ws = _tab(args.sheet_id)
    row = _find_row(ws, args.place_id)
    try:
        count = int(ws.cell(row, _col("call_count")).value or 0)
    except ValueError:
        count = 0

    fields = {"call_count": count + 1,
              "last_contact": args.date or dt.date.today().isoformat()}
    if args.status:
        if args.status not in STATUSES:
            sys.exit(f"status must be one of {STATUSES}")
        fields["status"] = args.status
    if args.contact_name:
        fields["contact_name"] = args.contact_name
    if args.outcome:
        fields["last_outcome"] = args.outcome

    _write_fields(ws, row, fields)
    print(json.dumps({"row": row, "call_count": count + 1, "set": list(fields)}))


def cmd_stats(args):
    """Conversion by segment -- what the skill reads before scoring anything.

    This is the entire self-improvement mechanism: outcomes you type into the
    sheet become the evidence for the next round's scoring. No model, no stored
    weights, nothing to go stale -- recomputed from the sheet on every run.
    """
    rows = _tab(args.sheet_id).get_all_records()
    worked = [r for r in rows
              if STAGE_RANK.get(str(r.get("status", "")).strip(), 0) > 0]
    print(json.dumps({
        "total_leads": len(rows),
        "worked": len(worked),
        "untouched": len(rows) - len(worked),
        "by_type": segment_stats(rows, lambda r: str(r.get("type", "")).strip()),
        "by_city": segment_stats(rows, lambda r: str(r.get("city", "")).strip()),
        "by_has_website": segment_stats(
            rows, lambda r: str(r.get("has_website", "")).strip()),
        "by_review_band": segment_stats(
            rows, lambda r: review_band(r.get("review_count"))),
        "by_source_query": segment_stats(
            rows, lambda r: str(r.get("source_query", "")).strip()),
    }, indent=2))


def _self_check():
    assert dedupe(["a"], [{"place_id": "a"}]) == []
    assert dedupe(["a"], [{"place_id": "b"}]) == [{"place_id": "b"}]
    assert dedupe([], [{"place_id": "c"}, {"place_id": "c"}]) == [{"place_id": "c"}]
    assert dedupe(["a"], [{"business_name": "x"}]) == [{"business_name": "x"}]
    assert len(set(COLUMNS)) == len(COLUMNS), "duplicate column name"

    assert review_band(0) == "0-9" and review_band(9) == "0-9"
    assert review_band(10) == "10-49" and review_band(199) == "50-199"
    assert review_band(200) == "200+" and review_band("") == "unknown"
    assert review_band("212") == "200+", "Sheets returns counts as strings"

    s = segment_stats([{"type": "plumber", "status": "won"},
                       {"type": "plumber", "status": "lost"},
                       {"type": "hvac", "status": "new"}], lambda r: r["type"])
    plumber = next(x for x in s if x["segment"] == "plumber")
    assert plumber["n"] == 2 and plumber["won"] == 1 and plumber["win_rate"] == 0.5
    hvac = next(x for x in s if x["segment"] == "hvac")
    assert hvac["won"] == 0 and hvac["enough_data"] is False, "n=1 must be flagged"

    # 20 leads nobody called is NOT evidence that the segment fails. win_rate
    # must be None (unknown), not 0.0, and enough_data must be False.
    untouched = segment_stats([{"t": "x", "status": "new"}] * 20, lambda r: r["t"])[0]
    assert untouched["n"] == 20 and untouched["worked"] == 0
    assert untouched["win_rate"] is None, "no calls means unknown, not zero"
    assert untouched["enough_data"] is False, "population is not evidence"
    # rate divides by worked, not by n
    partial = segment_stats(
        [{"t": "y", "status": "won"}] + [{"t": "y", "status": "new"}] * 9,
        lambda r: r["t"])[0]
    assert partial["win_rate"] == 1.0, "1 of 1 worked, not 1 of 10 present"

    # lost/dead sort after 'reached' in STATUSES; they must not be counted as
    # having reached the customer, or every dead lead inflates the contact rate.
    lost = segment_stats([{"t": "x", "status": "lost"}], lambda r: r["t"])[0]
    assert lost["reached"] == 0 and lost["consults"] == 0
    won = segment_stats([{"t": "x", "status": "won"}], lambda r: r["t"])[0]
    assert won["reached"] == 1 and won["consults"] == 1, "a win passed every stage"

    # Places says "Plumber", a typed row says " plumber " -- one segment, not three
    mixed = segment_stats([{"t": "Plumber", "status": "won"},
                           {"t": " plumber ", "status": "new"},
                           {"t": "plumber", "status": "new"}], lambda r: r["t"])
    assert len(mixed) == 1 and mixed[0]["n"] == 3, "segments must case-normalise"
    print("ok")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="write headers into a sheet you own")
    s.add_argument("sheet_id")
    s.add_argument("--force", action="store_true",
                   help="rewrite headers even with data present")
    s.set_defaults(fn=cmd_init)

    for name, fn, helptext in [
        ("format", cmd_format, "dropdowns, colour rules, column widths"),
        ("read", cmd_read, "all rows as JSON"),
        ("ids", cmd_ids, "existing place_ids"),
        ("append", cmd_append, "append rows from stdin JSON, deduped"),
        ("stats", cmd_stats, "conversion by segment — read before scoring"),
    ]:
        s = sub.add_parser(name, help=helptext)
        s.add_argument("sheet_id")
        s.set_defaults(fn=fn)

    s = sub.add_parser("update", help='e.g. update ID pid \'{"status":"won"}\'')
    s.add_argument("sheet_id")
    s.add_argument("place_id")
    s.add_argument("fields")
    s.set_defaults(fn=cmd_update)

    s = sub.add_parser("log", help="record a contact attempt (bumps call_count)")
    s.add_argument("sheet_id")
    s.add_argument("place_id")
    s.add_argument("--status", help=f"one of {STATUSES}")
    s.add_argument("--contact_name")
    s.add_argument("--outcome", help="what they said")
    s.add_argument("--date", help="defaults to today")
    s.set_defaults(fn=cmd_log)

    sub.add_parser("check", help="offline self-test").set_defaults(
        fn=lambda a: _self_check())

    args = p.parse_args()
    args.fn(args)
