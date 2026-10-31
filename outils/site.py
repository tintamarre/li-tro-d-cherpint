# -*- coding: utf-8 -*-
"""Fige le texte du livre dans un fichier JS, pour que la page s'ouvre aussi
bien depuis un fichier local que depuis un serveur (fetch() est interdit en file://)."""
import json, os

R = os.path.join(os.path.dirname(__file__), "..")
d = json.load(open(os.path.join(R, "texte", "pages.json"), encoding="utf-8"))
js = "// Fichier engendré par outils/site.py — ne pas modifier à la main.\n" \
     "// La source du texte est texte/pages.json.\nwindow.LIVRE = %s;\n" % json.dumps(d, ensure_ascii=False, indent=1)
open(os.path.join(R, "assets", "livre-data.js"), "w", encoding="utf-8").write(js)
print("assets/livre-data.js : %d pages" % len(d["pages"]))
