# -*- coding: utf-8 -*-
"""Les quatorze planches de « Li tro d' cherpint », en bandeau 1280 x 540."""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from dessin import *
from styles import STYLES

LW, LH = 1280, 540
STYLE = STYLES["epure"]


def S(slug, titre, seed):
    return Scene(slug, titre, seed, LW, LH, STYLE)


# ---------------------------------------------------------------- fonds types
def ciel(s, soleil=(.145, .24), nuage=(.72, .17), lune=None):
    if soleil:
        cx, cy = LW * soleil[0], LH * soleil[1]
        s.cercle(cx, cy, 42, s.C("soleil"), None, op=.85)
        s.ink("M %.1f %.1f a 42 42 0 1 1 84 0 a 42 42 0 1 1 -84 0" % (cx - 42, cy), 1.2, None, op=.5)
    if nuage:
        s.wash(blob(LW * nuage[0], LH * nuage[1], LW * .19, LH * .085, 12, 13, .3), s.C("ciel"), .34, "wc2")
    if lune:
        cx, cy = lune
        s.cercle(cx, cy, 30, s.C("soleil"), None, op=.9)
        s.cercle(cx + 11, cy - 7, 26, PAPER, None, op=1.0)


def pre(s, hz, bandes=2, ligne=True):
    """Le plateau : une ligne d'horizon tracee, deux bandes de pre."""
    s.wash(smooth([(-40, hz + 26), (LW * .22, hz - 22), (LW * .48, hz + 12), (LW * .74, hz - 26),
                   (LW + 40, hz + 8), (LW + 40, LH + 40), (-40, LH + 40)], True), s.C("herbe"), .42, "wc2")
    if bandes > 1:
        s.wash(smooth([(-40, hz + 92), (LW * .32, hz + 56), (LW * .64, hz + 104), (LW + 40, hz + 62),
                       (LW + 40, LH + 40), (-40, LH + 40)], True), s.C("herbe2"), .3, "wc2")
    if ligne:
        s.ink(smooth(wave(-30, hz + 2, LW + 30, hz - 10, 5, 2.2, 26)), 1.5, None, op=.45)


def trou(s, cx, cy, rx, ry, pierres=True, herbe=True):
    """Le pus' : une bouche noire, cerclee de pierres et d'herbe."""
    s.aplat(blob(cx, cy, rx, ry, 32, 15, .09), s.C("nuit"), .93)
    s.ink(blob(cx, cy, rx, ry, 32, 15, .09), 2.4)
    if pierres:
        for i in range(s.n(11)):
            a = math.pi * (i / max(1, s.n(11) - 1))
            s.add('<path d="%s" fill="%s" opacity="0.68"/>'
                  % (blob(cx + math.cos(a) * rx * 1.13, cy + math.sin(a) * ry * 1.28,
                          rx * .12, ry * .22, 40 + i, 7, .3), s.C("pierre")))
    if herbe:
        for i in range(s.n(8)):
            a = math.pi * (i / max(1, s.n(8) - 1))
            s.touffe(cx + math.cos(a) * rx * 1.04, cy + math.sin(a) * ry * 1.26 + 4, .65, s.C("herbe2"))


def interieur(s, sol=430, mur_h=0):
    """Une salle : le sol, et un appareil de pierre leger au fond."""
    s.wash(blob(LW * .5, LH * .42, LW * .56, LH * .42, 71, 15, .14), s.C("terre"), .22, "wc2")
    s.mur(-40, -20, LW + 40, sol - 40, h=62, w=128, color=s.C("pierre"), op=.17)
    s.wash(smooth([(-40, sol), (LW * .3, sol - 10), (LW * .7, sol + 8), (LW + 40, sol - 6),
                   (LW + 40, LH + 40), (-40, LH + 40)], True), s.C("terre"), .34, "wc2")
    s.ink(smooth(wave(-30, sol, LW + 30, sol - 6, 4, 2, 24)), 1.5, None, op=.4)


def serpent_lointain(s, bx, by, l=70, sc=1.0, col=None):
    """Un petit serpent, pour les bulles de pensee et les plateaux de balance."""
    mini = wave(bx - l * .5, by + 4 * sc, bx + l * .5, by - 2 * sc, 9 * sc, 2.2, 14)
    s.aplat(ribbon(mini, [11 * sc - j * .5 * sc for j in range(len(mini))]), col or s.C("serpent"), .92)
    s.ink(smooth(mini), 1.3)
    s.dot(bx - l * .5, by + 2 * sc, 2.0 * sc, s.st["encre"])


