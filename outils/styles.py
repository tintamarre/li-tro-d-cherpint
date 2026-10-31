# -*- coding: utf-8 -*-
"""La direction graphique du livre.

Beaucoup de papier nu, de petites figures posées dans le vide, un trait fin et
clair, une palette de quelques tons sourds. Le silence autour du dessin fait la
moitié du travail.
"""

ROLES = ("ciel", "herbe", "herbe2", "terre", "pierre", "serpent", "serpent2",
         "soleil", "toit", "mur", "eau", "nuit", "accent", "chair", "fleur")

EPURE = dict(
    label="Épuré",
    encre="#8C7B66", encre_w=0.68, encre_op=0.9, tremble=1.0,
    couleur="lavis", lavis_op=0.78, lavis_f="wc2",
    densite=0.42, ciel_plein=False, contour_perso=True, joues=True,
    pal=dict(ciel="#DCE4E6", herbe="#D3DCC4", herbe2="#AEBD9C", terre="#E0D3BC",
             pierre="#CBC1AC", serpent="#8D9C70", serpent2="#6E7D58", soleil="#F0E0B4",
             toit="#C4836A", mur="#EFE7D6", eau="#B8C9D2", nuit="#464F60",
             accent="#B4634A", chair="#F3DCC4", fleur="#D9A2A2"))

STYLES = {"epure": EPURE}
ORDRE = ["epure"]
