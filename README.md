# FreeCAD-Grundkurs – 33 Schritte mit echten Screenshots

**Live:** <https://danielgloeckler.github.io/freecad-anleitung/>

Sockel, Kopf und Vertiefung: erst ein **Sockel 50 × 40 × 10 mm**, dann ein
**Kopf 30 × 20 × 10 mm** als eigener Körper und zum Schluss eine
**Vertiefung 18 × 10 × 4 mm**. Jeder Schritt zeigt einen **echten Screenshot
aus FreeCAD 1.1** mit einer **Lupe** auf dem Element, das man anklicken soll.

## Benutzen

`index.html` im Browser öffnen.

- **Weiter / Zurück** rechts, die Schrittliste links oder `←` `→`
- **Orange Markierung + Lupe** = hier klicken
- **Bild anklicken** („Bild groß“) → Vollbild, mit `←` `→` durch die Schritte
- Fortschritt wird lokal gespeichert, „Neu starten“ setzt zurück
- Direktlink: `index.html?schritt=28` oder `index.html?schritt=fertig`

## Ablauf

**Sockel (1–17):** Neue Datei · Part Design · Neuer Körper · Neue Skizze
(Panel „Hilfswerkzeuge“) · XY-Ebene · OK · Rechteck-Werkzeug · Rechteck
50 × 40 · Bemaßung · 50 mm · vertikale Bemaßung · 40 mm · Skizze schließen ·
Aufpolsterung · Tiefe 10 mm · OK · Sockel fertig

**Kopf als neuer Körper (18–27):** Neuer Körper „Kopf“ · Neue Skizze ·
Deckfläche des Sockels · Referenz übernehmen („Erzeugen einer unabhängigen
Kopie“) · Rechteck 30 × 20 · bemaßen · Skizze schließen · Aufpolsterung
10 mm · OK · Kopf fertig

**Vertiefung (28–31):** Deckfläche des Kopfes · Rechteck 18 × 10 · bemaßen ·
Vertiefung 4 mm · fertig

**Abschluss (32–33):** Ansicht drehen · Speichern

## Screenshots

`assets/01_start.jpg` … `assets/23_speichern.jpg` – alle mit
**FreeCAD 1.1.4**, dunkles Theme, deutsche Oberfläche.

Neu erzeugen:

```
"D:\Programm\FreeCAD 1.1\bin\freecad.exe" tools\erzeuge_screenshots.py
```

Das Skript baut Sockel, Kopf und Vertiefung per Python-API, öffnet die echten
Dialoge (Befestigung, Referenzübernahme, Aufpolsterung, Vertiefung) und
fotografiert das komplette FreeCAD-Fenster. Das Fenster wird dafür auf
1500 × 844 gesetzt.

## Lupen anpassen

```js
focus:[0.48, 0.44, 0.23, 0.035],  // x, y, Breite, Höhe der Markierung
lens:[0.15, 0.72],                // Mittelpunkt der Lupe
zoom:1.8                          // Vergrößerung
```

Alle Werte sind Anteile der Bildfläche (0 … 1), bezogen auf 1500 × 844.

## Hosting

Rein statisch (HTML + JPG): GitHub Pages, Netlify, Schulserver, USB-Stick.
Für GitHub Pages genügt `index.html` im Branch `main`
(„Deploy from a branch → main / (root)“).