def bulle(s, bx, by, rx, ry, vers, seed=130):
    """Une bulle de pensee, avec son chapelet de petits ronds."""
    s.add('<path d="%s" fill="%s" opacity="0.92"/>' % (blob(bx, by, rx, ry, seed, 15, .13), PAPER))
    s.ink(blob(bx, by, rx, ry, seed, 15, .13), 1.6, None, op=.8)
    vx, vy = vers
    for k, rr in enumerate((6.5, 4.4, 2.9)):
        t = (k + 1) / 4.0
        s.cercle(bx + (vx - bx) * t, by + (vy - by) * t, rr, PAPER, None, op=.92)
        s.ink("M %.1f %.1f a %.1f %.1f 0 1 1 %.1f 0 a %.1f %.1f 0 1 1 %.1f 0"
              % (bx + (vx - bx) * t - rr, by + (vy - by) * t, rr, rr, 2 * rr, rr, rr, -2 * rr), 1.3, None, op=.75)


# ------------------------------------------------------------------- planches
def p00_couverture():
    s = S("couv", "Le serpent dresse hors du chantoir, parmi les eclats de miroir", 7)
    ciel(s, soleil=(.11, .20), nuage=(.80, .16))
    pre(s, 352)
    trou(s, 640, 452, 178, 50)
    pts = [(352, 108), (470, 86), (582, 140), (628, 248), (586, 352), (636, 430)]
    s.serpent(pts, 54, 8, s.C("serpent"), s.C("serpent2"))
    for (x, y, r) in ((196, 128, 11), (892, 150, 12), (1066, 262, 9), (170, 318, 8),
                      (1004, 96, 10), (766, 70, 8), (1156, 170, 9)):
        s.eclat(x, y, r, s.rnd.uniform(0, 3))
        s.etoile(x, y, r * .55, "#FFFDF6", .85, anim="scintille")
    s.procession(930, 1210, 372, 5, (.36, .46))
    for x, y, sc in ((1010, 112, .9), (248, 212, .8)):
        s.oiseau(x, y, sc)
    s.semis(60, 560, 468, 520, 10, s.C("fleur"), s.C("herbe2"))
    return s


def p01_li_pus():
    s = S("p01", "Un champ pres du hameau de Xhignez, et le trou que l'on nomme « on pus' »", 11)
    ciel(s)
    pre(s, 318)
    for i, fx in enumerate((.79, .865, .935)):
        s.maison(LW * fx, 316 - (i % 2) * 7, .6, s.C("mur"), s.C("toit"))
    # la haie
    for i in range(s.n(16)):
        x = 60 + i * 46
        if x > 880:
            break
        s.ink("M %.1f 322 q 5 -16 2 -26" % x, 1.4, s.C("herbe2"), op=.6)
    # le ruisseau qui se perd dans le pus'
    ruis = wave(-30, 404, 318, 452, 15, 2.0, 28)
    s.add('<g%s>' % s.cls("onde"))
    s.wash(ribbon(ruis, [24 - i * .45 for i in range(len(ruis))]), s.C("eau"), .5)
    s.ink(smooth(ruis), 1.5, s.C("eau"), op=.7)
    s.add('</g>')
    trou(s, 430, 462, 112, 34)
    # un villageois qui montre le trou
    s.personnage(770, 486, 1.15, bras="avant", bouche="o")
    s.ink("M 806 452 Q 700 436 566 452", 1.6, None, op=.55, dash="7 7")
    for x, y, sc in ((980, 118, .95), (1046, 158, .8), (268, 150, .85)):
        s.oiseau(x, y, sc)
    s.semis(80, 1200, 480, 526, 16, s.C("fleur"), s.C("herbe2"))
    return s


