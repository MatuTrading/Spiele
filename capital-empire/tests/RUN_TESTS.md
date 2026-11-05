# Testmatrix – 05.11.2026

## Automatisierte Wirtschaftssimulation

`node --test tests/engine.test.mjs`

**Ergebnis:** 11 von 11 Tests bestanden.

- Aktien: 12 Titel/4 Branchen; Kauf, Verkauf, durchschnittlicher Einstand, Rundungsbasis, Spread, unzulässige Orders.
- Private Markets: 3 Dealtypen × 4 Anlageklassen; Due Diligence, Liquidität, Kapitalabrufe, Exits.
- Personal und Büro: Gehälter, verfügbare Plätze, Ausbau, unzureichende Liquidität.
- Fonds: getrenntes Anlegervermögen, Managementgebühren und Kapitalabrufe.
- Spielstand: JSON-Roundtrip, inkompatible und beschädigte Daten.
- 100 simulierte Monate × 15 Zufallsstarts mit zwölf parallelen Dealtypen, ohne negative Cash-Bestände oder NaN.

## Chromium-UI-Smoketest

`python tests/browser_smoke.py`

**Ergebnis:** Desktop und simulierte Smartphone-Ansichten erfolgreich bedient, keine JavaScript-Fehler gemeldet.

- Headless Chromium über Python Playwright; Desktop 1440×900.
- Smartphone-Emulation mit Touch: 320, 360, 390, 480 und 768 px Breite, kein horizontales Dokument-Overflow.
- Firmengründung, Aktienkauf und -verkauf, DD und Private-Debt-Investment, Personal einstellen, Büroausbau, Fondsanlage, Kapitalabruf.
- Export einer JSON-Datei, Zustand manuell verändern, JSON wieder importieren und Stand wiederherstellen.
- Speichern und Wiederherstellen in einem frisch initialisierten Browser-Dokument.
- Screenshot-Prüfung von Start, Büro, Börse, Private Markets, Unternehmen und Fonds.
- Der Headless-Renderer erreichte im Test ungefähr 60 Browser-Frames pro Sekunde. Das ist **kein physischer Smartphone-Performancewert**.

## Nachvollziehbare Testeinschränkungen

Der Chromium-Test-Browser blockierte HTTP- und `file://`-Navigation mit `ERR_BLOCKED_BY_ADMINISTRATOR`. Deshalb wurden die **identischen Quellen temporär inline in ein Browser-Dokument geladen** (In-Memory-Bundle) und interaktiv getestet. Somit wurde weder eine echte Netzwerk-Auslieferung noch der GitHub-Pages-Host end-to-end verifiziert.

Die isometrische Bürowelt verwendet HTML5 Canvas in 2.5D und keine frei drehbare WebGL-3D-Kamera. Kein Test auf physischer Android- oder iOS-Hardware. Ein separates Gerätetestprotokoll ist noch ausstehend.