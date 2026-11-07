#!/usr/bin/env python3
"""Rebuild the self-contained V11.3 game from GitHub-sized UTF-8 chunks."""
from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
pieces=sorted((root/"source").glob("part_*.txt"))
assert len(pieces)==23, f"Expected 23 chunks, got {len(pieces)}"
out=root/"PrivateMarketsTycoon_V11_3_Nightly_Offline.html"
with out.open("wb") as f:
    for piece in pieces:
        f.write(piece.read_bytes())
data=out.read_bytes()
assert len(data)>9_000_000
assert data.startswith(b"<!DOCTYPE html>")
assert b"function odinWorld" in data and data.rstrip().endswith(b"</script></body></html>")
print("Built",out,"bytes",len(data),"SHA256",hashlib.sha256(data).hexdigest())