def p02_li_cherpint():
    s = S("p02", "Sous le champ, le serpent enroule dans le chantoir", 13)
    # le pre, en mince bandeau tout en haut
    s.wash(smooth([(-40, 92), (LW * .3, 76), (LW * .62, 98), (LW + 40, 74),
                   (LW + 40, 168), (-40, 182)], True), s.C("herbe"), .4, "wc2")
    for i, fx in enumerate((.07, .14, .21)):
        s.maison(LW * fx, 92 - (i % 2) * 5, .44, s.C("mur"), s.C("toit"))
    for i in range(s.n(18)):
        x = 460 + i * 30
        if x > 1210:
            break
        s.ink("M %.1f 94 L %.1f 66" % (x, x + 3), 1.5, s.C("accent"), op=.75)
        s.dot(x + 3, 64, 2.4, s.C("accent"), .9)
    s.ink(smooth(wave(-30, 108, LW + 30, 92, 5, 2.2, 26)), 1.6, None, op=.5)
    # la caverne
    cave = blob(640, 352, 584, 186, 55, 19, .11)
    s.aplat(cave, s.C("nuit"), .5)
    s.aplat(blob(640, 356, 540, 162, 56, 17, .1), "#1E2230", .55)
    s.ink(cave, 2.4)
    # racines qui pendent de la voute
    for i in range(s.n(16)):
        x = 110 + i * 70
        if x > 1180:
            break
        h = s.rnd.uniform(16, 52)
        s.ink("M %.1f 186 Q %.1f %.1f %.1f %.1f" % (x, x + s.rnd.uniform(-9, 9), 186 + h * .6,
                                                    x + s.rnd.uniform(-13, 13), 186 + h), 1.4, s.C("terre"), op=.5)
    # le serpent love, en spirale aplatie
    pts = [(452, 268), (620, 238), (812, 272), (886, 346), (812, 424), (624, 452),
           (452, 424), (392, 348), (470, 306), (640, 300), (730, 346), (662, 392)]
    s.serpent(pts, 58, 9, s.C("serpent"), s.C("serpent2"))
    for i in range(s.n(14)):
        s.eclat(s.rnd.uniform(120, 1160), s.rnd.uniform(240, 480), s.rnd.uniform(2.4, 4.6),
                0, s.C("soleil"), .4, stroke=False, anim="scintille")
    for px, py in ((196, 448), (1096, 426), (330, 486), (980, 480)):
        s.add('<path d="%s" fill="%s" opacity="0.5"/>' % (blob(px, py, 30, 13, int(px), 9, .3), s.C("pierre")))
    return s


def p03_les_tchesseus():
    s = S("p03", "Les chasseurs descendent au gouffre avec leurs lanternes, et n'en reviennent pas", 17)
    ciel(s, soleil=None, nuage=(.3, .14))
    s.wash(blob(640, 120, 620, 120, 61, 13, .22), s.C("nuit"), .14, "wc2")
    pre(s, 296)
    s.wash(smooth([(-40, 330), (LW * .3, 372), (LW * .62, 428), (LW + 40, 470),
                   (LW + 40, LH + 40), (-40, LH + 40)], True), s.C("terre"), .24, "wc2")
    trou(s, 912, 452, 168, 48)
    # la file qui descend
    for i, (x, y, sc) in enumerate([(132, 352, .58), (248, 368, .63), (372, 390, .68),
                                    (500, 414, .74), (628, 438, .8), (748, 462, .86)]):
        s.personnage(x, y, sc, bras="bas", dos=True, bouche=None)
        s.ink("M %.1f %.1f L %.1f %.1f" % (x + 15 * sc, y - 34 * sc, x + 24 * sc, y - 82 * sc), 2.0 * sc, None)
        lx, ly = x - 20 * sc, y - 36 * sc
        s.ink("M %.1f %.1f L %.1f %.1f" % (x - 16 * sc, y - 36 * sc, lx, ly - 2), 1.6 * sc, None)
        s.cercle(lx, ly + 10 * sc, 7 * sc, s.C("soleil"), s.st["encre"], 1.5 * sc, .95)
        s.etoile(lx, ly + 10 * sc, 13 * sc, s.C("soleil"), .35, anim="lueur")
    # les lueurs qui s'eteignent dans le noir
    for t in (0, .26, .5, .7, .86):
        a = t * 5.0
        r = 128 * (1 - t) + 8
        x, y = 912 + math.cos(a) * r, 456 + math.sin(a) * r * .34 + t * 26
        s.etoile(x, y, 15 * (1 - t) + 3, s.C("soleil"), .4 * (1 - t) + .06, anim="lueur")
        s.dot(x, y, 2.8 * (1 - t) + .8, s.C("soleil"), .8 * (1 - t) + .1)
    # les lances abandonnees
    for x, y in ((1118, 398), (196, 470), (1042, 344)):
        s.ink("M %.1f %.1f L %.1f %.1f" % (x, y, x + 9, y - 62), 2.2, None, op=.65)
    for x, y, sc in ((252, 110, 1.1), (330, 82, .9), (1062, 128, 1.0), (1140, 168, .85)):
        s.oiseau(x, y, sc, s.st["encre"], .8)
    return s


