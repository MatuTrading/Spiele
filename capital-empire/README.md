# Capital Empire – Börsen- und Private-Markets-Tycoon

Ein deutschsprachiges, responsives Browser-Spiel ohne externe Laufzeitbibliotheken oder echte Finanzdaten.

## Spielen

- **Online:** [Capital Empire auf GitHub Pages](https://matutrading.github.io/Spiele/capital-empire/)
- **Offline:** `index.html` direkt im Browser öffnen oder `Capital_Empire_Offline.html` aus dem Releasepaket verwenden. Beide enthalten alle Spielkomponenten als eine einzige HTML-Datei.
- **Einstieg:** Firma benennen, erste Aktie kaufen, einen Deal analysieren und investieren, Team und Büro ausbauen, eigene Fonds auflegen.

## Entwicklungsstruktur

- `index.html`: Produktions- und Offline-Bundle, **eigenständig direkt startbar**.
- `dev.html`: Modulare Entwickler-Startseite, lokal über HTTP-Server starten (ES-Module aus `file://` können blockiert sein).
- `data.mjs`: fiktive Unternehmen und Private-Markets-Deals.
- `engine.mjs`: reproduzierbare Wirtschafts- und Buchhaltungslogik.
- `office.mjs`: animierter, isometrischer **2.5D**-Canvas-Raum.
- `app.mjs`: UI, Navigation, Interaktion, Spielstand.
- `styles.css`: responsive Oberfläche.
- `scripts/build_bundle.py`: Erstellt das Produktions-Bundle aus modularen Quelldateien mit `python scripts/build_bundle.py`.

## Funktionen

- 12 synthetische Aktienwerte aus 4 Branchen; Kauf/Verkauf mit Spread und Gebühren; Einstand, realisierte und unrealisierte Ergebnisse, Dividenden.
- 12 Deals aus 4 Private-Markets-Klassen; Due Diligence, Kapitalabrufe, Risiken, laufende Cashflows, Restrukturierung, operative Maßnahmen und Exits.
- Gemeinsames Modell für Konjunktur, Zinsen, Inflation, Branchen und Unternehmensentwicklung.
- Büroausbau, Personal, vier Fonds und getrenntes Anlegervermögen mit Commitment, Abrufen, NAV, Gebühren, Carry und Ausschüttungen.
- Automatisches Speichern via Local Storage, JSON-Export/-Import, Pause und Geschwindigkeiten 1×/3×/10×.
- Eigene Spielgrafik, keine Drittmodelle, externen Bilddateien, Bibliotheken oder Live-Finanzdaten.

## Tests

- `node --test tests/engine.test.mjs`: **11/11 Tests bestanden**; 100 Monate × 15 Seeds im Langzeitszenario.
- `python tests/browser_smoke.py`: Chromium/Desktop/Touch-Emulation, Screenshots, UI-Klickpfade, Export/Import; im Testsystem ca. 60 Headless-FPS.
- Einzelheiten: [`tests/RUN_TESTS.md`](tests/RUN_TESTS.md).

Die Browser-Testumgebung blockierte direktes HTTP und `file://` mit `ERR_BLOCKED_BY_ADMINISTRATOR`. Die Tests spielten daher dieselben Quellen als In-Memory-Bundle ab. Die GitHub-Pages-URL wurde öffentlich abgerufen, **ein interaktiver Live-End-to-End-Test auf dem gehosteten Server und ein Hardwaretest auf echten Smartphones sind nicht nachgewiesen**.

## Hinweis

Ausschließlich fiktive Unternehmen, fiktive Deals und simulierte Finanzdaten. Die Simulation vereinfacht reale wirtschaftliche Risiken und ist kein Anlageberater.