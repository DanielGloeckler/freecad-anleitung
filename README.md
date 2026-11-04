# FreeCAD-Grundkurs – 29 Schritte mit echten Screenshots

**Live:** <https://danielgloeckler.github.io/freecad-anleitung/>

Zwei Körper, ein Bauteil: erst ein **Sockel 50 × 40 × 10 mm**, dann ein
**Kopf 30 × 20 × 10 mm** obendrauf – als eigener Körper. Jeder Schritt zeigt
einen **echten Screenshot aus FreeCAD 1.1** mit einer **Lupe** auf dem
Element, das man anklicken soll.

## Benutzen

`index.html` im Browser öffnen.

- **Weiter / Zurück** rechts, die Schrittliste links oder `←` `→`
- **Orange Markierung + Lupe** = hier klicken
- **Bild anklicken** („Bild groß“) → Vollbild, mit `←` `→` durch die Schritte
- Fortschritt wird lokal gespeichert, „Neu starten“ setzt zurück
- Direktlink: `index.html?schritt=21` oder `index.html?schritt=fertig`

## Ablauf

**Sockel (Schritte 1–17)**

1. Neue Datei
2. Arbeitsbereich Part Design
3. Neuer Körper
4. Neue Skizze (Panel „Hilfswerkzeuge“)
5. XY-Ebene
6. OK
7. Rechteck-Werkzeug
8. Rechteck 50 × 40 zeichnen
9. Bemaßung
10. 50 mm
11. Vertikale Bemaßung (Dropdown)
12. 40 mm
13. Skizze schließen
14. Aufpolsterung
15. Tiefe 10 mm
16. OK
17. Sockel fertig

**Kopf als neuer Körper (Schritte 18–27)**

18. Neuer Körper „Kopf“
19. Neue Skizze (Panel „Hilfswerkzeuge“)
20. Deckfläche des Sockels anklicken
21. Referenz übernehmen („Erzeugen einer unabhängigen Kopie“)
22. Rechteck 30 × 20 zeichnen
23. 30 und 20 mm bemaßen
24. Skizze schließen
25. Aufpolsterung, Tiefe 10 mm
26. OK
27. Kopf fertig

**Abschluss (Schritte 28–29)**

28. Ansicht drehen (NaviCube)
29. Speichern

## Screenshots

`assets/01_start.jpg` … `assets/19_speichern.jpg` – alle mit
**FreeCAD 1.1.4**, dunkles Theme, deutsche Oberfläche.

Neu erzeugen:

```
"D:\Programm\FreeCAD 1.1\bin\freecad.exe" tools\erzeuge_screenshots.py
```

Das Skript baut Sockel und Kopf per Python-API, öffnet die echten Dialoge
(Befestigung, Referenzübernahme, Aufpolsterung) und fotografiert das
komplette FreeCAD-Fenster. Das Fenster wird dafür auf 1500 × 844 gesetzt.

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
