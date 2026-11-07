# Private Markets Tycoon V11.3 – original-based Nightly
This version derives from the user's uploaded **V11.0 Premium Offline HTML**, not from the separately maintained 0.2 Preview.

## Build
Run `python3 nightly/v11-original/assemble.py` from the repository root.
The 23 ordered UTF-8 chunks reconstruct the complete self-contained standalone HTML file. No downloads or additional runtime assets are needed to play.
GitHub Actions `ODIN V11 original-based Nightly QA` generates a downloadable HTML artifact on every change.

## Verified locally in Chromium / Playwright
34 of 34 automated checks passed at 360x800, 390x844, 768x1024 and 1440x900.
Tests covered start, fund creation, investor interview, DD, successful investment and district progress, four simulated months, capital call, transaction rollback, game export/import, restart, invalid import rejection and navigation.
Browser console page errors: none; horizontal overflow: none on the four viewports.

## Changes from V11.0
- Animated investment-city map with dynamically growing districts and market-phase badge.
- Interactive four-step first-fund mission.
- Investment-share selector (22/35/50%) with actual ticket amounts and minimum-ticket guard.
- Missing V10 interview image replaced by an embedded V11 asset.
- Atomic rollback for failed economic transactions.

## Limits
Local filesystem URL navigation was blocked in the local Chromium environment; reload-persistence via localStorage was not verifiable there. JSON save export/import WAS tested.
No real mobile hardware or store release was tested. No changes were made to main, Pages or published releases.
