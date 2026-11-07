# STABILE ORIGINALBASIERTE BASIS: V11.6 (07.11.2026, 12:59 Europe/Berlin)

**Neueste erfolgreich getestete Original-Version: V11.6.** GitHub Actions Chromium Run [42370268266](https://github.com/MatuTrading/Spiele/actions/runs/42370268266) **PASS**, mit Download-Artefakt [PrivateMarketsTycoon-V11-6-Nightly-Offline](https://github.com/MatuTrading/Spiele/actions/runs/42370268266/artifacts/13573278348). Vier Viewports 360×800, 390×844, 768×1024, 1440×900 bestanden die automatisierten Tests: Fondsgründung, Navigation, Ausschüttungsbanner, korrekte Fondsnavigation, kontextabhängige Einstiegshilfe, eindeutige Anlegeraktionen, Tutorial-Ausblendung, mobile Erstbildschirm-Schaltfläche und reduzierte Statusanzeige. Keine JavaScript-Fehler, kaputten Bilder oder horizontalen Überläufe im Test. Manuelle visuelle Screenshotkontrolle für 360, 390 und 1440 sowie lokaler interaktiver Anlegerdialog-Test durchgeführt. Keine echte Android-Hardware getestet.

**WICHTIG für alle nächsten Automationen:** neue Basis ist `nightly/v11-original/v11_6/assemble.py`. Die V11.4 Originalteile bleiben unverändert; `v11_5/upgrade.js` und `v11_6/upgrade_v11_6.js` werden reproduzierbar angewendet. Nicht V11.4 oder Preview 0.2 als aktuelle Version ausgeben. Nutze V11.6 als grünen Fallback bis die nächste Version ebenfalls eine grüne CI besitzt. Ändere nur den Nightly-Branch, nicht main/Pages/Releases. Nächste Prioritäten: mobile Details bei längeren Partien, Echtgeld-freie Balance-Simulationen, UI für mehrere Fondsgenerationen und Speicherung auf gehosteter Origin testen.

---

# ODIN Nightly – Latest stable: V11.4 original-based (2026-11-07)

GitHub verified: Commit `618d18dbb55a020bb33b760ea4babcf9844a60f9`, GitHub Actions `https://github.com/MatuTrading/Spiele/actions/runs/42342434798` – PASS. Artifact `PrivateMarketsTycoon-V11-4-Nightly-Offline` (ID 13562541199): built playable HTML and Chromium screenshots.

**Build:** `python nightly/v11-original/v11_4/assemble.py`. Reuses the 22 preserved V11.3 parts, plus `v11_4/part_022.txt`. Playable single-file offline HTML output: `nightly/v11-original/PrivateMarketsTycoon_V11_4_Nightly_Offline.html`.

**Progress:** Original user-uploaded `PrivateMarketsTycoon_V11_0_Premium_Offline.html` (9,409,220 bytes), V11.1 original-world map + 4-stage tutorial + transaction rollback, V11.2 missing image fix, V11.3 22/35/50% ticket UI + minimum-ticket guard, V11.4 cross-fund LP payout notification + jump to relevant fund and marked payout. Local 34/34 Chromium tests PASS at 360x800,390x844,768x1024,1440x900. Browser screenshot visually reviewed. CI separate Chromium tests PASS on all four viewports, including payout scenario. Local V11.3 15 extended pure gameplay simulations across 1787 months, 322 investments, 776 payouts, all PASS.

**Next priorities:** start from this V11.4 source; protect existing immutable chunks and V11.3 fallback; longer interactive browser simulations with real URL reload on a hosted origin, payout stress tests, mobile touch accessibility/performance, polish cards and animated district. Save tests and screenshots in next release. Avoid claiming mobile physical device or localStorage origin reload tested. No changes to main, Pages, or releases. Follow branch-head optimistic concurrency to avoid overlapping commits.
