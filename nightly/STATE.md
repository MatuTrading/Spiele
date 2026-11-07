# STABILE BASIS: Private Markets Tycoon V11.4 – Original Premium, Stand 07.11.2026

**Aktuellste bestätigte Original-basierte Nightly-Version: V11.4.** GitHub Actions `ODIN V11.4 Nightly Original QA` Run **42342434798**, Commit `618d18dbb55a020bb33b760ea4babcf9844a60f9`, abgeschlossen mit PASS (Chromium vier Viewports, Spielstart, Mission, Navigation, Ausschüttungsbanner, Klick zum korrekten Fonds, keine JavaScript-Fehler, keine kaputten Bilder/Überläufe). Reproduzierbarer 9,4-MB-Offline-Build (23 Quellteile): `python nightly/v11-original/v11_4/assemble.py`. Das Artefakt der erfolgreichen CI-Läufe enthält vollständiges HTML + echte Screenshots; lokale HTML- und ZIP-Pakete wurden erzeugt.

**NÄCHSTER AUTOMATISCHER LAUF:** MUSS vom V11.4-Original-Stand unter `nightly/v11-original/v11_4` ausgehen, NICHT von alter Preview 0.1/0.2 oder V11.0. Original-V11.3 Source-Chunks unter `nightly/v11-original/source` sowie der V11.4-Tail unter `v11_4/part_022.txt` schützen. Verfolge neue Verbesserungen in neuen Versionen (V11.5 usw.) und verwende neueste grüne CI als Basis. Fortschritt im Nightly-Branch versionieren, nur getestete Änderungen freigeben. Niemals `main`, Releases oder GitHub Pages ohne ausdrückliche Freigabe verändern. Bei GitHub-Fehlern letzte grüne V11.4 zurückbehalten. Prüfe vorher Branch-HEAD / Überschneidungen.

**Qualität:** lokale Regression 34/34 PASS, V11.4 Auszahlungsnavigation separat interaktiv Chromium PASS, GitHub Actions 4/4 Viewports PASS. Vorgänger V11.3: 15/15 Direkt-Engine-Langzeitsimulationen über 1.787 Monate, 322 Investments, 776 Ausschüttungen PASS. LocalStorage-Reload über echtes URL-Navigieren wegen Browser-Sperre **NOT TESTED**; Export/Import **PASS**. Echte Android-Hardware **NOT TESTED**.

---

# WICHTIG: Aktuellste geprüfte ORIGINAL-V11-Version (November 2026)

Die hochgeladene Original-V11.0-Datei wurde im aktuellen Entwicklungsdurchlauf erfolgreich eingelesen. Die bisherige Aussage unten, sie sei nicht zugänglich, ist historisch und **nicht mehr aktuell**. **V11.3 Original-based** ist nach 34/34 lokalen Playwright-Prüfungen und dem erfolgreichen GitHub-Actions-Lauf 42341775901 sicher geprüft. Original-V11.3 liegt rekonstruktierbar unter `nightly/v11-original/source/` und `assemble.py`, 23 Teile, unverändert.

**V11.4 Candidate:** Separater, nicht-destruktiver Tail-Delta-Build unter `nightly/v11-original/v11_4/`, Funktion: sofort sichtbare LP-Ausschüttungs-Benachrichtigung mit Navigation zum betroffenen Fonds. Lokale Tests: 34/34 PASS + echter Chromium-Test Banner/Navigation, vier Viewports; GitHub-Actions-Prüfung steht bis zum grünen CI-Lauf aus. Nach grünem CI ist V11.4 die neue stabile Basis. Vermeide zurück zu Nightly Preview 0.2 oder V11.0 zu gehen.

**Fortsetzungsanweisung an Nacht-Automation:** GitHub-Branch `odin/private-markets-tycoon-nightly` verwenden, neueste grüne originale V11.x Version im Verzeichnis `nightly/v11-original/` prüfen, `assemble.py` (V11.3) bzw. `v11_4/assemble.py` (V11.4) ausführen. Danach auf der neuesten grünen Version weiterarbeiten. Niemals Main oder veröffentlichte Version ändern. Bei nichtgrüner V11.4 bleibt V11.3 stabiler Fallback. Prüfe jeden GitHub-Write mit aktuellem Head-SHA.

---

# ODIN Nightly – Projektstand (2026-11-07)

