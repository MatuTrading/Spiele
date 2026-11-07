# ODIN Nightly – Latest stable: V11.4 original-based (2026-11-07)

GitHub verified: Commit `618d18dbb55a020bb33b760ea4babcf9844a60f9`, GitHub Actions `https://github.com/MatuTrading/Spiele/actions/runs/42342434798` – PASS. Artifact `PrivateMarketsTycoon-V11-4-Nightly-Offline` (ID 13562541199): built playable HTML and Chromium screenshots.

**Build:** `python nightly/v11-original/v11_4/assemble.py`. Reuses the 22 preserved V11.3 parts, plus `v11_4/part_022.txt`. Playable single-file offline HTML output: `nightly/v11-original/PrivateMarketsTycoon_V11_4_Nightly_Offline.html`.

**Progress:** Original user-uploaded `PrivateMarketsTycoon_V11_0_Premium_Offline.html` (9,409,220 bytes), V11.1 original-world map + 4-stage tutorial + transaction rollback, V11.2 missing image fix, V11.3 22/35/50% ticket UI + minimum-ticket guard, V11.4 cross-fund LP payout notification + jump to relevant fund and marked payout. Local 34/34 Chromium tests PASS at 360x800,390x844,768x1024,1440x900. Browser screenshot visually reviewed. CI separate Chromium tests PASS on all four viewports, including payout scenario. Local V11.3 15 extended pure gameplay simulations across 1787 months, 322 investments, 776 payouts, all PASS.

**Next priorities:** start from this V11.4 source; protect existing immutable chunks and V11.3 fallback; longer interactive browser simulations with real URL reload on a hosted origin, payout stress tests, mobile touch accessibility/performance, polish cards and animated district. Save tests and screenshots in next release. Avoid claiming mobile physical device or localStorage origin reload tested. No changes to main, Pages, or releases. Follow branch-head optimistic concurrency to avoid overlapping commits.
