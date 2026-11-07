#!/usr/bin/env python3
"""Safely rebuild V11.5 from the verified immutable V11.4 source + small UI patch."""
from pathlib import Path
import hashlib
root = Path(__file__).resolve().parent.parent
parts = sorted((root / "source").glob("part_*.txt"))
assert len(parts) == 23, "Missing preserved original V11.3 chunks"
base = b"".join(x.read_bytes() for x in parts[:-1]) + (root / "v11_4" / "part_022.txt").read_bytes()
marker = b"\nrender();\n</script></body></html>"
assert base.count(marker) == 1, "Unexpected ending in V11.4"
addon = (root / "v11_5" / "upgrade.js").read_bytes()
target = root / "PrivateMarketsTycoon_V11_5_Nightly_Offline.html"
data = base.replace(marker, b"\n" + addon + marker)
assert len(data) > 9_000_000 and data.startswith(b"<!DOCTYPE html>")
assert b"odinV115NextStep" in data and b"V11.5" in data
target.write_bytes(data)
print(f"Built {target} bytes={len(data)} SHA256={hashlib.sha256(data).hexdigest()}")
