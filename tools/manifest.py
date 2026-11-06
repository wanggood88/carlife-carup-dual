#!/usr/bin/env python3
"""Build merged AndroidManifest.xml for the CarLife + CarUp unified app."""
import os, xml.etree.ElementTree as ET

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get("SRC_DIR") or os.path.join(ROOT, "work")
OUT_DIR = os.environ.get("MERGE_OUT") or os.path.join(ROOT, "build", "merged")

BASE = SRC
OUT = OUT_DIR
ANDROID = "http://schemas.android.com/apk/res/android"
ET.register_namespace("android", ANDROID)
A = "{%s}" % ANDROID


def attr(e, name):
    return e.get(A + name)


def sattr(e, name, value):
    e.set(A + name, value)


cl = ET.parse(os.path.join(BASE, "dec_carlife/AndroidManifest.xml")).getroot()
cu = ET.parse(os.path.join(BASE, "dec_carup/AndroidManifest.xml")).getroot()

# ---------- permissions ----------
def perm_key(e):
    return (attr(e, "name"), attr(e, "maxSdkVersion"), attr(e, "usesPermissionFlags"))

have = {perm_key(e) for e in cl if e.tag == "uses-permission"}
for e in cu:
    if e.tag == "uses-permission":
        k = perm_key(e)
        if k not in have:
            cl.append(e)
            have.add(k)

# ---------- features ----------
have_f = {attr(e, "name") for e in cl if e.tag == "uses-feature"}
for e in cu:
    if e.tag == "uses-feature" and attr(e, "name") not in have_f:
        cl.append(e)
        have_f.add(attr(e, "name"))

# ---------- queries / permission declarations ----------
cu_extra = []
for e in cu:
    if e.tag == "queries":
        cu_extra.append(e)
    if e.tag == "permission":
        sattr(e, "name", "com.baidu.carlifevehicle.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")
        cu_extra.append(e)
for e in list(cu_extra):
    cl.append(e)
# matching uses-permission for the androidx dynamic receiver permission
up = ET.SubElement(cl, "uses-permission")
sattr(up, "name", "com.baidu.carlifevehicle.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")

# ---------- application ----------
app = cl.find("application")
sattr(app, "name", "com.baidu.carlifevehicle.DualApplication")
sattr(app, "appComponentFactory", "androidx.core.app.CoreComponentFactory")
sattr(app, "allowBackup", "false")
sattr(app, "hardwareAccelerated", "true")
sattr(app, "largeHeap", "true")
sattr(app, "usesCleartextTraffic", "true")
sattr(app, "extractNativeLibs", "true")
sattr(app, "icon", "@drawable/ic_launcher")
sattr(app, "label", "@string/app_name")
sattr(app, "theme", "@style/AppTheme")

# CarLife main activity no longer the launcher entry
for act in app.findall("activity"):
    if attr(act, "name") == "com.baidu.carlifevehicle.CarlifeActivity":
        for f in act.findall("intent-filter"):
            if any(a.get(A + "name") == "android.intent.category.LAUNCHER" for a in f.findall("action") + f.findall("category")):
                act.remove(f)

cu_app = cu.find("application")
for child in list(cu_app):
    if child.tag in ("meta-data",):
        continue
    if child.tag in ("activity", "service", "receiver", "provider"):
        n = attr(child, "name")
        if n == "com.shilapi.xcertplay.DiPlayActivity":
            for f in child.findall("intent-filter"):
                cats = [c.get(A + "name") for c in f.findall("category")]
                acts = [a.get(A + "name") for a in f.findall("action")]
                if "android.intent.category.LAUNCHER" in cats or "android.intent.action.MAIN" in acts:
                    child.remove(f)
            sattr(child, "exported", "true")
        if child.tag == "provider":
            auth = attr(child, "authorities")
            if auth == "com.carup.car.updateprovider":
                sattr(child, "authorities", "com.baidu.carlifevehicle.updateprovider")
            if auth == "com.carup.car.androidx-startup":
                sattr(child, "authorities", "com.baidu.carlifevehicle.androidx-startup")
        app.append(child)

# ---------- unified entry activity ----------
entry = ET.Element("activity")
sattr(entry, "name", "com.baidu.carlifevehicle.ui.DualEntryActivity")
sattr(entry, "exported", "true")
sattr(entry, "launchMode", "singleTop")
sattr(entry, "screenOrientation", "landscape")
sattr(entry, "theme", "@android:style/Theme.Light.NoTitleBar.Fullscreen")
sattr(entry, "configChanges", "fontScale|keyboard|keyboardHidden|navigation|orientation|screenSize|smallestScreenSize|uiMode|density")
f = ET.SubElement(entry, "intent-filter")
a = ET.SubElement(f, "action"); sattr(a, "name", "android.intent.action.MAIN")
c = ET.SubElement(f, "category"); sattr(c, "name", "android.intent.category.LAUNCHER")
app.insert(0, entry)

# keep application meta-data from CarUp that are harmless (android support version etc.)
ET.indent(cl, space="    ")
xml = ET.tostring(cl, encoding="utf-8").decode()
xml = '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n' + xml
open(os.path.join(OUT, "AndroidManifest.xml"), "w", encoding="utf-8").write(xml)
print(xml[:1500])
