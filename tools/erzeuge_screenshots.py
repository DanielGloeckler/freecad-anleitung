# -*- coding: utf-8 -*-
"""
Erzeugt die echten FreeCAD-1.1-Screenshots fuer die interaktive Anleitung.

Aufruf (Windows, GUI noetig):
    "D:\\Programm\\FreeCAD 1.1\\bin\\freecad.exe" tools\\erzeuge_screenshots.py

Das Skript baut in FreeCAD ein neues Dokument, zeichnet die Skizze
(50 x 40 mm), polstert sie auf und fotografiert nach jedem Schritt das
komplette FreeCAD-Fenster. Die Bilder landen in assets/*.jpg.

Hinweis: Das FreeCAD-Fenster wird dafuer kurz auf 1500x900 gesetzt.
Am Ende wird das Dokument ohne Speichern geschlossen.
"""

import os
import traceback

import FreeCAD as App
import Part
import Sketcher
import FreeCADGui as Gui
from PySide import QtCore, QtGui, QtWidgets

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "assets")
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, "screenshots.log")
TMP_DOC = os.path.join(OUT, "_quader.FCStd")
WIDTH = 1500

# alte Logdatei leeren
open(LOG, "w", encoding="utf-8").close()


def log(msg):
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(str(msg) + "\n")


def pump(ms=350):
    QtWidgets.QApplication.processEvents()
    QtCore.QThread.msleep(ms)
    QtWidgets.QApplication.processEvents()


def _save(pm, name):
    if pm.width() > WIDTH:
        pm = pm.scaledToWidth(WIDTH, QtCore.Qt.SmoothTransformation)
    path = os.path.join(OUT, name + ".jpg")
    ok = pm.save(path, "JPG", 88)
    log("shot %s ok=%s %sx%s" % (name, ok, pm.width(), pm.height()))
    return ok


def hide_report():
    for dock in Gui.getMainWindow().findChildren(QtWidgets.QDockWidget):
        title = dock.windowTitle()
        if any(word in title for word in ("Ausgabe", "Report", "Python", "Konsole")):
            if dock.isVisible():
                log("verstecke Dock: " + title)
                dock.hide()


def shot(name, overlay=None):
    """Screenshot des Hauptfensters, optional mit Popup/Dialog darueber."""
    hide_report()
    Gui.updateGui()
    pump(400)
    mw = Gui.getMainWindow()
    pm = mw.grab()

    if overlay is not None:
        try:
            om = overlay.grab()
            if overlay.isWindow():
                pos = mw.mapFromGlobal(overlay.geometry().topLeft())
            else:
                pos = mw.mapFromGlobal(overlay.mapToGlobal(QtCore.QPoint(0, 0)))
            log("  overlay %s pos=%s size=%sx%s" % (name, pos, om.width(), om.height()))
            painter = QtGui.QPainter(pm)
            painter.drawPixmap(pos, om)
            painter.end()
        except Exception as exc:
            log("  overlay %s: %r" % (name, exc))

    return _save(pm, name)


# ------------------------------------------------------------------ Helfer
def dismiss_modals():
    dlg = QtWidgets.QApplication.activeModalWidget()
    while dlg is not None and "DocumentRecovery" in dlg.objectName():
        log("schliesse Dialog: " + dlg.objectName())
        dlg.reject()
        pump(400)
        dlg = QtWidgets.QApplication.activeModalWidget()


def visible_button(text):
    for btn in Gui.getMainWindow().findChildren(QtWidgets.QPushButton):
        if btn.isVisible() and btn.text().replace("&", "").strip() == text:
            return btn
    return None


def click_cancel():
    btn = visible_button("Abbrechen")
    log("Abbrechen-Button: %r" % (btn,))
    if btn:
        btn.click()
        pump(800)
    try:
        Gui.Control.closeDialog()
    except Exception:
        pass
    pump(500)


def workbench_combo():
    for combo in Gui.getMainWindow().findChildren(QtWidgets.QComboBox):
        try:
            items = [combo.itemText(i) for i in range(combo.count())]
        except Exception:
            continue
        if "Part Design" in items and "Sketcher" in items:
            return combo
    return None


def menu_by_text(text):
    for action in Gui.getMainWindow().menuBar().actions():
        if action.text().replace("&", "").strip() == text:
            return action
    return None