## Ausgangslage / Provenienz
- Vom Nutzer benannt: `PrivateMarketsTycoon_V11_0_Premium_Offline.html`, 9.409.220 Bytes im File-System der Chat-Plattform erkannt.
- KRITISCH: Die Nutzerdatei ließ sich in dieser Sitzung nicht in die lokal ausführbare Containerumgebung übernehmen. Daher wurde **keine Bearbeitung des originalen V11.0-Codes** behauptet.
- Autorisiert verfügbares Ersatzprojekt: `capital-empire/index.html` auf `main`; Quelle ist ein eigenständig spielbares Börsen- und Private-Markets-Spiel mit vier Assetklassen und zwölf Deals.
- Separate Arbeitskopie: `nightly/PrivateMarketsTycoon_NightlyPreview_0_1_Offline.html` im Branch `odin/private-markets-tycoon-nightly`.
- `main` und öffentliches Spiel wurden NICHT geändert. Nightly verwendet den separaten localStorage-Key `odin-pmt-nightly-v3`.

## Ausführung 1 – 2026-11-07 (partiell verifizierter Prototyp)
- Code-Verbesserungen: vollständige mobile 6-Seiten-Navigation + Einstellungen (zuvor nur 5 Tabs); Tastatur-/ARIA-Stati; Nav-Touchflächen mindestens 54 px hoch; bessere Safe-Area; Hinweis auf reduzierte Animationen; kontextabhängige nächste Mission im Dashboard; separate Save-Slots.
- PASS: Generierter 94-KB-HTML-Stand ist vollständig inline (keine externe Laufzeit-JS).
- PASS: JavaScript des Standalone-Bundles syntaktisch in V8 kompiliert.
- PASS: Pure Engine über 72 Monate, 4 Anlageklassen, 12 Deals, `validate()` ohne Fehler.
- PASS: Externer Live-Browser konnte den Nightly-Preview über htmlpreview.github.io rendern und zeigte den vorhandenen Startdialog (siehe Browserrun 43cbf86f-a448-4b9d-8eec-f95f08b3caab).
- NOT TESTED: Dialog-Submit, echte Kauftransaktionen, tatsächliche Navigation, Speichern/Laden über UI; der externe Browserlauf wurde durch Interaktions-/Budgetgrenze eingeschränkt.
- NOT TESTED: Screenshots und visueller Vergleich auf 360×800, 390×844, 768×1024, 1440×900, physisches Smartphone.
- **Status: PREVIEW / PARTIALLY TESTED – NICHT als vollständig geprüfter V11-Nachfolger freigegeben.**

## Prioritäten (nächster Lauf)
1. Originale V11.0-Datei technisch zugänglich machen und die Versionsbasis eindeutig vergleichen. Nichts stillschweigend umstellen.
2. Startdialog vollständig durchklicken und reale Browser-Smoke-Tests für 4 Viewports durchführen.
3. Navigation, Save/Load, Kauf, Deal-Management und Eventfortschritt prüfen; Screenshots visuell begutachten.
4. Mobile-UI-Überlauf / Schaltflächengrößen nach Screenshots korrigieren.
5. Danach mehr grafische Spielwelt-Elemente, Charakteranimationen und Langzeit-Balancing.

## Fortsetzungssicherheit
- Vor jedem Schreibzugriff aktuellen Branch-Head prüfen; bei unerwarteten Änderungen erneut laden.
- Einen erfolgreichen Testlauf dokumentieren, keine reine Analyse als Entwicklungszyklus zählen.
- Im Zweifel nur Nightly-Dateien ändern. Kein Merge, kein Main-Push, keine Seitenveröffentlichung ohne Freigabe.

## 2026-11-07 Browserabnahme Preview 0.1
- GitHub Actions run 42340781068, commit 94e010c5d7: PASS.
- 4 Bildschirmgrößen × 7 Szenariotests = 28/28 PASS, keine Console- oder Pageerrors.
- Startdialog, sechs Navigationsseiten, Aktienkauf, DD, Monatsvorschub, LocalStorage-Reload, Einstellungen und Export-UI verifiziert.
- Elf Chromium-Screenshots gesichert: https://github.com/MatuTrading/Spiele/actions/runs/42340781068/artifacts/13561915287
- Screenshots visuell ausgewertet: doppelte Tutorial-/Mission-Banner sowie ungenutzte Büro-Panel-Höhe auf Desktop.
- STATUS: Preview 0.1 funktional im Chromium-Smoke verifiziert; kein Hardwaretest; Original V11 weiterhin unabhängig.