def p04_deus_condanes():
    s = S("p04", "Les deux condamnes dans leur cachot, la veille du supplice", 19)
    interieur(s, 404)
    # la lucarne et la lune
    s.aplat(blob(1004, 176, 86, 92, 80, 13, .07), s.C("nuit"), .9)
    s.ink(blob(1004, 176, 86, 92, 80, 13, .07), 3.0)
    ciel(s, soleil=None, nuage=None, lune=(982, 150))
    for x, y, r in ((1046, 128, 5.5), (1056, 206, 4.5), (952, 216, 4)):
        s.etoile(x, y, r, s.C("soleil"), .9, anim="scintille")
    for bx in (974, 1004, 1034):
        s.ink("M %.1f 92 L %.1f 262" % (bx, bx), 5.0, None, op=.9)
    s.ink("M 926 176 L 1082 176", 4.2, None, op=.85)
    # le rayon de lune sur la paille
    s.wash(smooth([(946, 252), (1062, 252), (1180, 500), (836, 500)], True), s.C("soleil"), .3, "wc2")
    s.wash_blob(640, 492, 560, 46, s.C("terre"), .38, f="wc2")
    for i in range(s.n(40)):
        x, y = s.rnd.uniform(60, 1220), s.rnd.uniform(462, 516)
        s.ink("M %.1f %.1f l %.1f %.1f" % (x, y, s.rnd.uniform(-16, 16), s.rnd.uniform(-5, 5)), 1.1, s.C("terre"), op=.6)
    # les deux
    s.personnage(368, 480, 1.9, bouche="droite", bras="croises")
    s.personnage(548, 486, 1.85, s.C("accent"), bouche="droite", bras="bas")
    # la chaine
    s.ink("M 300 452 Q 220 468 150 456", 2.4, None, op=.75)
    for i in range(6):
        s.cercle(286 - i * 26, 456 + math.sin(i) * 5, 6.5, "none", s.st["encre"], 2.0)
    # la souris
    s.personnage(1130, 510, .3, s.C("pierre"), cheveux=s.C("pierre"))
    s.ink("M 1142 500 Q 1166 494 1180 506", 1.4, None, op=.7)
    return s


def p05_pindards_fotches():
    s = S("p05", "Les fourches patibulaires, et les manants qui ne pensent qu'au serpent", 23)
    ciel(s, soleil=(.90, .17), nuage=(.42, .13))
    s.wash(smooth([(-40, 300), (LW * .16, 244), (LW * .34, 292), (LW + 40, 318),
                   (LW + 40, LH + 40), (-40, LH + 40)], True), s.C("terre"), .26, "wc2")
    pre(s, 352)
    # le gibet a plusieurs potences
    base = 300
    for px in (168, 286, 404):
        s.ink("M %.1f %.1f L %.1f 108" % (px, base, px), 6.0, None)
    s.ink("M 160 112 L 412 108", 7.0, None)
    s.ink("M 168 116 L 286 142 M 404 114 L 286 142", 2.0, None, op=.55)
    for hx in (226, 346):
        s.ink("M %.1f 112 L %.1f 166" % (hx, hx), 2.4, None)
        s.add('<ellipse cx="%.1f" cy="176" rx="12" ry="15" fill="none" stroke="%s" stroke-width="2.4"/>' % (hx, s.st["encre"]))
    for x, y, sc in ((146, 84, 1.0), (436, 74, .85), (240, 54, .7)):
        s.oiseau(x, y, sc, s.st["encre"], .9)
    s.add('<path d="M 392 98 q 10 -8 20 0 q 8 10 -4 16 q -14 4 -16 -8 Z" fill="%s" opacity="0.9"/>' % s.st["encre"])
    s.ink("M 412 104 l 13 4", 1.8, None)
    # les manants, et le serpent qui leur trotte en tete
    gens = [(606, 468, 1.0), (714, 482, 1.1), (826, 470, 1.02), (936, 486, 1.12), (1046, 472, 1.04)]
    for x, y, sc in gens:
        s.personnage(x, y, sc, bouche="droite")
    for i, (x, y, sc) in enumerate(gens):
        if i % 2:
            continue
        bx, by = x + 10, y - 62 * sc - 72
        bulle(s, bx, by, 60, 38, (x + 4, y - 60 * sc), 130 + i)
        serpent_lointain(s, bx, by, 62, .9)
    return s


def p06_l_ideye():
    s = S("p06", "Les juges autour de la table, et l'idee qui vient a l'un d'eux", 29)
    interieur(s, 392)
    s.wash_blob(640, 316, 300, 180, s.C("soleil"), .32, f="wc2")
    # les juges, debout derriere la table
    for x, sc in ((206, 1.55), (396, 1.46), (884, 1.46), (1050, 1.55), (700, 1.34)):
        s.personnage(x, 452, sc, chapeau="juge", bouche="droite", bras="croises")
    # la table, posee par-dessus : elle cache les jambes
    s.aplat("M 96 442 Q 640 424 1184 442 L 1184 540 L 96 540 Z", s.C("terre"), .92)
    s.ink("M 96 442 Q 640 424 1184 442", 2.4)
    s.ink("M 96 470 Q 640 452 1184 470", 1.6, None, op=.45)
    # la chandelle et les roles
    s.chandelle(640, 440, 70, 21, 46)
    for rx in (400, 880):
        s.add('<path d="%s" fill="%s" opacity="0.95"/>' % (blob(rx, 462, 52, 13, 120 + rx, 11, .18), PAPER))
        s.ink(blob(rx, 462, 52, 13, 120 + rx, 11, .18), 1.4, None, op=.8)
        for k in range(2):
            s.ink("M %.1f %.1f l 60 0" % (rx - 30, 458 + k * 6), .9, None, op=.45)
    # la bulle : un serpent et un eclat de miroir
    bx, by = 1090, 150
    bulle(s, bx, by, 100, 58, (1010, 300), 150)
    serpent_lointain(s, bx - 20, by + 12, 84, 1.0)
    for k, (ex, ey) in enumerate(((bx + 44, by - 22), (bx + 20, by - 36), (bx + 60, by - 2))):
        s.eclat(ex, ey, 11 - k * 2, k)
        s.etoile(ex, ey, 5 - k, "#FFFDF6", .9, anim="scintille")
    return s


