/* ODIN V11.6: action-first mobile layout, less distracting finance chrome. */
const odinV116Status = document.querySelector('.status-details');
const odinV116Macro = document.getElementById('macro');
if (odinV116Status && odinV116Macro) {
  odinV116Status.appendChild(odinV116Macro);
  const summary = odinV116Status.querySelector('summary');
  if (summary) summary.innerHTML = 'Markt & Fondskennzahlen <span>⌄</span>';
}
const odinV116Styles = document.createElement('style');
odinV116Styles.textContent = [
  '.status-details .macro{margin:12px 0 3px}',
  '@media(max-width:560px){',
  '  .feature-card{display:flex;flex-direction:column-reverse}',
  '  .feature-card .pad{padding:13px}',
  '  .feature-card .pad h2{font-size:20px;margin:5px 0 6px}',
  '  .feature-card .pad > p,.feature-card .feature-facts{display:none}',
  '  .feature-card .pad .actions{margin-top:7px}',
  '  .feature-card .pad .actions .btn{width:100%;min-height:48px}',
  '  .feature-card .feature-visual{max-height:150px;min-height:110px}',
  '  .feature-card .feature-visual img{max-height:150px}',
  '  .decision-head h1{font-size:22px}',
  '}',
  '@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}'
].join('\n');
document.head.appendChild(odinV116Styles);
document.title = 'Private Markets Tycoon V11.6 – Nightly Evolution';
const odinV116Brand = document.querySelector('.brand small');
if (odinV116Brand) odinV116Brand.textContent = 'V11.6 · NIGHTLY EVOLUTION';
