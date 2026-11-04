# FreeCAD-Grundkurs – interaktive Anleitung

Eine einzelne HTML-Seite, die das FreeCAD-Fenster simuliert: Man klickt sich durch
13 Schritte – vom leeren Dokument bis zum fertigen Quader 50 × 40 × 10 mm.
Keine Installation, keine Internetverbindung, keine externen Dateien.

## Benutzen

`index.html` im Browser öffnen. Fertig.

- **Orange markierte Elemente** im simulierten FreeCAD-Fenster anklicken –
  oder den **Weiter**-Button rechts benutzen.
- Der Fortschritt wird lokal im Browser gespeichert (`localStorage`).
- **Icon-Legende** (oben rechts) erklärt alle Werkzeuge mit Tastenkürzel.
- Direktlink auf einen Schritt: `index.html?schritt=6`
- Direktlink auf die Abschlussseite: `index.html?schritt=fertig`
- `index.html#legende` öffnet die Icon-Legende.

## Inhalt

1. Neues Dokument
2. Arbeitsbereich Part Design
3. Neuer Körper
4. Neue Skizze
5. XY-Ebene wählen
6. Rechteck zentriert zeichnen
7. Bemaßung 50 mm
8. Bemaßung 40 mm
9. Skizze schließen
10. Aufpolstern
11. Höhe 10 mm + OK
12. Ansicht & Navigation
13. Speichern & Ausblick

## Anpassen

Alles steckt in `index.html`:

| Was | Wo |
|---|---|
| Texte der Schritte | `<script>` → `STEPS` (Titel, Lead, Bullets, Tipps, Statuszeile) |
| Icon-Liste der Legende | `<script>` → `ICONS` |
| Icons | `<svg><defs>` oben im Dokument (`#i-…`) |
| Farben / Layout | CSS-Variablen in `:root` |

Ein Schritt braucht mindestens `short`, `title`, `section`, `lead`, `bullets`,
`target` (CSS-Selektor des klickbaren Elements) und `status`.
`calloutOn` verschiebt die Sprechblase auf ein anderes Element, `tip` und `warn`
sind optionale Merkkästen.

## Hosting

Die Seite ist statisch und läuft überall: GitHub Pages, Netlify, Schulserver,
USB-Stick. Für GitHub Pages genügt es, `index.html` im Branch `main` zu haben
und Pages auf „Deploy from a branch → main / (root)“ zu stellen.

## Hinweis

Die FreeCAD-Oberfläche ist nachgebaut, keine echten Screenshots. Die Begriffe
entsprechen der deutschen FreeCAD-1.x-Oberfläche (Part Design, Aufpolstern,
Befestigung auswählen …). Maße und Reihenfolge folgen dem Grundkurs
„Quader erstellen“.
