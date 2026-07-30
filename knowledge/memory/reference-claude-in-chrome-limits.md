---
name: reference-claude-in-chrome-limits
description: Claude-in-Chrome MCP extension hard constraints — tab visibility, file:// block, and the stable deviceId→profile mapping
metadata: 
  node_type: memory
  type: reference
  originSessionId: e9cc0f22-a17b-492f-abcb-ce5ad201bab9
  modified: 2026-07-30T16:12:00.000Z
---

Three hard constraints found across multiple sessions using the Claude-in-Chrome extension:

1. **Tab visibility:** The extension can only see tabs inside the Chrome window it controls. Tabs in other windows and user-defined tab groups are invisible. Fix: drag tabs into the extension's controlled window before starting the automation loop.

2. **`file://` URLs are blocked:** The extension cannot navigate to or read local files via `file://`. Serve local HTML over HTTP instead — `python3 -m http.server <port>`, then navigate to `http://localhost:<port>`.

3. **The extension is per Chrome profile, and so is every login.** Each profile is a separate cookie jar and needs its own install; only profiles with the extension appear in `list_connected_browsers`. Nate has at least two — the default (personal, `nseluga@g.hmc.edu`) and **"Work Profile"** (`nseluga@bcn-services.com`, which owns the bcns Vercel team — see [[reference-bcns-platform-vercel]]). Wrong profile = logged into the wrong account with no way to reach the right one from that session. Fix: install the extension in the target profile, then `switch_browser` and click Connect there. Dragging tabs does *not* help across profiles — only across windows of the same profile.

4. **The two profiles' deviceIds (stable identifiers — the display names are not).**
   `list_connected_browsers` shows "Browser 1"/"Browser 2" and the labels reshuffle
   on every reconnect; Nate has re-named them 5+ times and it never persists,
   because the naming lives in the extension, not anywhere Claude can write.
   Stop relying on names — use the deviceId:

   | deviceId | Profile | Google account |
   |---|---|---|
   | `6ebf38dd-c2de-467a-9bf6-36624fd49d9c` | **School Profile** (default/personal) | nseluga@g.hmc.edu |
   | `c00a1f24-e61f-40be-ac13-0ec584afc72e` | **Work Profile** | nseluga@bcn-services.com |

   Verified 2026-07-30 by `select_browser` → `https://myaccount.google.com` →
   read the signed-in address. `chrome://version` is blocked by the extension,
   so the signed-in account is the only usable profile fingerprint.
   **Re-verify with that same one-step check if a deviceId is ever unknown** —
   and re-record here if these ever rotate.

**How to apply:** Flag all three at the start of any Claude-in-Chrome session involving multiple tabs, local files, or an account-scoped web app. When a dashboard shows the wrong account, check the profile before assuming the URL or slug is wrong — a 404 on a team URL usually means wrong login, not a bad path.