def p07_l_offe():
    s = S("p07", "Le magistrat offre la vie sauve aux prisonniers a travers les barreaux", 31)
    interieur(s, 430)
    s.wash(blob(300, 260, 340, 290, 141, 15, .16), s.C("soleil"), .32, "wc2")
    s.wash(blob(1000, 280, 340, 300, 142, 15, .16), s.C("nuit"), .2, "wc2")
    # la grille, du sol au plafond
    for bx in range(598, 879, 70):
        s.ink("M %.1f 14 L %.1f 520" % (bx, bx), 7.0, None, op=.95)
    for by in (132, 414):
        s.ink("M 566 %.1f L 910 %.1f" % (by, by), 5.4, None, op=.9)
    # la hart, qui descend et s'enroule
    corde = wave(392, 14, 392, 214, 16, 2.2, 20)
    s.ink(smooth(corde), 3.2, s.C("terre"), op=.95)
    s.add('<ellipse cx="392" cy="248" rx="25" ry="31" fill="none" stroke="%s" stroke-width="3.2"/>' % s.C("terre"))
    # le magistrat, qui parle au travers
    s.personnage(486, 486, 2.0, s.C("accent"), chapeau="juge", bras="avant", bouche="o")
    s.add('<path d="%s" fill="%s" opacity="0.95"/>' % (blob(392, 400, 48, 28, 150, 11, .16), PAPER))
    s.ink(blob(392, 400, 48, 28, 150, 11, .16), 1.5, None, op=.85)
    # les prisonniers, derriere la grille
    s.personnage(968, 492, 1.78, bouche="droite", bras="bas")
    s.personnage(1106, 498, 1.66, s.C("herbe2"), bouche="droite", bras="croises")
    for k, rr in enumerate((7, 4.6)):
        s.cregle = None
        s.cercle(1040 + k * 18, 508 + k * 7, rr, "none", s.st["encre"], 2.0)
    for x, y, r in ((170, 122, 9), (300, 86, 7), (120, 250, 6)):
        s.etoile(x, y, r, s.C("soleil"), .55, anim="scintille")
    return s


def p08_li_drossart():
    s = S("p08", "Le magistrat pese la corde d'un cote, le serpent de l'autre", 37)
    s.wash(blob(640, 230, 600, 230, 161, 15, .16), s.C("terre"), .16, "wc2")
    pre(s, 404, bandes=1)
    # le visage, moitie clair moitie ombre
    s.aplat(blob(286, 196, 112, 126, 163, 15, .08), s.C("chair"), .97)
    s.wash(blob(352, 196, 56, 126, 164, 13, .12), s.C("nuit"), .2, "wc2")
    s.ink(blob(286, 196, 112, 126, 163, 15, .08), 2.4)
    s.add('<path d="M 182 136 q 104 -80 208 0 q -10 20 -208 0 Z" fill="%s" opacity="0.92"/>' % s.st["encre"])
    s.ink("M 182 136 q 104 -80 208 0", 1.8)
    for ex in (250, 330):
        s.cercle(ex, 188, 10.5, PAPER, s.st["encre"], 2.0)
        s.dot(ex + 1, 190, 5.0, s.st["encre"])
        s.ink("M %.1f 170 q 11 -8 22 0" % (ex - 11), 1.8)
    s.ink("M 258 250 q 28 13 56 -2", 2.2, None, op=.9)
    # la balance
    s.ink("M 820 196 L 820 266", 3.6, None)
    s.ink("M 620 282 L 1020 268", 4.0, None)
    s.dot(820, 272, 9, s.st["encre"])
    for px, py in ((624, 284), (1016, 270)):
        for k in (-1, 1):
            s.ink("M %.1f %.1f L %.1f %.1f" % (px, py, px + k * 54, py + 98), 1.7, None, op=.85)
        s.ink("M %.1f %.1f q 54 36 108 0" % (px - 54, py + 98), 2.8, None)
        s.add('<path d="M %.1f %.1f q 54 36 108 0 Z" fill="%s" opacity="0.45"/>' % (px - 54, py + 98, s.C("pierre")))
    # plateau gauche : la corde — plateau droit : le serpent
    for k in range(4):
        s.add('<ellipse cx="624" cy="%.1f" rx="%.1f" ry="8" fill="none" stroke="%s" stroke-width="3.0"/>'
              % (366 - k * 13, 36 - k * 4, s.C("terre")))
    s.ink("M 624 320 q 22 -26 7 -50", 2.8, s.C("terre"))
    serpent_lointain(s, 1016, 350, 86, 1.0)
    s.semis(60, 1220, 460, 520, 12, s.C("fleur"), s.C("herbe2"))
    return s


