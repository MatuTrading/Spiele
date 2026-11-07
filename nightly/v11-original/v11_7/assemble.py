#!/usr/bin/env python3
"""Reproducible original-based V11.7 build. Every prior stable source stays immutable."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent.parent
chunks=sorted((root/'source').glob('part_*.txt'))
assert len(chunks)==23,'Original 23-piece source missing'
html=b''.join(c.read_bytes() for c in chunks[:-1])+(root/'v11_4'/'part_022.txt').read_bytes()
marker=b'\nrender();\n</script></body></html>'
assert html.count(marker)==1
for path in (root/'v11_5'/'upgrade.js',root/'v11_6'/'upgrade_v11_6.js',root/'v11_7'/'upgrade_v11_7.js'):
    addon=path.read_bytes()
    assert b'ODIN GAME STUDIO V11.7' in addon if 'v11_7' in str(path) else True
    html=html.replace(marker,b'\n'+addon+marker)
assert b'function odinV117Advance' in html and len(html)>9_000_000
out=root/'PrivateMarketsTycoon_V11_7_Nightly_Offline.html'
out.write_bytes(html)
print('Built',out,'bytes=',len(html),'sha256=',hashlib.sha256(html).hexdigest())