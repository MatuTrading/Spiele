#!/usr/bin/env python3
"""Rebuild original-based V11.4 from V11.3's immutable first 22 parts and patched final part."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent.parent
parts=sorted((root/"source").glob("part_*.txt"))
assert len(parts)==23,"Missing V11.3 source parts"
target=root/"PrivateMarketsTycoon_V11_4_Nightly_Offline.html"
with target.open("wb") as out:
    for part in parts[:-1]: out.write(part.read_bytes())
    out.write((root/"v11_4"/"part_022.txt").read_bytes())
data=target.read_bytes()
assert len(data)>9_000_000 and data.startswith(b"<!DOCTYPE html>")
assert b"V11.4" in data and b"function odinPayouts()" in data
assert data.rstrip().endswith(b"</script></body></html>")
print(f"Built {target} bytes={len(data)} SHA256={hashlib.sha256(data).hexdigest()}")
