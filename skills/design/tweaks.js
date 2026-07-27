/* Drop-in tweaks panel — no deps, no build, no model round-trip.
 *
 *   <script>window.TWEAKS = [ {var:'--accent', label:'Accent', type:'color'}, ... ]</script>
 *   <script src="tweaks.js"></script>
 *
 * Every control writes a CSS custom property on :root. Style the page off those
 * properties and the panel drives the whole design live. Declare TWEAKS yourself —
 * list the faces the page actually loaded and the variables it actually uses. The
 * defaults below are a fallback, not a contract.
 *
 * "Copy CSS" puts the current values on the clipboard as a :root block. That is how
 * a tweaking session gets baked back into the source.
 */
(() => {
  if (window.__tweaks) return;
  window.__tweaks = 1;

  const root = document.documentElement;
  const specs = window.TWEAKS || [
    { var: '--font-display', label: 'Heading font', type: 'select',
      options: ['ui-serif, Georgia, serif', 'ui-sans-serif, system-ui, sans-serif', 'ui-monospace, monospace'] },
    { var: '--font-body', label: 'Body font', type: 'select',
      options: ['ui-sans-serif, system-ui, sans-serif', 'ui-serif, Georgia, serif', 'ui-monospace, monospace'] },
    { var: '--type-scale', label: 'Type scale', type: 'range', min: 0.8, max: 1.4, step: 0.01 },
    { var: '--accent', label: 'Accent', type: 'color' },
    { var: '--space-scale', label: 'Spacing', type: 'range', min: 0.7, max: 1.6, step: 0.02 },
    { var: '--radius', label: 'Radius', type: 'range', min: 0, max: 28, step: 1, unit: 'px' },
    { var: '--motion', label: 'Motion weight', type: 'range', min: 0, max: 2, step: 0.05 },
    { var: '--reveal', label: 'Reveal distance', type: 'range', min: 0, max: 80, step: 1, unit: 'px' },
  ];

  const KEY = 'tweaks:' + location.pathname;
  let state = {};
  try { state = JSON.parse(localStorage.getItem(KEY)) || {}; } catch { state = {}; }

  // Starting value: whatever the user already set, else whatever the page declares.
  const base = {};
  for (const s of specs) base[s.var] = getComputedStyle(root).getPropertyValue(s.var).trim();
  const value = (s) => state[s.var] ?? base[s.var] ?? '';

  const toCss = (o) => ':root {\n' +
    Object.entries(o).map(([k, v]) => `  ${k}: ${v};`).join('\n') + '\n}';

  const apply = () => {
    for (const [k, v] of Object.entries(state)) root.style.setProperty(k, v);
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch {}
  };

  const host = document.createElement('div');
  host.style.cssText = 'position:fixed;right:16px;bottom:16px;z-index:2147483647';
  // Shadow root so the draft's own global CSS cannot reach in and restyle the panel.
  const sh = host.attachShadow({ mode: 'open' });
  sh.innerHTML = `<style>
    :host{all:initial}
    *{box-sizing:border-box;font:12px/1.4 ui-sans-serif,system-ui,sans-serif;color:#e8e8ea}
    button{background:#1c1c1f;border:1px solid #34343a;color:#e8e8ea;border-radius:6px;
      padding:6px 10px;cursor:pointer}
    button:hover{background:#26262b}
    #panel{width:280px;max-height:70vh;overflow:auto;background:#141416;border:1px solid #34343a;
      border-radius:10px;padding:12px;margin-bottom:8px;box-shadow:0 12px 40px rgba(0,0,0,.5)}
    #panel[hidden]{display:none}
    label{display:block;margin:0 0 10px}
    .row{display:flex;justify-content:space-between;color:#9a9aa2;margin-bottom:4px}
    .row b{font-weight:500;color:#e8e8ea}
    input,select{width:100%;background:#1c1c1f;border:1px solid #34343a;border-radius:5px;
      color:#e8e8ea;padding:4px}
    input[type=range]{padding:0}
    input[type=color]{height:28px;padding:2px}
    footer{display:flex;gap:6px;margin-top:4px}
    footer button{flex:1}
  </style>
  <div id="panel" hidden></div>
  <button id="toggle">Tweaks</button>`;

  const panel = sh.getElementById('panel');

  for (const s of specs) {
    const label = document.createElement('label');
    const cur = value(s);
    const row = document.createElement('div');
    row.className = 'row';
    row.innerHTML = `<span>${s.label}</span><b></b>`;
    const out = row.querySelector('b');

    let input;
    if (s.type === 'select') {
      input = document.createElement('select');
      for (const o of s.options || []) {
        const opt = document.createElement('option');
        opt.value = o;
        opt.textContent = o.split(',')[0].replace(/["']/g, '');
        input.append(opt);
      }
      input.value = cur;
      // The page's current value may not be one of the offered options; show it rather
      // than silently snapping the control to option[0] and lying about the page.
      if (input.value !== cur && cur) {
        input.insertAdjacentHTML('afterbegin',
          `<option value="${cur.replace(/"/g, '&quot;')}">${cur.split(',')[0].replace(/["']/g, '')}</option>`);
        input.value = cur;
      }
    } else if (s.type === 'color') {
      input = document.createElement('input');
      input.type = 'color';
      // <input type=color> only accepts #rrggbb; anything else (oklch, var(), a name) starts neutral.
      input.value = /^#[0-9a-f]{6}$/i.test(cur) ? cur : '#888888';
    } else {
      input = document.createElement('input');
      input.type = 'range';
      input.min = s.min ?? 0; input.max = s.max ?? 1; input.step = s.step ?? 0.01;
      const n = parseFloat(cur);
      input.value = Number.isFinite(n) ? n : (Number(input.min) + Number(input.max)) / 2;
    }

    const show = () => { out.textContent = s.type === 'select' ? '' : input.value; };
    show();

    input.addEventListener('input', () => {
      state[s.var] = s.type === 'range' ? input.value + (s.unit || '') : input.value;
      show();
      apply();
    });

    label.append(row, input);
    panel.append(label);
  }

  const footer = document.createElement('footer');
  const copy = document.createElement('button');
  copy.textContent = 'Copy CSS';
  copy.onclick = async () => {
    const merged = {};
    for (const s of specs) merged[s.var] = value(s);
    try { await navigator.clipboard.writeText(toCss(merged)); copy.textContent = 'Copied'; }
    catch { console.log(toCss(merged)); copy.textContent = 'In console'; }
    setTimeout(() => (copy.textContent = 'Copy CSS'), 1200);
  };
  const reset = document.createElement('button');
  reset.textContent = 'Reset';
  reset.onclick = () => {
    for (const k of Object.keys(state)) root.style.removeProperty(k);
    state = {};
    try { localStorage.removeItem(KEY); } catch {}
    location.reload();
  };
  footer.append(copy, reset);
  panel.append(footer);

  sh.getElementById('toggle').onclick = () => (panel.hidden = !panel.hidden);

  apply();
  document.body.append(host);
})();
