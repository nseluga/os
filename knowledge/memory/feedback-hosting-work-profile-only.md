---
name: feedback-hosting-work-profile-only
description: "All hosting/domain/deploy management via Claude in Chrome must happen in Nate's WORK Chrome profile, never the school profile"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e9cc0f22-a17b-492f-abcb-ce5ad201bab9
  modified: 2026-07-30T02:52:02.991Z
---

Any hosting management done through Claude in Chrome — Vercel, Squarespace/DNS,
registrars, deploy dashboards — must happen in Nate's **work** Chrome profile
only. Never open or drive these in the school profile.

**Why:** work infrastructure (the `bcns` Vercel team, `bcn-services.com` DNS,
Google Workspace) belongs to the bcn-services.com identity and must stay
separated from his school/personal profile. Nate had to interrupt twice on
2026-07-29 because tabs kept being created in the school window.

**How to apply:** do not infer the profile from a `list_connected_browsers`
deviceId or display name — the labels reshuffle as extensions connect, and a
work-account session (e.g. the `bcns` Vercel team) can exist in the school
profile too, so a logged-in dashboard is NOT proof of the right profile. Confirm
the window explicitly before acting: call `switch_browser` and have Nate click
Connect in the work window, or ask him directly. If tabs end up in the wrong
window, close them. See [[reference-claude-in-chrome-limits]] (extension is per
profile) and [[reference-bcns-platform-vercel]] (which accounts own what).
