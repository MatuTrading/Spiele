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
