# AKTUELL SPIELBARE ORIGINAL-VERSION: PRIVATE MARKETS TYCOON V11.7

**Stabil / GitHub Chromium PASS:** [Testlauf](https://github.com/MatuTrading/Spiele/actions/runs/42374811272) · [Download (vollständiges Offline-HTML + Screenshots)](https://github.com/MatuTrading/Spiele/actions/runs/42374811272/artifacts/13574933118).

V11.7 aktualisiert den Original-V11-Spielpfad mit originalem Matu-Trading-Logo, intuitiven 1/3/12-Monat-Sprüngen und radikal vereinfachtem Mobile-Dashboard. Mehrfach reale Chromium-Spieltests auf vier Bildschirmgrößen durchgeführt; Asset-Dekodierprüfung 223/223 PASS, Export/Import und tatsächlicher LocalStorage-Reload auf GitHub Actions PASS. Für einen erneuten Build: `python nightly/v11-original/v11_7/assemble.py`.

Die separate ältere Capital-Empire-Preview ist **nicht** die aktuelle Version. Kein Main-/Pages-Deployment. Neuester grüner Stand V11.7, älterer Fallback V11.6.

---

# NEUESTE SPIELBARE ORIGINAL-VERSION: PRIVATE MARKETS TYCOON V11.6

**Bestätigt am 07.11.2026 – GitHub Actions PASS:** [Chromium-/Gameplay-Tests](https://github.com/MatuTrading/Spiele/actions/runs/42370268266). [Offline-HTML mit Screenshots herunterladen](https://github.com/MatuTrading/Spiele/actions/runs/42370268266/artifacts/13573278348) (GitHub-Actions-ZIP, Login kann erforderlich sein).

V11.6 baut auf der echten Premium-V11.0-Linie auf und enthält die stabilen Verbesserungen bis V11.4 sowie zwei weitere UI/UX-Zyklen:
- V11.5: intuitive Erklärung der nächsten Aktion, einfachere Kapitalabruf-/Ausschüttungsbegriffe, nach Abschluss verschwindende Einstiegsmission.
- V11.6: Anlegergespräch auf dem ersten Smartphone-Bildschirm sichtbar, große Illustration nach der Aktion, Marktdaten in einklappbarer Statusansicht.
- Vier Chromium-Screenauflösungen automatisiert getestet, Screenshots der Änderungen tatsächlich betrachtet. Kein physischer Smartphone-Hardwaretest.

**Wiederaufbau:** `python nightly/v11-original/v11_6/assemble.py`. `main`, Releases und Pages sind nicht geändert worden.

---

# Aktuell: Original-basiertes Private Markets Tycoon V11.4 – im Chromium getestet

**Neueste Version (07.11.2026): V11.4 Nightly Evolution**, tatsächlich auf Basis des vom Nutzer hochgeladenen 9,4-MB-V11.0-Premium-Spiels weiterentwickelt. Bisherige 0.2 Preview siehe Archivhinweis weiter unten; **nicht mehr neueste getestete Version**.

- **GitHub-Abnahme V11.4:** https://github.com/MatuTrading/Spiele/actions/runs/42342434798 (PASS, Chromium, vier Viewports, Ausschüttungsbanner und Navigation)
- **HTML herunterladen:** Öffne den Actions-Lauf und lade das Artefakt `PrivateMarketsTycoon-V11-4-Nightly-Offline` herunter (enthält HTML und Screenshots; Artefakte sind zeitlich begrenzt).
- **Dauerhaft gespeicherte Quellen und Zusammenbau:** https://github.com/MatuTrading/Spiele/tree/odin/private-markets-tycoon-nightly/nightly/v11-original
- **Reproduzierbar erstellen:** `python nightly/v11-original/v11_4/assemble.py` (erzeugt spielbare, vollständig offline nutzbare HTML-Datei)
- **Progress/QA:** `nightly/STATE.md` und `nightly/v11-original/STATE.md`. Lokale QA 34/34 PASS; Langzeitsimulationen 15/15 PASS.

Der `main`-Branch und veröffentlichte GitHub-Pages-Versionen blieben unverändert.

---

## Älteres Archiv (Preview 0.2, separate Codebasis)

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
