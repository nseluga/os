---
topic: astro-markdown-ssr
updated: 2026-07-25
sources: [https://www.npmjs.com/package/@astrojs/markdown-remark, https://www.npmjs.com/package/rehype-sanitize, https://github.com/withastro/roadmap/discussions/1094, https://www.npmjs.com/package/marked, https://www.npmjs.com/package/markdown-it, https://www.npmjs.com/package/unist-util-visit]
---
## Recommendation
`@astrojs/markdown-remark` v7.2.1 (Astro's own public markdown-to-HTML package, same unified/remark/rehype pipeline Astro uses for `.md` content collections) + `rehype-sanitize` v6.0.0 for sanitization + a hand-rolled ~15-line remark plugin (using `unist-util-visit`) for wikilinks. First-party, version-locked to installed Astro (7.1.3 in this repo), avoids the fragmented/unmaintained wikilink-plugin ecosystem entirely.

## Rejected Alternatives
- `marked`/`markdown-it` alone — lighter, but you'd hand-assemble sanitization + wikilinks yourself with no AST guarantee against touching code fences unless you write custom tokenizer extensions anyway; no benefit over the Astro-native pipeline here.
- `remark-wiki-link` / `markdown-it-wikilinks` (and their ~5 competing forks) — ecosystem is fragmented, most originals 3+ years stale; forks like `remark-wiki-link-plus`/`markdown-it-wikilinks-plus` exist but add a dependency for something a 15-line visitor does directly.
- `experimental_AstroContainer` / `astro:content` render — wrong tool class: Container API renders Astro *components*, `astro:content` render() requires a content-collection entry backed by a project-local loader; neither converts an arbitrary external markdown string.
- Zero-dependency hand-rolled parser — ruled out per task constraint; correct GFM tables + nested lists are real parsing complexity, not worth reinventing.

## Version / Deprecation / CVE Notes
- `@astrojs/markdown-remark` 7.2.1, `astro` 7.1.3, `rehype-sanitize` 6.0.0 (3yr old but stable/compatible with unified 11/hast 3), `marked` 18.0.7, `markdown-it` 14.3.0 — all current as of 2026-07.
- unified/remark/rehype v11+ line is ESM-only (`"type":"module"` required) — fine, repo is already ESM. `@astrojs/markdown-remark` matches.
- `markdown-it` ships dual ESM/CJS exports; `marked` is ESM-only (`type: module`) as of v18.

## Integration Notes
- Install: `npm install @astrojs/markdown-remark rehype-sanitize unist-util-visit` — put in `dependencies`, not devDeps (this repo's standalone-build precedent). Verify with `npm run build && node dist/server/entry.mjs` before trusting it.
- Create the processor ONCE at module scope (top-level in e.g. `src/lib/markdown.ts`), reuse across requests — `createMarkdownProcessor()` is async setup work, not free; do not call it per-request.
- Set `syntaxHighlight: false` for MVP — default is Shiki, which dynamic-imports grammars (classic standalone-bundle footgun) and injects inline `style`/`class` attrs that break `rehype-sanitize`'s default schema unless extended. Plain `<pre><code>` is fine for a notes browser; revisit later.
- `gfm: true` is the default — tables/strikethrough/autolinks work with zero config.
- Sanitize: `rehypePlugins: [[rehypeSanitize, defaultSchema]]` (import `defaultSchema` from `rehype-sanitize`). Warranted here — `rehype-raw` (already in the pipeline) passes inline HTML in notes straight through to `set:html`; cheap 1-package insurance against a stray `<script>`/`<iframe>` in old pasted note content, not paranoia.
- Wikilinks: write a remark plugin — `visit(tree, 'text', (node) => { /* split on [[...]], build link mdast nodes */ })` using `unist-util-visit`. Operates only on `text` mdast nodes, so code-fence content (a distinct node type) is never touched — correctly avoids the "regex over raw markdown matches inside code fences" trap without needing a wikilink package.
- Tree listing (<500ms) is unrelated to the renderer choice — it's a filesystem walk + `gray-matter` frontmatter parse (already a dep, regex-based, cheap); don't invoke the markdown processor for the listing page at all.
