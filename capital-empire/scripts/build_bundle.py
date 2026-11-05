"""Generate the single-file GitHub Pages / offline release from modular sources.

Usage: python scripts/build_bundle.py
The resulting index.html works when opened directly from disk.
"""
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
html=(ROOT/'dev.html').read_text(encoding='utf-8')
css=(ROOT/'styles.css').read_text(encoding='utf-8')
js=[]
for filename in ('data.mjs','engine.mjs','office.mjs','app.mjs'):
    text=(ROOT/filename).read_text(encoding='utf-8')
    text=re.sub(r'^import .*?;\s*$', '',text,flags=re.MULTILINE)
    text=re.sub(r'^export ', '',text,flags=re.MULTILINE)
    js.append('// '+filename+'\n'+text)
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+css+'\n</style>')
html=html.replace('<script type="module" src="app.mjs"></script>','<script>\n'+'\n'.join(js)+'\n</script>')
assert '<script type="module"' not in html
assert 'function advanceMonth' in html and '</html>' in html
(ROOT/'index.html').write_text(html,encoding='utf-8')
print('Built production index.html',len(html),'characters')