---
name: reference-claude-in-chrome-limits
description: "Claude-in-Chrome MCP extension hard constraints — tab visibility and file:// URL block"
metadata:
  type: reference
---

Two hard constraints found across multiple sessions using the Claude-in-Chrome extension:

1. **Tab visibility:** The extension can only see tabs inside the Chrome window it controls. Tabs in other windows and user-defined tab groups are invisible. Fix: drag tabs into the extension's controlled window before starting the automation loop.

2. **`file://` URLs are blocked:** The extension cannot navigate to or read local files via `file://`. Serve local HTML over HTTP instead — `python3 -m http.server <port>`, then navigate to `http://localhost:<port>`.

**How to apply:** Flag both constraints at the start of any Claude-in-Chrome session that involves multiple tabs or local files, so the user can set up the window correctly before the loop begins.