## Version 0.2 – Quality-of-Life Korrektur (Tests nach Commit ausstehend)
- Erstelle einen eindeutigen einzelnen Missionshinweis statt Dopplung.
- Zeige Tutorial auf Unterseiten nur, wenn es zur aktuellen Zielseite gehört.
- Büro-Canvas wächst mit der Desktop-Kartenhöhe.
- Screenshots ohne kurzlebige Toast-Overlays; Test findet neueste Version automatisch.
- Bis zur grünen CI-Abnahme bleibt 0.1 der verifizierte Fallback.

## 2026-11-07 — Abschluss Entwicklungszyklus 2
- **Version 0.2 ist im Chromium erfolgreich abgenommen:** GitHub Actions Run 42341253507 (Commit e3a4cce113c5).
- **PASS 28/28:** 7 Real-Browserprüfungen auf 360×800, 390×844, 768×1024, 1440×900.
- Startdialog, 6 Navigationseinträge, Aktienkauf, Due Diligence, Monatsfortschritt, Autosave+Reload, Einstellungen+Exportoberfläche und Layout ohne Body-Horizontaloverflow bestanden.
- Browser hat keinerlei Pageerrors/Console-Errors gemeldet.
- Tatsächliche Screenshots im Artefakt https://github.com/MatuTrading/Spiele/actions/runs/42341253507/artifacts/13561059646.
- Screenshots nach dem Test visuell geöffnet (360 und 390 Smartphone, 1440 Desktop). Die zuvor beobachtete doppelte Tutorial-/Missionseinblendung ist behoben; Büro füllt Desktop-Panel besser. Auf kleinem Handy bleibt bewusst eine 7-Tabs-Navigation, aktuell nicht abgeschnitten.
- 72-Monats-Pure-Engine-Simulation des Release-Codes vor Commit ohne Exception; alle vier Assetklassen vorhanden.
- Rollback: eigenständig spielbare 0.1 Datei liegt unverändert weiter im Branch.
- Hardware-Tests, Langzeit-Gaming, vollständiger Investment-Cashflow-/Fonds-Flow weiterhin NOT TESTED.
- Nachprüfbare Artefakte und Spielstartlinks: siehe nightly/README.md.
- Branch-only GitHub CI läuft nach Änderung an Workflow neu und erstellt nun auch ein HTML-Downloadpaket, falls der Test grün ist.

## Offene nächste Prioritäten
1. Original V11.0 Datei zugänglich machen, Quellstand eindeutig abgleichen; bis dahin keine als V11 ausgegebenen Änderungen.
2. Längere simulierte Spielerstrategien, Cashflow-/Fondsauflage-/Investitions/Exittest ergänzen.
3. Die UI-Grafik konsequent in Richtung Mobile-Spiel weiterentwickeln; visuell auf vier Viewports prüfen.
4. Nach jedem Durchlauf Commit+CI+Screenshots+State; fehlerhafte Vorschau nicht als stabil deklarieren.

## 2026-11-07 — Releasepaket 0.2 (branch-only)
- Abschließender GitHub Actions Regressionslauf 42341413066 **PASS**. `nightly/tests/browser_smoke.py` hat explizit 0.2 als Prüfdatei gewählt; sieben Interaktionen auf vier Viewports erfolgreich.
- CI-Artefakt `odin-nightly-playable`: https://github.com/MatuTrading/Spiele/actions/runs/42341413066/artifacts/13561369400 (enthält offline-HTML und BUILD_INFO).
- Screenshot-Artefakt: https://github.com/MatuTrading/Spiele/actions/runs/42341413066/artifacts/13561084910.
- Gelieferte HTML-Datei SHA256: `04aca85a1660ef5bb883d0d85104288b33ad77287cfae32dc15a49520cb83b8f`, rund 95 KB, vollständig inline ohne externe Script-Abhängigkeiten.
- Standalone-Version für Nutzer auch direkt per `raw.githubusercontent.com` aus dem Branch ladbar. Veröffentlichtes GitHub Pages/main ausdrücklich nicht verändert.
- Zwei tatsächlich abgeschlossene Verbesserungs-/Testzyklen: 0.1 (Mobile-Navigation + Mission), 0.2 (grafisches Layout / Deduplizierung / QA).
- Morgenübergabe-Automation täglich um 07:00 Europe/Berlin zusätzlich angelegt.
