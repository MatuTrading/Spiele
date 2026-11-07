# ODIN – V91 Animation QA (isolierter Entwicklungsbranch)
**Status: Diagnose / nicht als V91-Spiel freigegeben.**

Die verpflichtende V90-Quelldatei `Kampf_fuer_Odin_V90_Animation_Polish_Offline.html` ist nicht im aktuell verfügbaren Repo oder als zugänglicher Upload vorhanden. Ein altes, separat archiviertes "Kampf für Odin.html" diente ausschließlich als KayKit-Clip-Testfixture. **Diese alte Version ist nicht V90.**

## Nachgewiesene Ergebnisse
- Die KayKit-GLB-Clips `Running_A` (68 Tracks) und `Ranged_Bow_Idle` (69 Tracks) besitzen **68 identische animierte Node/Property-Paare**. Ein falscher Mixer-Layer kann so Hüften, Beine, Oberkörper und Hände gleichzeitig überschreiben.
- Lower-body/Upper-body-Separation ist mit `animation_layers.mjs` vorbereitet. Namen wie `upperleg.l` und `upperlegl` werden unterstützt.
- Lokale Node-Unit-Tests und Python-Syntaxprüfung bestanden.
- Chromium über `file://` und `http://127.0.0.1` durch Administrator blockiert; echter Gameplay-/WebGL-Test derzeit blockiert.
- Eine neue V91-HTML-Datei wurde **nicht** als abgeschlossen bezeichnet. V88, V89 und V90 werden nicht überschrieben.

## Nächster Schritt
Die echte Ausgangsdatei `Kampf_fuer_Odin_V90_Animation_Polish_Offline.html` im Chat bereitstellen. Dann die echte Lauf-/Bogen-Logik integrieren, 12 Frames pro Laufzyklus aus 7 Perspektiven rendern, echte Game-Regressionstests mit Chromium/WebGL und Kontaktbögen durchführen. Niemals ein altes Spiel als V91 ausgeben.

Dieses Modul ist ein getesteter technischer Baustein, **kein fertiger Animation-Fix und keine visuelle Qualitätsabnahme**.