def p09_l_armure():
    s = S("p09", "La nuit passee a tailler les miroirs et a coudre l'armure", 41)
    interieur(s, 420)
    s.wash(blob(640, 250, 560, 240, 171, 15, .16), s.C("nuit"), .22, "wc2")
    s.wash_blob(640, 280, 300, 220, s.C("soleil"), .32, f="wc2")
    # la chandelle
    s.chandelle(1079, 386, 56, 18, 44)
    # le mannequin, et l'armure en cours
    s.ink("M 640 468 L 640 330", 4.6, None)
    s.ink("M 604 470 q 36 16 72 0", 3.6, None)
    s.armure_miroirs(640, 408, 1.9, n=s.n(44), corps_col=s.C("eau"))
    # les deux tailleurs de miroirs
    s.personnage(276, 470, 1.6, s.C("accent"), bras="avant", bouche="droite")
    s.personnage(944, 476, 1.55, s.C("herbe2"), bras="avant", bouche="droite")
    for x, y, sc in ((372, 420, 10), (856, 426, 9)):
        s.eclat(x, y, sc, 1.2)
        s.etoile(x, y, sc * .6, "#FFFDF6", .9, anim="scintille")
    # les eclats par terre
    for i in range(s.n(30)):
        s.eclat(s.rnd.uniform(60, 1220), s.rnd.uniform(486, 528), s.rnd.uniform(3.4, 8),
                s.rnd.uniform(0, 3), anim="scintille" if i % 4 == 0 else None)
    s.add('<path d="%s" fill="%s" opacity="0.6"/>' % (blob(166, 508, 50, 20, 180, 11, .2), s.C("terre")))
    s.ink(blob(166, 508, 50, 20, 180, 11, .2), 1.5, None, op=.8)
    return s


def p10_a_p_tit_djou():
    s = S("p10", "A l'aube, les deux hommes scintillants prennent le chemin du chantoir", 43)
    s.wash(blob(700, 110, 620, 120, 191, 13, .22), s.C("fleur"), .22, "wc2")
    ciel(s, soleil=(.84, .22), nuage=(.26, .14))
    pre(s, 322)
    # le chemin qui file vers le chantoir
    chemin = wave(250, 548, 836, 372, 34, 1.3, 26)
    larg = [max(150 - i * 5.2, 16) for i in range(len(chemin))]
    s.wash(ribbon(chemin, larg), s.C("terre"), .42, "wc2")
    s.ink(smooth([(p[0] - larg[i] / 2, p[1]) for i, p in enumerate(chemin)]), 1.5, None, op=.5)
    s.ink(smooth([(p[0] + larg[i] / 2, p[1]) for i, p in enumerate(chemin)]), 1.5, None, op=.5)
    trou(s, 868, 366, 52, 17, pierres=False)
    # les deux, de dos, scintillants
    for (x, y, sc) in ((470, 476, 1.35), (586, 452, 1.2)):
        s.wash(smooth([(x - 12 * sc, y), (x + 54 * sc, y + 20 * sc), (x + 12 * sc, y + 4 * sc)], True),
               s.C("nuit"), .18, "wc2")
        s.personnage(x, y, sc, s.C("eau"), dos=True, bouche=None, bras="bas")
        s.ink("M %.1f %.1f L %.1f %.1f" % (x + 17 * sc, y - 36 * sc, x + 30 * sc, y - 92 * sc), 2.4 * sc * .8, None)
        s.ink("M %.1f %.1f L %.1f %.1f" % (x + 30 * sc, y - 92 * sc, x + 36 * sc, y - 116 * sc), 3.4 * sc * .8, SILVER)
        for i in range(s.n(20)):
            a = s.rnd.uniform(0, 6.3); rr = s.rnd.uniform(0, 1) ** .5
            s.eclat(x + math.cos(a) * rr * 17 * sc, y - 34 * sc + math.sin(a) * rr * 22 * sc,
                    s.rnd.uniform(2.4, 4.8) * sc * .85, a)
        for i in range(s.n(6)):
            s.etoile(x + s.rnd.uniform(-28, 42) * sc, y - s.rnd.uniform(4, 40) * sc,
                     s.rnd.uniform(2.6, 5.0), "#FFFDF6", .85, anim="scintille")
    # les alouettes
    for x, y, sc in ((214, 124, 1.15), (300, 92, .95), (156, 184, .8), (1024, 112, 1.0),
                     (1116, 152, .85), (548, 88, .9), (420, 140, 1.0)):
        s.oiseau(x, y, sc)
        s.ink("M %.1f %.1f q 6 14 -2 24" % (x, y + 3), 1.0, None, op=.25)
    s.semis(60, 1220, 470, 524, 12, s.C("fleur"), s.C("herbe2"))
    return s


