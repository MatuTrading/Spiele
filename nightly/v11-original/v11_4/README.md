# ODIN Private Markets Tycoon V11.4 — Original-based

Die stabile V11.3 ist unter `../source/` und `../assemble.py` eingefroren. V11.4 nutzt ausschließlich diese ersten 22 unveränderten Stücke und das korrigierte Stück `part_022.txt` in diesem Verzeichnis.

Ausführen: `python nightly/v11-original/v11_4/assemble.py`. Ergebnis: eine einzige offline spielbare HTML-Datei `nightly/v11-original/PrivateMarketsTycoon_V11_4_Nightly_Offline.html`.

Verbesserung: Ausschüttbare Cashflows werden fondsübergreifend auf der Spieloberfläche angezeigt, und der Spieler kann direkt zum betroffenen Fonds springen. Der Fonds erhält eine ausschüttbare Markierung. Dies vereinfacht Langzeitpartien mit vielen Fondsgenerationen.

Lokale Tests: Node --check PASS; 34/34 Playwright Regression PASS; mobile Auszahlungsbenachrichtigung visuell geprüft, Klick führt zum korrekten Fonds; vier Viewports. CI-Testergebnis folgt aus `.github/workflows/odin-v11-4-qa.yml`. Keine Änderung an main, Pages oder Releases.
