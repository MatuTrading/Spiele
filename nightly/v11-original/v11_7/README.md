# ODIN Private Markets Tycoon V11.7 – Matu Trading Premium Mobile

**Status:** STABLE · Original-based · GitHub Actions Chromium PASS on November 7, 2026

- [Grüner CI-Lauf: JS, Wirtschaftslogik, Browseraktionen und visuelle Screenshots](https://github.com/MatuTrading/Spiele/actions/runs/42374811272)
- [Download-Paket mit vollständiger Offline-HTML, Screenshots und JSON-Testberichten](https://github.com/MatuTrading/Spiele/actions/runs/42374811272/artifacts/13574933118)
- Direkter eigenständig generierbarer Build: `python nightly/v11-original/v11_7/assemble.py` (Ergebnis: `nightly/v11-original/PrivateMarketsTycoon_V11_7_Nightly_Offline.html`)
- Komplette Single-HTML-Version ist offline nutzbar; bislang veröffentlichtes GitHub Pages / main unverändert.

## Änderungen gegenüber V11.6

1. Echtes Original-Matu-Trading-Logo (aus zuvor bereitgestelltem Northstar-HTML) im Header, Startbildschirm, Einstellungen, Endbildschirm und als Favicon; Original-Markeninhalt nicht nachgezeichnet.
2. +1 / +3 / +12 Monate, auf dem Spielbildschirm mit großen Sticky-Touchflächen sichtbar. Jeder Monat läuft durch die echte `nextMonth`-Engine; keine multiplizierte Einmalrendite. Bei Ereignissen, Exits, Cashflow-Bereitschaft oder neuen Fondsgenerationen wird angehalten. Summarischer Zeitsprungbericht.
3. Haupt-HUD zeigt Vermögen und 2-Mio.-Ziel; weitere KPIs/News sind einklappbar. Tutorial auf ein kompaktes Ziel reduziert, Investmentwelt ist via Touch und Tastatur interaktiv.
4. Begriffe vereinfacht, Buttonflächen und aufklappbare Bereiche mindestens 48px hoch, konzentrierter Dark/Gold-Markenstil.
5. Grafiklayout und Bildpositionen visuell auf verschiedenen Viewports geprüft, alle 223 vollständig eingebetteten Story-Illustrationen technisch dekodiert; keine defekten Dateien.

## Tatsächlich durchgeführte QA

- GitHub Actions Run 42374811272: PASS, 360x800, 390x844, 768x1024 und 1440x900.
- Zeitsteuerung über reale Klickaktionen mit unabhängiger monatsweiser Vergleichssimulation geprüft. 1/3/12-Monatstasten und Unterbrechung durch wichtiges Ereignis PASS.
- Investorengespräch, Investmentwelt-Navigation, Spielstand-Export/-Import, **echter LocalStorage-Reload auf CI-Origin** PASS.
- 223/223 Story-Illustrationen laden und dekodieren; Pageerrors und externe Request-Failures 0.
- Screenshotbilder 360, 390 und 1440 wurden lokal visuell geöffnet. Die GitHub-Version 390 wurde ebenfalls geprüft.
- **NOT TESTED:** Physische Android-/iOS-Hardware; vollständige Langzeitanalyse aller Fondsgenerationen; visuelle Einzelbewertung jedes der 223 Motive. Technischer Dekodiertest ist nicht gleich umfassende visuelle Prüfung.

## Sicherheit

Das Original V11.4, die Rückfallversion V11.6, der Main-Branch sowie Pages/Releases wurden nicht überschrieben. Die nächste Nightly-Iteration muss von der letzten grün getesteten Version V11.7 ausgehen.
