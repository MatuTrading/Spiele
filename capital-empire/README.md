# Capital Empire – Börsen- und Private-Markets-Tycoon

Ein deutschsprachiges, responsives Browser-Spiel ohne externe Laufzeitbibliotheken oder echte Finanzdaten.

## Spielen

- **Online:** GitHub Pages unter dem Unterordner `capital-empire/`.
- **Offline:** `Capital_Empire_Offline.html` aus dem Releasepaket direkt im Browser öffnen. Die modularen Quelldateien (`index.html`, `.mjs`, `.css`) benötigen lokal einen kleinen HTTP-Server, da Webbrowser ES-Module aus `file://` aus Sicherheitsgründen oft blockieren.
- **Start:** Firma benennen, erste Aktie kaufen, einen Deal analysieren und investieren, Team und Büro ausbauen, eigene Fonds auflegen.

## Technik

- HTML5/CSS, Vanilla JavaScript als ES-Module, HTML5 Canvas (animierte isometrische **2.5D**-Büroszene). **Keine echte Three.js-/WebGL-3D-Welt.**
- 12 synthetische Aktienwerte aus 4 Branchen und 12 Dealtypen aus 4 Private-Markets-Klassen.
- Gemeinsame monatliche Wirtschafts-, Zins-, Inflations- und Branchenfaktoren.
- Aktienorders mit Spread, Gebühren, Einstandsbasis, realisierten/unrealisierten Ergebnissen und Dividenden.
- Private-Equity-, Private-Debt-, Infrastruktur- und Immobilien-Zahlungsströme sowie Risikoszenarien.
- Fonds mit getrenntem Anlegervermögen, Commitment, Abrufen, NAV, Management Fees, Carry und Ausschüttungen.
- Autosave mittels Local Storage; JSON-Export/Import; spielbare Geschwindigkeiten 0×/1×/3×/10×, Monatsvorschub.
- Sämtliche dargestellten Unternehmen und Deals sind fiktiv. Die Simulation ist kein Finanzratgeber.

## Qualitätssicherung

- `node --test tests/engine.test.mjs` – Wirtschafts-, Persistenz- und Langzeittests.
- `python tests/browser_smoke.py` – lokales UI-Smoketest-Skript für Chromium/Playwright. Weil lokale URL-Navigation der verwendeten Testumgebung administrativ blockiert war, werden die identischen Quelldateien für den Test zu einem **temporären In-Memory-Bundle** verbunden und per `page.set_content` in Chromium geladen. Es wurden **keine realen HTTP-Aufrufe** getestet; der Screenshot-Test erfasst die tatsächliche Browserdarstellung des eingebetteten Bundles. Screenshots liegen im externen Releasepaket unter `screenshots/`.
- Hardwaretest auf physischem Android-Gerät und Online-Test der GitHub-Pages-Adresse: gesondert durchführen, falls nicht ausdrücklich als bestanden vermerkt.

## Daten und Lizenz

Spielgrafik, UI und Simulationsdaten wurden für dieses Projekt erstellt. Keine externen Bilder, Modelle oder Audioassets; keine Drittbibliotheken im Laufzeitpfad.