# FreeCAD-Grundkurs – 19 Schritte mit echten Screenshots

**Live:** <https://danielgloeckler.github.io/freecad-anleitung/>

Eine statische HTML-Seite, die Schritt für Schritt durch ein einfaches
Part-Design-Bauteil führt: vom leeren Dokument zum Quader **50 × 40 × 10 mm**.
Jeder Schritt zeigt einen **echten Screenshot aus FreeCAD 1.1** – und eine
**Lupe**, die genau auf den Knopf zeigt, den man anklicken soll.

## Benutzen

`index.html` im Browser öffnen – fertig.

- **Weiter / Zurück** rechts, die Schrittliste links oder die Pfeiltasten `←` `→`
- **Orange Markierung** = hier klicken; die Lupe zeigt die Stelle vergrößert
- **Bild anklicken** (oder „Bild groß“) → Vollbild, mit `←` `→` durch die Schritte
- Fortschritt wird lokal gespeichert (`localStorage`), „Neu starten“ setzt zurück
- Direktlink auf einen Schritt: `index.html?schritt=10`
- Direktlink auf das Ende: `index.html?schritt=fertig`

## Die 19 Schritte

| # | Schritt | Was markiert wird |
|---|---|---|
| 1 | Neue Datei | Kachel „Leere Datei“ |
| 2 | Part Design | Eintrag in der Arbeitsbereich-Liste |
| 3 | Neuer Körper | „Neuer Körper“ im Aufgaben-Panel |
| 4 | Neue Skizze | Skizzen-Symbol oben rechts |
| 5 | XY-Ebene | Zeile „XY-Ebene“ |
| 6 | OK | OK-Knopf |
| 7 | Rechteck-Werkzeug | Rechteck-Symbol |
| 8 | Rechteck zeichnen | Ursprung im Skizzenfeld |
| 9 | Bemaßung | Bemaßungs-Symbol |
| 10 | 50 mm | Maß „50 mm“ |
| 11 | Vertikale Bemaßung | vertikales Maß-Symbol |
| 12 | 40 mm | Maß „40 mm“ |
| 13 | Skizze schließen | „Schließen“ im Panel |
| 14 | Aufpolsterung | Aufpolsterung-Symbol |
| 15 | Tiefe 10 mm | Feld „Tiefe“ |
| 16 | OK | OK-Knopf |
| 17 | Fertig | Eintrag „Aufpolster“ im Modellbaum |
| 18 | Ansicht | NaviCube |
| 19 | Speichern | Menüeintrag „Speichern“ |

## Screenshots neu erzeugen

Die Bilder in `assets/` wurden mit **FreeCAD 1.1.4** und
`tools/erzeuge_screenshots.py` aufgenommen. Das Skript baut das Modell per
Python-API, öffnet die echten Dialoge und fotografiert das komplette
FreeCAD-Fenster (`QWidget.grab`, inkl. Menüs).

```
"D:\Programm\FreeCAD 1.1\bin\freecad.exe" tools\erzeuge_screenshots.py
```

- Das FreeCAD-Fenster wird dafür kurz auf 1500 × 900 gesetzt.
- Das Skript schließt das Dokument am Ende ohne Speichern.
- Ergebnisse: `assets/01_start.jpg` … `assets/13_speichern.jpg`
- Voraussetzung: FreeCAD 1.1 mit dunklem Theme und deutscher Oberfläche.

## Lupen anpassen

Jeder Schritt hat drei Werte, alle als Anteile der Bildfläche (0 … 1):

```js
focus:[0.44, 0.40, 0.18, 0.025],  // x, y, Breite, Höhe der Markierung
lens:[0.70, 0.28],                // Mittelpunkt der Lupe
zoom:1.9                          // Vergrößerung
```

`tools/` enthält zusätzlich nichts weiter – die Screenshots werden bei Bedarf
neu erzeugt; die Lupenwerte stehen direkt in `index.html` (`STEPS`).

## Anpassen

| Was | Wo |
|---|---|
| Texte der Schritte | `<script>` → `STEPS` (Titel, Lead, Liste, Tipp, Bildpfad) |
| Lupen-Position | `focus`, `lens`, `zoom` im jeweiligen Schritt |
| Farben / Layout | CSS-Variablen in `:root` |

## Hosting

Die Seite ist rein statisch (HTML + JPG) und läuft überall: GitHub Pages,
Netlify, Schulserver, USB-Stick. Für GitHub Pages genügt `index.html` im
Branch `main` mit „Deploy from a branch → main / (root)“.
