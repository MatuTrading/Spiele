#!/usr/bin/env python3
"""Build V11.6 from immutable V11.4 original, V11.5 guide and the V11.6 mobile change."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent.parent
parts=sorted((root/"source").glob("part_*.txt"))
assert len(parts)==23,"Missing original game chunks"
base=b"".join(p.read_bytes() for p in parts[:-1])+(root/"v11_4"/"part_022.txt").read_bytes()
marker=b"\nrender();\n</script></body></html>"
assert base.count(marker)==1
for version in ("v11_5","v11_6"):
    base=base.replace(marker,b"\n"+(root/version/("upgrade.js" if version=="v11_5" else "upgrade_v11_6.js")).read_bytes()+marker)
target=root/"PrivateMarketsTycoon_V11_6_Nightly_Offline.html"
assert len(base)>9_000_000 and b"odinV116Status" in base and b"odinV115NextStep" in base
target.write_bytes(base)
print(f"Built {target} bytes={len(base)} SHA256={hashlib.sha256(base).hexdigest()}")
