# ODIN Private Markets Tycoon — Nightly Preview

**Status:** eigenständiger, im Chromium getesteter Entwicklungsprototyp auf Basis des bereits vorhandenen `capital-empire/index.html`. **Kein Nachweis, dass dies die Bearbeitung der separat hochgeladenen V11.0 ist**; deren Quellcode war in dieser Entwicklungsumgebung nicht lesbar. Produktiven `main` unverändert lassen.

## Aktueller geprüfter Spielstand
- **Version:** Nightly Preview 0.2 (Datei `PrivateMarketsTycoon_NightlyPreview_0_2_Offline.html`)
- **Direkt im Browser öffnen:** https://htmlpreview.github.io/?https://github.com/MatuTrading/Spiele/blob/odin/private-markets-tycoon-nightly/nightly/PrivateMarketsTycoon_NightlyPreview_0_2_Offline.html
- **Standalone-HTML / speichern:** https://raw.githubusercontent.com/MatuTrading/Spiele/odin/private-markets-tycoon-nightly/nightly/PrivateMarketsTycoon_NightlyPreview_0_2_Offline.html
- **GitHub-Code:** https://github.com/MatuTrading/Spiele/blob/odin/private-markets-tycoon-nightly/nightly/PrivateMarketsTycoon_NightlyPreview_0_2_Offline.html

## Abnahme & Beweismittel
- GitHub Actions Chromium: https://github.com/MatuTrading/Spiele/actions/runs/42341253507
- **PASS:** 28/28 echte Spielaktions-Tests (7 Tests × 4 Viewports 360×800, 390×844, 768×1024, 1440×900).
- **PASS:** Spielstart, 6 Navigationsseiten, Aktienkauf, Due Diligence, Zeitfortschritt, Autosave + Reload, Einstellungs-/Exportdialog, keine horizontalen Überläufe; keine JavaScript-/Console-Errors.
- Die Screenshots wurden danach manuell visuell geprüft (0.2) und zeigen die behobene doppelte Missionsanzeige und verbesserte Desktop-Flächennutzung.
- **Offen:** V11.0-Provenienz, lange reale Spielsitzungen, physische Android-/iOS-Hardware, vollständiges Balancing und 100%-Regressionsabdeckung.
- Screenshots und JSON-Bericht: https://github.com/MatuTrading/Spiele/actions/runs/42341253507/artifacts/13561059646

## Nightly Fortsetzung
- `STATE.md` als Fortschrittsgedächtnis
- `tests/browser_smoke.py` als reale UI-/Chromium-Regression
- `.github/workflows/odin-nightly-qa.yml` auf dem Nightly-Branch
- Bei fehlerhaftem Nightly-Build: letzte grüne Version 0.1 erhalten.
