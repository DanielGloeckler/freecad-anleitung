# FreeCAD-Grundkurs – 13 Schritte mit echten Screenshots

**Live:** <https://danielgloeckler.github.io/freecad-anleitung/>

Eine statische HTML-Seite, die Schritt für Schritt durch ein einfaches
Part-Design-Bauteil führt: vom leeren Dokument zum Quader **50 × 40 × 10 mm**.
Jeder Schritt zeigt einen **echten Screenshot aus FreeCAD 1.1** (dunkles Theme) –
keine Nachbauten, keine Platzhalter, keine externen Bibliotheken.

## Benutzen

`index.html` im Browser öffnen – fertig.

- **Weiter / Zurück** rechts, die Schrittliste links oder die Pfeiltasten `←` `→`
- **Bild anklicken** (oder „Bild groß“) → Vollbild, mit `←` `→` durch die Schritte
- Fortschritt wird lokal gespeichert (`localStorage`), „Neu starten“ setzt zurück
- Direktlink auf einen Schritt: `index.html?schritt=6`
- Direktlink auf das Ende: `index.html?schritt=fertig`

## Die Schritte

| # | Schritt | Screenshot |
|---|---|---|
| 1 | Neues Dokument | Startseite / „Leere Datei“ |
| 2 | Arbeitsbereich Part Design | aufgeklappte Arbeitsbereich-Liste |
| 3 | Neuer Körper | leeres Dokument, Panel „Start Part“ |
| 4 | Neue Skizze | Körper + „Hilfswerkzeuge“ |
| 5 | XY-Ebene wählen | Dialog „Befestigung auswählen“ |
| 6 | Rechteck zentriert | Skizze mit Randbedingungen (2 Freiheitsgrade) |
| 7 | Bemaßung 50 mm | 1 Freiheitsgrad |
| 8 | Bemaßung 40 mm | grün, „Vollständig bestimmt“ |
| 9 | Skizze schließen | Drahtmodell in der Isometrie |
| 10 | Aufpolstern | Parameter + grüne Vorschau |
| 11 | Höhe 10 mm | fertiger Quader |
| 12 | Ansicht & Navigation | gedrehte Ansicht, NaviCube |
| 13 | Speichern | Datei-Menü mit „Speichern“ |

## Screenshots neu erzeugen

Die Bilder in `assets/` wurden mit **FreeCAD 1.1.4** und
`tools/erzeuge_screenshots.py` aufgenommen. Das Skript baut das Modell per
Python-API, öffnet die echten Dialoge und fotografiert das komplette
FreeCAD-Fenster (`QWidget.grab`, inkl. Popups/Menüs).

```
"D:\Programm\FreeCAD 1.1\bin\freecad.exe" tools\erzeuge_screenshots.py
```

- Das FreeCAD-Fenster wird dafür kurz auf 1500 × 900 gesetzt.
- Das Skript schließt das Dokument am Ende ohne Speichern.
- Ergebnisse: `assets/01_start.jpg` … `assets/13_speichern.jpg`
- Voraussetzung: FreeCAD 1.1 mit dunklem Theme und deutscher Oberfläche.

## Anpassen

Alles steckt in `index.html`:

| Was | Wo |
|---|---|
| Texte der Schritte | `<script>` → `STEPS` (Titel, Lead, Bullets, Tipps, Bildpfad, Bildunterschrift) |
| Startbild / Abschlussbild | `STEPS[…].img` bzw. `FINAL_IMG` |
| Farben / Layout | CSS-Variablen in `:root` |
| Fortschritts-Speicherung | Konstante `KEY` |

Ein Schritt braucht `short`, `title`, `section`, `img`, `alt`, `caption`,
`lead` und `bullets`; `tip`, `warn` und `keys` sind optional.

## Hosting

Die Seite ist rein statisch (HTML + JPG) und läuft überall: GitHub Pages,
Netlify, Schulserver, USB-Stick. Für GitHub Pages genügt `index.html` im
Branch `main` mit „Deploy from a branch → main / (root)“.
