# Private Markets Tycoon V11.6 – Mobile-first candidate

Source lineage: V11.4 original-based, plus the reversible V11.5 and V11.6 patches. All original chunks and verified prior releases remain unchanged.

**New:** market macro KPIs move to an expandable status area; the most important first action appears before the large illustration on small phones. The current action is visible without scrolling at 360×800 and 390×844.

Rebuild: `python nightly/v11-original/v11_6/assemble.py`.

Local Chromium: actual first-investor flow, modal interaction, JS error checks, overflow tests, and viewport screenshots at 360×800, 390×844, 768×1024 and 1440×900. Screenshot images at 360, 390 and 1440 were visually reviewed. CI runs the previous payout regression and the new mobile first-screen check; only label green after CI confirms it.
