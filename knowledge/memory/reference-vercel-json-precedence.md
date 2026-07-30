---
name: reference-vercel-json-precedence
description: "Vercel gotcha — vercel.json overrides dashboard settings, and its paths resolve relative to Root Directory (monorepo double-nesting)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: e9cc0f22-a17b-492f-abcb-ce5ad201bab9
  modified: 2026-07-30T01:42:42.861Z
---

Two Vercel behaviors that together cost a full debugging session on 2026-07-29
(`bcns-landing`, see [[reference-bcns-platform-vercel]]):

1. **`vercel.json` beats project settings.** Clearing an override in the
   dashboard does nothing if `vercel.json` still sets it. Proven the hard way:
   cleared the Output Directory override, redeployed the same commit, got a
   byte-identical failure. The file has to be changed and **pushed**.

2. **Paths in `vercel.json` resolve relative to Root Directory**, not the repo
   root. With Root Directory = `apps/web`, an `outputDirectory` of
   `"apps/web/.next"` becomes `/vercel/path0/apps/web/apps/web/.next`:

   ```
   The Next.js output directory "apps/web/.next" was not found at
   "/vercel/path0/apps/web/apps/web/.next"
   ```

For a Next.js app in a pnpm monorepo, the supported setup is Root Directory =
the app dir with **no** `vercel.json` and no `outputDirectory` override — let
the framework preset do it.

**Why:** this failure mode looks like a build error but the build succeeds; it
dies at the final output-directory check, so build logs read clean until the
last line. A local `pnpm build` always passes and proves nothing.

**How to apply:** when a Vercel deploy fails but the code builds locally, read
the real build log before theorizing — the dashboard's Build & Deployment
fields hydrate late, so an accessibility-tree read can report them empty when
they're actually set. Screenshot/zoom to confirm. Then check `vercel.json` and
Root Directory together, never separately.
