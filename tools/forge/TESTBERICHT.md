# Prüfbericht: Odin Character Forge V15

Stand: 27. Oktober 2026. Ergebnis: **39 Prüfungen bestanden**, keine unbehandelten JavaScript- oder Konsolenfehler.

Geprüfte Datei: `Odin_Character_Forge.html` (16,003,355 Bytes).

SHA-256: `e0e0b6ab435db31cb8e89efd14b51a7e17b264e17e43f0ce2e1bba77b6ef4ad6`

## Tatsächlich bedient und geprüft

- Alle acht Schnellvorlagen und zehn Originalfiguren über die sichtbare Oberfläche ausgewählt.
- Körperteile gewechselt, Modellregler per Tastatur bedient und deren Synchronisation geprüft.
- Bauteilfarbe und Farbstärke geändert; echte Texturfärbung in der 3D-Vorschau und nach GLB-Reimport betrachtet.
- Rückgängig/Wiederholen, Namensvorschau, automatische Sicherung und Wiederherstellung nach Neuladen geprüft.
- Bauplan gespeichert und erneut geladen: Körperfamilie, alle Teile, Farben, Name und Animation wiederhergestellt. Ungültiger Bauplan wird vor Änderungen abgelehnt.
- Animation gesucht, gestartet, tatsächlich pausiert und über die Zeitleiste positioniert. Bei allen 132 Clips deformierte Vertexpositionen in einer Stichprobenpose auf endliche Werte geprüft.
- Modell-GLB, GLB mit einer Animation und GLB mit allen 132 Animationen heruntergeladen und die tatsächlichen Dateien strukturell geprüft. Reimport einschließlich Skinning geprüft; eine heruntergeladene animierte GLB-Datei in einer getrennten 3D-Ansicht gerendert.
- Kamera per Maus gedreht und gezoomt; Vorder-/Rückansicht, automatische Drehung, PNG-Download und Qualitätswechsel bedient.
- Desktop und Tabletbreiten 721, 768, 1024, 1100 und 1440 Pixel geprüft. Bedienelemente bleiben neben der Vorschau.
- Touch-Navigation bei 360, 390 und 412 Pixeln im Hochformat sowie 740 Pixeln im Querformat geprüft. Kein horizontaler Überlauf. Vorschau bleibt beim Scrollen bis zu den unteren Bauteilen sichtbar.
- Einfinger-Drehen und Zweifinger-Pinch durch echte Browser-Touch-Ereignisse geprüft.
- Lokalen HTML-Dateistart bei ausgeschaltetem Browsernetzwerk geprüft.

## Tatsächlich grafisch betrachtet

Screenshots der Originalfiguren und Schnellvorlagen, mehrere Animationszeitpunkte, Nahansicht der Farbänderung, getrennte GLB-Reimportansicht, Desktop-/Tabletoberfläche sowie Handy-Hoch- und Querformat wurden angesehen. Die sichtbaren Schattenstreifen auf Gesicht und Haaren der V14 sind beseitigt. Bei den betrachteten Kombinationen waren keine abgelösten oder auseinanderfallenden Körperteile zu sehen.

Die eingebetteten Modell-/Animationsdaten sind gegenüber der gelieferten V14 bytegleich erhalten. Die JavaScript-Bibliotheken wurden für den GitHub-Upload mit esbuild 0.25.12 verkleinert; Lizenzkommentare bleiben erhalten. Auch diese kompakte Fassung hat den vollständigen Testlauf bestanden. Die zehn Quellfiguren besitzen dieselben 23 Knochenbezeichnungen; inverse Bindematrizen stimmen bis auf Rundungsabweichungen von höchstens 5,46 × 10⁻¹² überein.

## Grenzen

Chromium mit SwiftShader und simulierten Touch-Ereignissen; kein Test auf einem physischen Samsung Galaxy A16. Keine Garantie für Bildrate auf echter Handyhardware oder jede denkbare Kombination und jeden Animationsframe. Die Stichprobe aller 132 Clips ist eine technische Prüfung, keine vollständige künstlerische Abnahme aller Bewegungen. Waffen, neu modellierte Vampirteile, eine trainierte Text-zu-3D-KI und die Integration der Exporte ins Tower-Defense-Spiel sind nicht Bestandteil dieser Version.

Die Screenshots dienen als interne Prüfnachweise; der Runner erzeugt sie bei erneuter Ausführung. Die maschinenlesbaren Ergebnisse stehen in `test-results.json`.