def zoom_out(view, steps=1):
    """Etwas Rand ums Modell, ohne die Kamera zu verlieren."""
    for _ in range(steps):
        try:
            view.zoomOut()
            pump(200)
        except Exception as exc:
            log("zoomOut: %r" % (exc,))
            break



def handle_reference():
    """Referenzdialog beim Skizzieren auf einer fremden Flaeche."""
    dlg = QtWidgets.QApplication.activeModalWidget()
    log("Referenzdialog: %r" % (dlg,))
    if dlg is None:
        return
    radio = dlg.findChild(QtWidgets.QRadioButton, "radioIndependent")
    if radio is not None:
        radio.setChecked(True)
    pump(250)
    shot("14_kopf_referenz", dlg)
    for btn in dlg.findChildren(QtWidgets.QPushButton):
        if btn.text().replace("&", "").strip() == "OK":
            btn.click()
            return
    dlg.reject()

# ------------------------------------------------------------------ Ablauf
def run():
    try:
        mw = Gui.getMainWindow()
        mw.resize(1500, 844)
        mw.move(20, 20)
        mw.raise_()
        pump(900)
        dismiss_modals()
        log("Fenster: %sx%s" % (mw.width(), mw.height()))

        # --- 1: Startseite ----------------------------------------------
        shot("01_start")

        doc = App.newDocument("Quader")
        doc.Label = "Quader"
        Gui.activateWorkbench("PartDesignWorkbench")
        pump(900)

        # --- 3: leeres Dokument + Aufgaben-Panel ------------------------
        shot("03_neuer_koerper")

        # --- 2: Arbeitsbereich-Auswahl ----------------------------------
        combo = workbench_combo()
        log("Combo: %r" % (combo,))
        if combo:
            combo.showPopup()
            pump(500)
            popup = combo.view().window()
            try:
                pos = combo.mapToGlobal(QtCore.QPoint(0, combo.height()))
                popup.move(pos)
            except Exception as exc:
                log("popup move: %r" % (exc,))
            pump(300)
            shot("02_arbeitsbereich", popup)
            combo.hidePopup()
            pump(300)

        # --- 4: Koerper anlegen (echter FreeCAD-Befehl) -----------------
        Gui.runCommand("PartDesign_Body")
        pump(1400)
        body = [o for o in doc.Objects if o.TypeId == "PartDesign::Body"][-1]
        body.Label = "Körper"
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(body)
        pump(900)
        shot("04_neue_skizze")

        # --- 5: Befestigung auswaehlen (Task-Panel, kein Modal) ---------
        Gui.runCommand("PartDesign_NewSketch")
        pump(1600)
        shot("05_xy_ebene")
        click_cancel()

        # evtl. angelegte Skizze entfernen
        for obj in list(body.Group):
            if obj.TypeId == "Sketcher::SketchObject":
                log("entferne Temp-Skizze: " + obj.Name)
                body.removeObject(obj)
        doc.recompute()
        pump(400)
        log("aktiver Dialog nach Abbruch: %r" % (Gui.Control.activeDialog(),))

        # --- Skizze auf XY-Ebene anlegen --------------------------------
        sketch = body.newObject("Sketcher::SketchObject", "Sketch")
        sketch.Label = "Skizze"
        plane = [o for o in body.Origin.OriginFeatures if o.Name == "XY_Plane"][0]
        sketch.AttachmentSupport = [(plane, "")]
        sketch.MapMode = "FlatFace"
        doc.recompute()
        pump(500)

        Gui.activeDocument().setEdit(sketch.Name)
        pump(900)
        view = Gui.activeDocument().activeView()
        view.setCameraType("Orthographic")
        view.viewTop()
        pump(400)

        # Rechteck 50 x 40, zentriert um den Ursprung
        pts = [App.Vector(-25, -20, 0), App.Vector(25, -20, 0),
               App.Vector(25, 20, 0), App.Vector(-25, 20, 0)]
        for i in range(4):
            sketch.addGeometry(Part.LineSegment(pts[i], pts[(i + 1) % 4]), False)
        for i in range(4):
            sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 4, 1))
        sketch.addConstraint(Sketcher.Constraint("Horizontal", 0))
        sketch.addConstraint(Sketcher.Constraint("Horizontal", 2))
        sketch.addConstraint(Sketcher.Constraint("Vertical", 1))
        sketch.addConstraint(Sketcher.Constraint("Vertical", 3))
        sketch.addConstraint(Sketcher.Constraint("Symmetric", 0, 1, 2, 1, -1, 1))
        doc.recompute()
        pump(500)
        view.fitAll()
        pump(600)
        shot("06_rechteck")

        # --- 7: 50 mm ---------------------------------------------------
        c50 = sketch.addConstraint(Sketcher.Constraint("Distance", 2, 50.0))
        doc.recompute()
        pump(600)
        try:
            sketch.setDatum(c50, App.Units.Quantity("50.00 mm"))
        except Exception as exc:
            log("Datum50: %r" % (exc,))
        Gui.updateGui()
        pump(400)
        shot("07_bemassung_50")

        # --- 8: 40 mm ---------------------------------------------------
        c40 = sketch.addConstraint(Sketcher.Constraint("Distance", 1, 40.0))
        doc.recompute()
        pump(600)
        try:
            sketch.setDatum(c40, App.Units.Quantity("40.00 mm"))
        except Exception as exc:
            log("Datum40: %r" % (exc,))
        Gui.updateGui()
        pump(700)
        view.fitAll()
        pump(300)
        shot("08_bemassung_40")

        # --- 9: Skizze schliessen ---------------------------------------
        Gui.activeDocument().resetEdit()
        Gui.Selection.clearSelection()
        pump(900)
        view = Gui.activeDocument().activeView()
        view.setCameraType("Perspective")
        view.viewIsometric()
        view.fitAll()
        pump(700)
        shot("09_skizze_geschlossen")

        # --- 10: Aufpolstern (Parameter-Dialog) --------------------------
        hide_report()
        pad = body.newObject("PartDesign::Pad", "Pad")
        pad.Label = "Aufpolstern"
        try:
            pad.Profile = sketch
        except Exception as exc:
            log("Profile: %r" % (exc,))
        pad.Length = 10.0
        doc.recompute()
        pump(900)
        try:
            sketch.ViewObject.Visibility = False
        except Exception:
            pass

        view = Gui.activeDocument().activeView()
        view.setCameraType("Perspective")
        view.viewIsometric()
        view.fitAll()
        zoom_out(view, 1)

        try:
            Gui.activeDocument().setEdit(pad.Name)
            pump(1600)
        except Exception as exc:
            log("Pad-Edit: %r" % (exc,))
        shot("10_aufpolstern")
        try:
            Gui.activeDocument().resetEdit()
        except Exception:
            pass
        pump(800)

        view = Gui.activeDocument().activeView()
        view.setCameraType("Perspective")
        view.viewIsometric()
        view.fitAll()
        zoom_out(view, 1)
        pump(700)
        shot("11_quader")

        # ================= Kopf als neuer Koerper ======================
        # --- 12: neuer Koerper ------------------------------------------
        Gui.Selection.clearSelection()
        pump(500)
        Gui.runCommand("PartDesign_Body")
        pump(1500)
        head_body = [o for o in doc.Objects
                     if o.TypeId == "PartDesign::Body" and o is not body][-1]
        head_body.Label = "Kopf"
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(head_body)
        pump(900)
        shot("12_kopf_body")

        # --- 13: Deckflaeche auswaehlen ---------------------------------
        top = None
        for i, f in enumerate(body.Shape.Faces):
            n = f.normalAt(0, 0)
            c = f.CenterOfMass
            if abs(n.z - 1.0) < 0.01 and abs(c.z - 10.0) < 0.01:
                top = i + 1
                break
        log("Top-Face: %r" % top)
        Gui.Selection.clearSelection()
        Gui.Selection.addSelection(body, "Face%d" % top)
        pump(700)
        shot("13_kopf_flaeche")

        # --- 14: Referenzdialog + Skizze --------------------------------
        QtCore.QTimer.singleShot(1600, handle_reference)
        Gui.runCommand("PartDesign_NewSketch")
        pump(1600)
        head = [o for o in head_body.Group if o.TypeId == "Sketcher::SketchObject"][0]
        head.Label = "Kopfskizze"
        try:
            copy = doc.getObject("CopyBody")
            if copy is not None:
                copy.Label = "Bezugsfläche"
                copy.ViewObject.Visibility = False
        except Exception as exc:
            log("CopyBody: %r" % (exc,))
        if not Gui.activeDocument().getInEdit():
            Gui.activeDocument().setEdit(head.Name)
            pump(600)

        # --- 15: Kopf-Rechteck 30 x 20 ----------------------------------
        hp = [App.Vector(-15, -10, 0), App.Vector(15, -10, 0),
              App.Vector(15, 10, 0), App.Vector(-15, 10, 0)]
        for i in range(4):
            head.addGeometry(Part.LineSegment(hp[i], hp[(i + 1) % 4]), False)
        for i in range(4):
            head.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % 4, 1))
        head.addConstraint(Sketcher.Constraint("Horizontal", 0))
        head.addConstraint(Sketcher.Constraint("Horizontal", 2))
        head.addConstraint(Sketcher.Constraint("Vertical", 1))
        head.addConstraint(Sketcher.Constraint("Vertical", 3))
        head.addConstraint(Sketcher.Constraint("Symmetric", 0, 1, 2, 1, -1, 1))
        doc.recompute()
        pump(700)
        view = Gui.activeDocument().activeView()
        view.viewTop()
        view.fitAll()
        pump(700)
        shot("15_kopf_rechteck")

        head.addConstraint(Sketcher.Constraint("Distance", 2, 30.0))
        head.addConstraint(Sketcher.Constraint("Distance", 1, 20.0))
        doc.recompute()
        pump(700)
        view.viewTop()
        view.fitAll()
        pump(700)
        shot("15_kopf_skizze")

        # --- 16: Kopf aufpolstern ---------------------------------------
        Gui.activeDocument().resetEdit()
        pump(800)
        hpad = head_body.newObject("PartDesign::Pad", "Pad001")
        hpad.Label = "Aufpolsterung"
        hpad.Profile = head
        hpad.Length = 10.0
        doc.recompute()
        pump(800)
        try:
            head.ViewObject.Visibility = False
        except Exception:
            pass
        view = Gui.activeDocument().activeView()
        view.setCameraType("Perspective")
        view.viewIsometric()
        view.fitAll()
        zoom_out(view, 1)
        try:
            Gui.activeDocument().setEdit(hpad.Name)
            pump(1600)
        except Exception as exc:
            log("Kopf-Pad-Edit: %r" % (exc,))
        shot("16_kopf_pad")
        try:
            Gui.activeDocument().resetEdit()
        except Exception:
            pass
        pump(800)

        # --- 17: Ergebnis: Sockel + Kopf --------------------------------
        view = Gui.activeDocument().activeView()
        view.setCameraType("Perspective")
        view.viewIsometric()
        view.fitAll()
        zoom_out(view, 1)
        Gui.Selection.clearSelection()
        pump(800)
        shot("17_kopf_fertig")

        # --- 18: Ansicht drehen -----------------------------------------
        try:
            rotation = App.Rotation(App.Vector(0, 0, 1), 28)
            view.setCameraOrientation(rotation.multiply(view.getCameraOrientation()))
            view.fitAll()
            pump(600)
            zoom_out(view, 1)
            pump(400)
        except Exception as exc:
            log("Ansicht: %r" % (exc,))
        shot("18_kopf_ansicht")

        # --- 19: Speichern ----------------------------------------------
        doc.saveAs(TMP_DOC)
        pump(900)
        action = menu_by_text("Datei")
        log("Datei-Menue: %r" % (action,))
        if action:
            menu = action.menu()
            rect = mw.menuBar().actionGeometry(action)
            menu.popup(mw.menuBar().mapToGlobal(rect.bottomLeft()))
            QtWidgets.QApplication.processEvents()
            popup = QtWidgets.QApplication.activePopupWidget()
            log("Datei-Popup: %r" % (popup,))
            if popup is not None:
                shot("19_speichern", popup)
                popup.close()
            else:
                shot("19_speichern")
            pump(300)
        else:
            shot("19_speichern")

        log("FERTIG")
    except Exception:
        log("FEHLER\n" + traceback.format_exc())
    finally:
        try:
            if App.activeDocument() and App.activeDocument().FileName == TMP_DOC:
                App.closeDocument(App.activeDocument().Name)
        except Exception:
            pass
        pump(500)
        try:
            if os.path.exists(TMP_DOC):
                os.remove(TMP_DOC)
        except Exception:
            pass
        QtCore.QTimer.singleShot(1500, QtWidgets.QApplication.quit)


QtCore.QTimer.singleShot(2500, run)
