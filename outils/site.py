# -*- coding: utf-8 -*-
"""Fige le texte du livre dans un fichier JS, pour que la page s'ouvre aussi
bien depuis un fichier local que depuis un serveur (fetch() est interdit en file://)."""
import glob, hashlib, json, os

R = os.path.join(os.path.dirname(__file__), "..")
d = json.load(open(os.path.join(R, "texte", "pages.json"), encoding="utf-8"))
d["glossaire"] = json.load(open(os.path.join(R, "texte", "glossaire.json"), encoding="utf-8"))

# Empreinte des planches : elle sert de paramètre d'URL pour que le navigateur
# aille rechercher les images dès qu'une seule a changé. Sans elle, Chrome sert
# indéfiniment la version qu'il a en cache, puisque les noms ne bougent pas.
h = hashlib.md5()
for f in sorted(glob.glob(os.path.join(R, "illustrations", "*.svg"))):
    h.update(os.path.basename(f).encode())
    h.update(open(f, "rb").read())
d["version"] = h.hexdigest()[:10]
js = "// Fichier engendré par outils/site.py — ne pas modifier à la main.\n" \
     "// La source du texte est texte/pages.json.\nwindow.LIVRE = %s;\n" % json.dumps(d, ensure_ascii=False, indent=1)
open(os.path.join(R, "assets", "livre-data.js"), "w", encoding="utf-8").write(js)
print("assets/livre-data.js : %d pages, %d mots glosés, planches v%s"
      % (len(d["pages"]), len(d["glossaire"]), d["version"]))