def p11_li_combat():
    s = S("p11", "Le serpent contemple mille fois son image dans l'armure de miroirs", 47)
    s.wash(blob(640, 270, 600, 250, 201, 15, .16), s.C("nuit"), .18, "wc2")
    pre(s, 386, bandes=1)
    s.wash_blob(880, 300, 230, 220, s.C("soleil"), .3, f="wc2")
    for i in range(s.n(14)):
        a = 2 * math.pi * i / max(1, s.n(14))
        s.ink("M %.1f %.1f L %.1f %.1f" % (880 + math.cos(a) * 112, 300 + math.sin(a) * 112,
                                           880 + math.cos(a) * 236, 300 + math.sin(a) * 236),
              1.3, s.C("soleil"), op=.4)
    # le serpent, en gros plan
    pts = [(626, 250), (470, 212), (300, 254), (216, 362), (298, 466), (482, 500), (690, 486), (900, 512)]
    s.serpent(pts, 84, 13, s.C("serpent"), s.C("serpent2"))
    # l'homme-miroir
    s.armure_miroirs(898, 468, 2.3, n=s.n(48), corps_col=s.C("eau"))
    # dans plusieurs facettes, la tete du serpent reflechie
    for i in range(s.n(9)):
        a = s.rnd.uniform(0, 6.3); rr = s.rnd.uniform(.25, 1) ** .5
        ex, ey = 898 + math.cos(a) * rr * 44, 362 + math.sin(a) * rr * 62
        s.add('<g transform="translate(%.1f,%.1f) scale(0.21)" opacity="0.75">' % (ex, ey))
        s.add('<path d="M -44 -25 Q -4 -32 28 -22 Q 50 -14 55 -3 Q 56 7 46 12 Q 18 25 -44 25 Q -56 0 -44 -25 Z" fill="%s"/>' % s.C("serpent2"))
        s.add('<circle cx="14" cy="-9" r="10" fill="%s"/>' % s.C("soleil"))
        s.add("</g>")
    # les epees
    for (x0, y0, ang) in ((846, 418, 206), (862, 468, 196)):
        s.epee(x0, y0, ang, 190, 1.0)
    for x, y in ((700, 330), (646, 372), (742, 300)):
        s.add('<path d="M %.1f %.1f q 5 9 0 14 q -6 -5 0 -14 Z" fill="%s" opacity="0.75"/>' % (x, y, s.C("accent")))
    for i in range(s.n(12)):
        s.etoile(s.rnd.uniform(760, 1200), s.rnd.uniform(140, 470), s.rnd.uniform(3, 7),
                 "#FFFDF6", .7, anim="scintille")
    return s


def p12_li_rivnowe():
    s = S("p12", "Les juges stupefaits de voir revenir les deux combattants", 53)
    interieur(s, 400)
    # la porte ouverte, et le plein jour derriere
    porte = "M 540 500 L 540 288 Q 540 168 640 168 Q 740 168 740 288 L 740 500 Z"
    s.wash_blob(640, 300, 190, 230, s.C("soleil"), .3, f="wc2")
    s.aplat(porte, s.C("soleil"), .62)
    s.ink(porte, 3.4)
    s.ink("M 516 506 L 516 282 Q 516 144 640 144 Q 764 144 764 282 L 764 506", 4.4, None, op=.9)
    for k in range(5):
        s.ink("M %.1f 500 L %.1f %.1f" % (556 + k * 42, 556 + k * 42, 300 + abs(k - 2) * 26), 1.3, None, op=.3)
    # le banc des juges
    s.aplat(blob(640, 500, 600, 58, 214, 17, .06), s.C("terre"), .9)
    s.ink(blob(640, 500, 600, 58, 214, 17, .06), 2.4)
    for i, (x, sc) in enumerate(((176, 1.28), (334, 1.2), (946, 1.2), (1104, 1.28))):
        s.personnage(x, 470, sc, bouche="o", bras="haut")
        hy = 470 - 66 * sc - 26 - (i % 2) * 12          # le chapeau qui saute
        s.add('<path d="M %.1f %.1f q %.1f %.1f %.1f 0 q %.1f %.1f %.1f %.1f Z" fill="%s" opacity="0.92" transform="rotate(%.1f %.1f %.1f)"/>'
              % (x - 21 * sc, hy, 21 * sc, -20 * sc, 42 * sc, -3 * sc, 11 * sc, -42 * sc, 0,
                 s.st["encre"], -20 + i * 13, x, hy))
        for k in range(3):
            s.ink("M %.1f %.1f l %.1f %.1f" % (x - 15 + k * 15, hy + 18, -5 + k * 5, 17), 1.5, None, op=.55)
    # les deux revenants, a contre-jour
    for (x, y, sc) in ((562, 486, 1.9), (722, 492, 2.0)):
        s.armure_miroirs(x, y, sc, n=s.n(26), corps_col=s.C("nuit"))
        s.ink("M %.1f %.1f L %.1f %.1f" % (x + 20 * sc, y - 60 * sc, x + 30 * sc, y - 116 * sc), 2.6, None)
        s.ink("M %.1f %.1f L %.1f %.1f" % (x + 30 * sc, y - 116 * sc, x + 36 * sc, y - 146 * sc), 4.0, SILVER)
        for i in range(s.n(6)):
            s.add('<path d="M %.1f %.1f q 4 7 0 11 q -5 -4 0 -11 Z" fill="%s" opacity="0.8"/>'
                  % (x + s.rnd.uniform(-16, 16) * sc, y - 46 * sc + s.rnd.uniform(-22, 22) * sc, s.C("accent")))
    return s


