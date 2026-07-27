---
topic: force-directed-graph-astro
updated: 2026-07-26
sources: [https://bundlephobia.com/package/d3-force, https://bundlephobia.com/package/cytoscape, https://bundlephobia.com/package/sigma, https://bundlephobia.com/package/graphology, https://docs.astro.build/en/guides/client-side-scripts/, https://registry.npmjs.org/d3-force]
---
## Recommendation
`d3-force@3.0.0` (headless simulation only) + hand-rolled `<canvas>` render/drag/zoom/hit-test, imported inside a normal (non-`is:inline`) `<script>` in the `.astro` page.
Smallest correct choice: d3-force is 5.7KB gzipped, battle-tested (Barnes-Hut quadtree repulsion, stable integrator), and replaces the risky part of the "no-dep" Verlet loop (physics correctness) while keeping bundle weight near-zero. At 200-600 nodes / 400-1500 edges this beats cytoscape/sigma on both size and complexity.

## Rejected Alternatives
- cytoscape@3.34.0 + built-in `cose` layout (no separate fcose ext needed, cose ships in core) — 430KB min / 134KB gzip, overkill for click+drag+zoom only; cytoscape-fcose (2.2.0, npm pkg 3yr stale but stable/maintained via GitHub) adds more weight for a nicer layout you don't need.
- sigma@3.0.3 (WebGL) + graphology@0.26 + graphology-layout-forceatlas2 — ~26KB + ~13KB + a few KB gzip (~40KB total), reasonable but still 7x d3-force; sigma v4 is alpha-only (4.0.0-alpha.5), not production-ready.
- Pure hand-rolled Verlet/force loop, zero deps — smallest bundle (0KB) but you own physics-stability bugs (jitter/explosion at 600 nodes, no spatial partitioning) for a save of ~5.7KB gzip; not worth it.

## Version / Deprecation / CVE Notes
- d3-force latest = 3.0.0 (dist-tags.latest confirmed via npm registry), no newer major, no open CVEs known. Pure ESM, zero DOM/Node access at import time — SSR-safe by construction.
- cytoscape 3.34.0 latest (active, 2mo old release). sigma 3.0.3 latest stable; v4 alpha exists, skip it.
- graphology 0.26.x still pre-1.0 but de facto stable and required by sigma.

## Integration Notes
- Install target: `dependencies`, not `devDependencies` (this project's @astrojs/node standalone build omits devDeps at build time).
- `npm install d3-force@3.0.0` — named ESM imports: `forceSimulation, forceManyBody, forceLink, forceCenter, forceCollide`.
- In the `.astro` page use a plain `<script>` (NOT `is:inline`) so Vite bundles/resolves the `import` and it still only ever runs client-side — Astro never executes non-inline `<script>` during SSR regardless.
- `is:inline` would break this: it skips Astro's import resolution, so a bare `import 'd3-force'` won't resolve without a CDN URL/import map — avoid it here.
- Run `forceSimulation` headless (no d3-selection/d3-drag/d3-zoom needed): draw nodes/edges yourself on `<canvas>` each `tick`, hand-roll pointer listeners for drag (update `fx/fy`) and wheel/pinch for a manual pan/zoom transform, and do click hit-testing with a simple O(n) distance check (trivial at ≤600 nodes).
- Perf cliff: `simulation.alphaDecay()` default (~0.0228) is fine to 600 nodes; if it feels sluggish, raise `alphaDecay` to ~0.05 (converges faster, fewer ticks) and/or cap ticks manually (`simulation.stop()` after N ticks or once `alpha < 0.01`). Canvas, not SVG, is required at this node count — SVG DOM churn per tick is the actual cliff, not d3-force's math.
- Graceful degradation: Astro page already SSR-fetches `{ok,nodes,edges}` from `/api/graph` server-side — render a plain `<ul>`/table of node links (to the note viewer) in the HTML by default; client script wraps init in try/catch and only hides/replaces that list with the canvas on successful mount. No JS → list stays visible.
