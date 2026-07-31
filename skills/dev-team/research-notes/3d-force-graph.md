---
topic: 3d-force-graph
updated: 2026-07-31
sources: [https://registry.npmjs.org/3d-force-graph, https://bundlephobia.com/package/3d-force-graph@1.80.0, https://github.com/vasturiano/3d-force-graph, https://unpkg.com/3d-force-graph@1.80.0/dist/3d-force-graph.d.ts, https://github.com/vasturiano/d3-force-3d/blob/master/src/link.js, https://github.com/vasturiano/three-forcegraph/issues/40, https://threejs.org/manual/en/webgl-compatibility-check.html]
---
## Recommendation
`3d-force-graph@1.80.0` (current latest, active, released 2026-04-05) — only if the 3D/orbit requirement is real; it is ~336KB gzip / ~1.23MB min all-in (three.js is a hard `dependency`, not peer, so it always bundles). See `force-directed-graph-astro.md` for the 2D sibling decision this repo already made for a graph at this scale.

## Rejected Alternatives
- `force-graph` (2D, same author, same API family) — 57KB gzip all-in; only rejected if 3D/orbit is a real requirement, otherwise this beats 3d-force-graph 6x on weight for click/hover/drag.
- `react-force-graph` — N/A, no React in this repo.
- Raw `three` + `d3-force`/`d3-force-3d` hand-rolled — smallest 3D option (three alone is 178KB gzip) but you own camera controls, node meshes, hit-testing, resize; only worth it if 3D is required AND you don't need node/link accessor sugar.
- 3d-force-graph with `three` externalized via Vite `build.rollupOptions.external` + global THREE — saves nothing in *this* app (single page, no other three.js consumer to share the CDN copy with) and adds real Vite config risk; not worth it here.

## Version / Deprecation / CVE Notes
- `3d-force-graph@1.80.0` latest (npm dist-tags), released 2026-04-05, repo pushed same day, not archived, 6.2k stars — actively maintained.
- Hard `dependencies` (auto-installed, count toward bundle): `three` `>=0.179 <1` (latest 0.185.1, active), `three-forcegraph` `1` (1.43.4), `three-render-objects` `^1.41` (1.42.0), `kapsule` `^1.16` (1.16.3, stable/slow-moving), `accessor-fn` `1` (1.5.3, stable/slow-moving). No `peerDependencies` declared at the top-level package — three is NOT something the app installs separately, npm pulls a real copy in automatically.
- Transitively via `three-forcegraph`: `d3-force-3d` (3.0.6), `ngraph.forcelayout`/`ngraph.graph`, `d3-scale`, `d3-scale-chromatic`, `tinycolor2`, `data-bind-mapper` — all pulled in regardless of which force engine you use.
- No open CVEs known on any of these as of this check.

## Integration Notes
- `new ForceGraph3D(domElement, configOptions)` mounts immediately, no separate `.mount()`. Ships its own `.d.ts` (`types: dist/3d-force-graph.d.ts` in package.json) — no `@types/*` needed.
- `graphData({nodes, links})`: link endpoints are `source`/`target` (id strings by default, `nodeId()` to customize). **Mutates in place** — d3-force-3d's `forceLink` resolves string ids to live node object refs on the link objects, and adds `x/y/z/vx/vy/vz/index` onto every node object, same as classic d3-force.
- **Missing node id in a link THROWS**, does not warn or drop: `d3-force-3d`'s internal `find()` does `if (!node) throw new Error("node not found: " + nodeId)` — confirmed in source. Filter/validate links against the node id set before calling `graphData()`.
- Styling: `nodeColor`/`nodeVal`/`nodeLabel`/`nodeAutoColorBy`/`nodeOpacity` per-node; `linkColor`/`linkWidth`/`linkVisibility`/`linkAutoColorBy` per-link (independent accessor per link, so two edge kinds is just a function keyed on link data). Hiding a subset: prefer `linkVisibility(fn)` (keeps physics, hides render) over re-setting `graphData` (cheaper, no re-layout).
- `nodeLabel`/`linkLabel` accept **plain text, HTML string, or HTMLElement** — HTML string is rendered as raw HTML in the tooltip (XSS surface if labels come from untrusted/filename input; sanitize or pass an HTMLElement with `.textContent` set instead of a string).
- `onNodeClick((node, event) => {})` — passes the mutated node object (with live x/y/z) and the MouseEvent.
- Default controls: `controlType('trackball'|'orbit'|'fly')`, default `'trackball'` (free rotate, no fixed up-vector — set `'orbit'` if you want a locked up-axis). `camera()` returns the live `THREE.Camera`, `controls()` returns the live controls object, `scene()` returns the live `THREE.Scene`, `renderer()` returns the `THREE.WebGLRenderer`.
- **Seam for later per-frame/glow work**: `onEngineTick(fn)`/`onEngineStop(fn)` fire on simulation ticks (not animation frames); for animation-frame-driven camera/rotation work, drive it yourself from `requestAnimationFrame` and read/write `camera()` directly (e.g. orbit by mutating `camera().position` and calling `controls().update()`), or use `cameraPosition({x,y,z}, lookAt, transitionMs)` for eased moves. For brightness/glow, there's no top-level `nodeEmissive` accessor — use `nodeThreeObject(node => custom THREE.Mesh with MeshStandardMaterial({emissive}))` per node, or grab `lights()`/`scene()` and mutate material/light properties directly each frame.
- No documented public dispose in the README, but the `.d.ts` exposes `_destructor(): void` on the instance — call it on teardown to release the renderer/context. Known memory-leak reports exist when swapping `graphData` repeatedly without disposing old geometries/materials (vasturiano/3d-force-graph#255) — expect this if the page ever re-renders the graph instead of mounting once.
- `width()`/`height()` default to **window** size, not the parent container — with a `pl-16` gutter and a fixed-height box you must explicitly set both (and re-set on resize; there's no built-in ResizeObserver) or the canvas overflows/misaligns.
- WebGL absence: the library does not pre-flight-check; `THREE.WebGLRenderer` construction throws an uncaught exception if no context is obtainable — wrap construction in try/catch. Skip three's `WebGL.js` addon import just for the boolean; the native one-liner `!!document.createElement('canvas').getContext('webgl2')` (fallback `'webgl'`) is enough and costs nothing.
- SSR: `three-forcegraph` has a known `window is not defined` issue when imported/constructed during Node SSR (vasturiano/three-forcegraph#40) — confirms real hazard if evaluated server-side. Not an issue here only because Astro never executes non-`is:inline` `<script>` blocks during SSR at all (same guarantee the d3-force note already relies on).