def p13_li_pus_vude():
    s = S("p13", "La bete etendue, le puits desert, et tout le village accouru", 59)
    ciel(s)
    pre(s, 318)
    for i, fx in enumerate((.80, .875, .945)):
        s.maison(LW * fx, 316 - (i % 2) * 6, .58, s.C("mur"), s.C("toit"))
    trou(s, 838, 392, 78, 26)
    # le serpent etendu, d'un bord a l'autre
    ys = 452
    pts = [(64, ys + 8), (282, ys - 30), (512, ys + 5), (742, ys - 28), (972, ys + 3), (1228, ys - 22)]
    s.serpent(pts, 52, 9, s.C("serpent"), s.C("serpent2"), tete=False, op=.86)
    s.tete_serpent((64, ys + 8), (282, ys - 30), 50, s.C("serpent"), s.C("pierre"), langue=False)
    s.ink("M 26 446 l 20 13 M 26 459 l 20 -13", 2.2)
    for fx in (.30, .40, .50, .62, .72, .84):
        x, y = LW * fx, ys - 13
        s.ink("M %.1f %.1f l %.1f %.1f" % (x - 6, y - 10, 12, 20), 2.0, s.C("accent"), op=.7)
    # la procession
    s.procession(120, 700, 360, 11, (.40, .52))
    # les deux liberes, au premier plan, sans chaines
    for fx, sc in ((.135, 1.3), (.255, 1.4)):
        x, y = LW * fx, LH - 6
        s.personnage(x, y, sc, s.C("mur"), bras="haut", bouche="o")
        for i in range(s.n(12)):
            a = s.rnd.uniform(0, 6.3); rr = s.rnd.uniform(0, 1) ** .5
            s.eclat(x + math.cos(a) * rr * 16 * sc, y - 44 * sc + math.sin(a) * rr * 20 * sc,
                    s.rnd.uniform(2.4, 4.6), a, anim="scintille" if i % 3 == 0 else None)
    for x, y, sc in ((920, 118, 1.0), (1024, 92, .85), (820, 76, .75), (460, 104, .95)):
        s.oiseau(x, y, sc)
    s.semis(420, 1220, 480, 528, 18, s.C("fleur"), s.C("herbe2"))
    return s


PLANCHES = [("00-couverture", p00_couverture), ("01-li-pus", p01_li_pus),
            ("02-li-cherpint", p02_li_cherpint), ("03-les-tchesseus", p03_les_tchesseus),
            ("04-deus-condanes", p04_deus_condanes), ("05-pindards-fotches", p05_pindards_fotches),
            ("06-l-ideye", p06_l_ideye), ("07-l-offe", p07_l_offe),
            ("08-li-drossart", p08_li_drossart), ("09-l-armure", p09_l_armure),
            ("10-a-p-tit-djou", p10_a_p_tit_djou), ("11-li-combat", p11_li_combat),
            ("12-li-rivnowe", p12_li_rivnowe), ("13-li-pus-vude", p13_li_pus_vude)]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "illustrations")
    os.makedirs(out, exist_ok=True)
    for nom, fn in PLANCHES:
        svg = fn().render()
        open(os.path.join(out, nom + ".svg"), "w", encoding="utf-8").write(svg)
        print("%-24s %6d o" % (nom + ".svg", len(svg)))
