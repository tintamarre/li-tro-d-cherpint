# -*- coding: utf-8 -*-
"""
Bibliotheque de dessin pour « Li tro d' cherpint ».

Vocabulaire graphique : un trait d'encre tremble et des aplats d'aquarelle
translucides qui se superposent en multiply. Le trait, lui, reste franc.
Tout est genere en SVG pur, sans dependance.
"""
import math, random

W, H = 720, 900

# --- palette sobre et chaude -------------------------------------------------
PAPER    = "#F6F0E4"
INK      = "#2E2419"
INK_SOFT = "#5B4A38"
OCHRE    = "#DFA94A"
SAND     = "#E8C98A"
TERRA    = "#C9714A"
OXBLOOD  = "#9A3F33"
MOSS     = "#86A066"
DEEPGRN  = "#4A6350"
SLATE    = "#6E86A6"
PALEBLUE = "#B5CBD8"
SILVER   = "#D4DEE1"
BROWN    = "#A07A4E"
NIGHT    = "#3B4668"
ROSE     = "#E0A697"
PEAU     = "#F0D2B0"
PIERRE   = "#C9BFA9"


# --- geometrie ---------------------------------------------------------------
def smooth(pts, closed=False, t=0.5):
    """Catmull-Rom -> cubiques de Bezier. Donne des courbes molles, dessinees."""
    if len(pts) < 2:
        return ""
    p = list(pts)
    p = ([pts[-1]] + list(pts) + [pts[0], pts[1]]) if closed else ([pts[0]] + list(pts) + [pts[-1]])
    d = "M %.1f %.1f" % (p[1][0], p[1][1])
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * t * 2, p1[1] + (p2[1] - p0[1]) / 6 * t * 2)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * t * 2, p2[1] - (p3[1] - p1[1]) / 6 * t * 2)
        d += " C %.1f %.1f %.1f %.1f %.1f %.1f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    return d + (" Z" if closed else "")


def blob(cx, cy, rx, ry, seed=0, n=11, wob=0.17):
    """Tache organique : un cercle dont chaque sommet respire."""
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + rnd.uniform(-wob, wob)
        pts.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    return smooth(pts, closed=True)


def ribbon(pts, widths):
    """Bande d'epaisseur variable le long d'une ligne : le corps du serpent."""
    left, right, n = [], [], len(pts)
    for i in range(n):
        x, y = pts[i]
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == n - 1:
            dx, dy = x - pts[-2][0], y - pts[-2][1]
        else:
            dx, dy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
        L = math.hypot(dx, dy) or 1
        nx, ny, w = -dy / L, dx / L, widths[i] / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return smooth(left) + " L " + smooth(list(reversed(right)))[2:] + " Z"


def wave(x0, y0, x1, y1, amp, cycles, n=40, phase=0.0):
    """Une ligne qui serpente d'un point a l'autre."""
    pts = []
    for i in range(n):
        t = i / (n - 1)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        off = math.sin(t * math.pi * cycles + phase) * amp
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1
        pts.append((x - dy / L * off, y + dx / L * off))
    return pts


# --- briques SVG -------------------------------------------------------------
class Scene:
    """Accumule les elements d'une planche et les serialise."""

    STYLE_DEFAUT = dict(encre=INK, encre_w=1.0, encre_op=1.0, tremble=2.4,
                        couleur="lavis", lavis_op=1.0, lavis_f="wc2", densite=1.0,
                        ciel_plein=True, contour_perso=True, joues=True, pal={})

    # Bord mouillé : le lavis s'arrête où le pinceau s'est levé, plutôt que net
    # au cadre — mais sur une vingtaine de pixels, pas davantage, sinon le fondu
    # mange le dessin. (déplacement du bord, flou, retrait) ; (7, 2.5, 5) est
    # plus discret encore, (0, 0.01, -2) revient au bord franc.
    BORD = (12, 4, 9)

    def __init__(self, slug, titre, seed=1, w=W, h=H, style=None, bord=None):
        self.slug, self.titre = slug, titre
        self.w, self.h = w, h
        self.st = dict(self.STYLE_DEFAUT, **(style or {}))
        self.bord = bord or self.BORD
        self.rnd = random.Random(seed)
        self.body = []

    def C(self, role, defaut=None):
        """Couleur d'un role, selon la palette du style."""
        return self.st["pal"].get(role, defaut or INK)

    def n(self, combien):
        """Un nombre de petits motifs, module par la densite du style."""
        return max(1, int(round(combien * self.st["densite"])))

    def add(self, s):
        self.body.append(s)

    # ---- aquarelle : toujours en multiply, pour que les passages se cumulent
    def wash(self, d, color, op=0.4, f="wc"):
        if self.st["couleur"] == "aplat":
            self.add('<path d="%s" fill="%s" opacity="%.2f" filter="url(#%s-wc)"/>'
                     % (d, color, min(1.0, op * 2.1 * self.st["lavis_op"]), self.slug))
            return
        self.add('<path d="%s" fill="%s" opacity="%.2f" filter="url(#%s-%s)" '
                 'style="mix-blend-mode:multiply"/>'
                 % (d, color, op * self.st["lavis_op"], self.slug, self.st["lavis_f"] if f == "wc2" else f))

    def wash_blob(self, cx, cy, rx, ry, color, op=0.4, seed=None, f="wc", wob=0.17, n=11):
        s = self.rnd.randint(0, 9999) if seed is None else seed
        self.wash(blob(cx, cy, rx, ry, s, n, wob), color, op, f)

    def aplat(self, d, color, op=1.0):
        """Couleur franche, sans multiply : pour les objets au premier plan."""
        self.add('<path d="%s" fill="%s" opacity="%.2f" filter="url(#%s-wc)"/>'
                 % (d, color, op, self.slug))

    # ---- encre
    def ink(self, d, w=2.2, color=None, cap="round", fill="none", op=1.0, dash=None):
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        c = color if color not in (None, INK) else self.st["encre"]
        if color == INK_SOFT:
            c = self.st["encre"]
        self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="%.1f" stroke-linecap="%s" '
                 'stroke-linejoin="round" opacity="%.2f"%s filter="url(#%s-ink)"/>'
                 % (d, fill, c, max(0.5, w * self.st["encre_w"]), cap,
                    min(1.0, op * self.st["encre_op"]), da, self.slug))

    def line(self, x0, y0, x1, y1, w=2.0, color=None, op=1.0):
        self.ink("M %.1f %.1f L %.1f %.1f" % (x0, y0, x1, y1), w, color, op=op)

    def dot(self, x, y, r, color=None, op=1.0):
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>'
                 % (x, y, r, color or INK, op))

    def cercle(self, x, y, r, fill="none", stroke=None, w=2.2, op=1.0):
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, r, fill, op))
        if stroke:
            self.ink("M %.1f %.1f a %.1f %.1f 0 1 1 %.1f 0 a %.1f %.1f 0 1 1 %.1f 0"
                     % (x - r, y, r, r, 2 * r, r, r, -2 * r), w, stroke)

    # ---- motifs ------------------------------------------------------------
    def touffe(self, x, y, s=1.0, color=None, n=5):
        c = color or DEEPGRN
        for i in range(n):
            a = -math.pi / 2 + (i - n / 2) * 0.33
            h = s * self.rnd.uniform(9, 18)
            self.ink("M %.1f %.1f Q %.1f %.1f %.1f %.1f"
                     % (x, y, x + math.cos(a) * h * 0.2, y + math.sin(a) * h * 0.6,
                        x + math.cos(a) * h * 0.55, y + math.sin(a) * h), 1.4 * s, c)

    def etoile(self, x, y, r, color=None, op=0.9, anim=None):
        d = ("M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f "
             "Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z") % (
            x, y - r, x + r * .18, y - r * .18, x + r, y, x + r * .18, y + r * .18, x, y + r,
            x - r * .18, y + r * .18, x - r, y, x - r * .18, y - r * .18, x, y - r)
        self.add('<path d="%s" fill="%s" opacity="%.2f"%s/>'
                 % (d, color or SAND, op, self.cls(anim) if anim else ""))

    def eclat(self, x, y, s, rot=0, color=SILVER, op=0.9, stroke=True, anim=None):
        """Eclat de miroir : un petit polygone qui accroche la lumiere."""
        rnd = random.Random(int(abs(x) * 7 + abs(y) * 13 + s * 31))
        pts = []
        n = rnd.choice([3, 4, 4, 5])
        for i in range(n):
            a = 2 * math.pi * i / n + rot
            r = s * rnd.uniform(0.6, 1.25)
            pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        d = "M " + " L ".join("%.1f %.1f" % p for p in pts) + " Z"
        self.add('<path d="%s" fill="%s" opacity="%.2f"%s/>'
                 % (d, color, op, self.cls(anim) if anim else ""))
        if stroke:
            self.ink(d, 0.9, INK_SOFT, op=.5)

    def mur(self, x0, y0, x1, y1, h=46, w=92, color=PIERRE, op=0.3, plinthe=True):
        """Appareil de pierre en assises décalées, chaque pierre d'un ton un peu à elle."""
        r, y = 0, y0
        while y < y1:
            c = x0 - (w // 2 if r % 2 else 0)
            while c < x1:
                k = self.rnd.uniform(.62, 1.5)
                d = ("M %.1f %.1f q %.1f -3 %.1f 0 q 3 %.1f 0 %.1f q %.1f 3 %.1f 0 q -3 %.1f 0 %.1f Z"
                     % (c + 4, y + h - 4, w * .5, w - 8, h * .5, h - 8, -w * .5, -(w - 8), -h * .5, -(h - 8)))
                self.add('<path d="%s" fill="%s" opacity="%.2f" style="mix-blend-mode:multiply"/>'
                         % (d, color, min(.62, op * k)))
                self.ink(d, 1.3, None, op=.3)
                c += w
            y += h
            r += 1
        if plinthe:
            self.ink(smooth(wave(x0 - 10, y1, x1 + 10, y1 - 5, 4, 2, 22)), 2.2, None, op=.5)

    def torche(self, x, y, s=1.0, halo=56):
        """Une torche fichée au mur : la douille, la flamme qui danse, la lueur."""
        self.ink("M %.1f %.1f l %.1f %.1f" % (x - 14 * s, y + 12 * s, 14 * s, -12 * s), 4.0 * s, None)
        self.add('<path d="M %.1f %.1f l %.1f %.1f l %.1f %.1f Z" fill="%s" opacity="0.9"/>'
                 % (x - 7 * s, y + 2 * s, 14 * s, 0, -7 * s, -13 * s, INK_SOFT))
        self.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="0.28"%s/>'
                 % (x, y - 20 * s, halo * s, halo * s * .95, self.C("soleil", "#F0E0B4"), self.cls("lueur")))
        self.add('<path d="M %.1f %.1f q %.1f %.1f %.1f %.1f q %.1f %.1f %.1f %.1f Z" fill="%s"%s/>'
                 % (x, y - 36 * s, 15 * s, 17 * s, 2 * s, 27 * s, -15 * s, -9 * s, -2 * s, -27 * s,
                    self.C("soleil", "#F0E0B4"), self.cls("flamme")))

    def maison(self, x, y, s=1.0, mur=SAND, toit=TERRA):
        w, h = 28 * s, 22 * s
        self.add('<path d="M %.1f %.1f h %.1f v %.1f h %.1f Z" fill="%s" opacity="0.95"/>'
                 % (x - w / 2, y, w, -h, -w, mur))
        self.add('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="%s" opacity="0.95"/>'
                 % (x - w / 2 - 4 * s, y - h, x, y - h - 15 * s, x + w / 2 + 4 * s, y - h, toit))
        self.ink("M %.1f %.1f h %.1f v %.1f h %.1f Z" % (x - w / 2, y, w, -h, -w), 1.4 * s, INK, op=.85)
        self.ink("M %.1f %.1f L %.1f %.1f L %.1f %.1f Z"
                 % (x - w / 2 - 4 * s, y - h, x, y - h - 15 * s, x + w / 2 + 4 * s, y - h), 1.4 * s, INK, op=.85)
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="0.9"/>'
                 % (x - 4.5 * s, y - h * .66, 9 * s, 9 * s, OCHRE))

    def semis(self, x0, x1, y0, y1, n=18, fleur=None, tige=None):
        """Des fleurs posees par petits bouquets plutot qu'au hasard."""
        bouquets = max(2, n // 4)
        for b in range(bouquets):
            bx = x0 + (x1 - x0) * ((b + .5) / bouquets + self.rnd.uniform(-.07, .07))
            by = y0 + (y1 - y0) * self.rnd.uniform(.15, .95)
            for k in range(self.rnd.randint(2, 4)):
                fx = bx + self.rnd.uniform(-22, 22)
                fy = by + self.rnd.uniform(-9, 9)
                h = self.rnd.uniform(9, 16)
                self.ink("M %.1f %.1f q %.1f %.1f %.1f %.1f"
                         % (fx, fy + h, self.rnd.uniform(-3, 3), -h * .5, self.rnd.uniform(-2, 2), -h),
                         1.1, tige or DEEPGRN, op=.7)
                self.add('<g%s>' % self.cls("souffle"))
                self.etoile(fx, fy, self.rnd.uniform(3.0, 5.0), fleur or ROSE, .85)
                self.add('</g>')

    def procession(self, x0, x1, y, n=12, ech=(.40, .58), ondule=8, **kw):
        """Une file de villageois, par grappes et a des tailles variees."""
        i, k = 0, 0
        while i < n:
            grappe = min(n - i, self.rnd.randint(1, 3))
            bx = x0 + (x1 - x0) * (i / max(1, n - 1))
            for j in range(grappe):
                t = (i + j) / max(1, n - 1)
                sc = self.rnd.uniform(*ech) * (0.88 + t * 0.3)
                self.personnage(bx + j * self.rnd.uniform(16, 26) + self.rnd.uniform(-5, 5),
                                y + math.sin(k * 1.7) * ondule + self.rnd.uniform(-4, 4) + t * 10,
                                sc, bouche="o" if k % 4 == 0 else "sourire", **kw)
                k += 1
            i += grappe

    def oiseau(self, x, y, s=1.0, color=None, op=0.85, anim="derive"):
        if anim:
            self.add('<g%s>' % self.cls(anim))
        self.ink("M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f"
                 % (x - 10 * s, y, x - 5 * s, y - 7 * s, x, y - 1.5 * s,
                    x + 5 * s, y - 7 * s, x + 10 * s, y), 1.6 * s, color or INK_SOFT, op=op)
        if anim:
            self.add('</g>')

    # ---- personnages --------------------------------------------------------
    def personnage(self, x, y, s=1.0, robe=None, peau=PEAU, cheveux=None, chapeau=None,
                   bras="bas", regard=(0, 0), bouche="sourire", dos=False, op=1.0, cligne=None):
        """Une petite personne ronde : jambes, tunique, bras, tete, joues.

        y est au sol. La silhouette fait environ 76*s de haut.
        """
        r = robe or self.rnd.choice([SLATE, TERRA, MOSS, BROWN, OXBLOOD, NIGHT])
        ch = cheveux if cheveux is not None else self.rnd.choice([INK_SOFT, INK, "#6B4A2E", "#8A6A47"])
        hx, hy, hr = x, y - 56 * s, 13 * s
        self.add('<g opacity="%.2f">' % op)
        # jambes
        for k in (-1, 1):
            self.ink("M %.1f %.1f L %.1f %.1f" % (x + k * 6 * s, y - 17 * s, x + k * 7 * s, y - 3 * s), 3.4 * s, INK_SOFT)
            self.ink("M %.1f %.1f q %.1f 0 %.1f -1" % (x + k * 7 * s - k * 1.5 * s, y - 2 * s, k * 8 * s, k * 8 * s), 3.6 * s, INK)
        # tunique
        corps = smooth([(x - 18 * s, y - 13 * s), (x - 15 * s, y - 32 * s), (x - 10 * s, y - 44 * s),
                        (x, y - 46 * s), (x + 10 * s, y - 44 * s), (x + 15 * s, y - 32 * s),
                        (x + 18 * s, y - 13 * s), (x, y - 9 * s)], True)
        self.aplat(corps, r, .95)
        self.ink(corps, 2.0 * s, INK, op=.9)
        # bras
        if bras == "haut":
            geo = [(-1, -40, -26, -62, -32, -86), (1, -40, 26, -62, 32, -86)]
        elif bras == "avant":
            geo = [(-1, -38, -26, -34, -34, -24), (1, -38, 26, -34, 34, -24)]
        elif bras == "croises":
            geo = [(-1, -38, -18, -26, 6, -22), (1, -38, 18, -26, -6, -26)]
        else:
            geo = [(-1, -38, -24, -28, -20, -12), (1, -38, 24, -28, 20, -12)]
        for k, ay, cx2, cy2, ex, ey in geo:
            d = ("M %.1f %.1f Q %.1f %.1f %.1f %.1f"
                 % (x + k * 14 * s, y + ay * s, x + cx2 * s, y + cy2 * s, x + ex * s, y + ey * s))
            self.ink(d, 6.4 * s, INK)              # le cerne
            self.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" '
                     'filter="url(#%s-ink)"/>' % (d, r, 4.0 * s, self.slug))   # la manche
            self.cercle(x + ex * s, y + ey * s, 4.0 * s, peau, INK, 1.5 * s)
        # tete
        self.cercle(hx, hy, hr, peau, INK, 2.1 * s)
        # cheveux : une calotte posee sur le crane
        self.add('<path d="M %.1f %.1f a %.1f %.1f 0 0 1 %.1f 0 q %.1f %.1f %.1f %.1f q %.1f %.1f %.1f %.1f Z" fill="%s" opacity="0.95"/>'
                 % (hx - hr, hy - 1 * s, hr, hr, 2 * hr, -2 * s, -3 * s, -5 * s, -1 * s,
                    -4 * s, 4 * s, -2 * hr + 10 * s, 0, ch))
        if not dos:
            dx, dy = regard
            # au loin, les yeux restent tranquilles : seuls les gros plans clignent
            cl = (s >= 1.15) if cligne is None else cligne
            if cl:
                self.add('<g%s>' % self.cls("oeil", self.rnd.uniform(5.5, 9.0)))
            for k in (-1, 1):
                self.dot(hx + k * 4.6 * s + dx * s, hy - 1 * s + dy * s, 1.7 * s, INK)
            if cl:
                self.add('</g>')
            if self.st["joues"]:
                for k in (-1, 1):
                    self.dot(hx + k * 8.4 * s, hy + 4 * s, 3.2 * s, ROSE, .55)
            if bouche == "sourire":
                self.ink("M %.1f %.1f q %.1f %.1f %.1f 0" % (hx - 3.4 * s, hy + 5.5 * s, 3.4 * s, 3.4 * s, 6.8 * s), 1.5 * s, INK, op=.85)
            elif bouche == "o":
                self.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>' % (hx, hy + 6.5 * s, 2.6 * s, 3.6 * s, INK))
            elif bouche == "droite":
                self.ink("M %.1f %.1f l %.1f 0" % (hx - 3.4 * s, hy + 6.5 * s, 6.8 * s), 1.5 * s, INK, op=.85)
        if chapeau == "juge":
            self.add('<path d="M %.1f %.1f q %.1f %.1f %.1f 0 q %.1f %.1f %.1f %.1f Z" fill="%s" opacity="0.95"/>'
                     % (hx - 21 * s, hy - 7 * s, 21 * s, -20 * s, 42 * s, -3 * s, 11 * s, -42 * s, 0, INK_SOFT))
            self.ink("M %.1f %.1f q %.1f %.1f %.1f 0" % (hx - 21 * s, hy - 7 * s, 21 * s, -20 * s, 42 * s), 1.8 * s, INK)
        elif chapeau == "bonnet":
            self.add('<path d="M %.1f %.1f q %.1f %.1f %.1f 0 q %.1f %.1f %.1f %.1f Z" fill="%s" opacity="0.95"/>'
                     % (hx - 14 * s, hy - 7 * s, 14 * s, -26 * s, 28 * s, -2 * s, 8 * s, -28 * s, 0, OXBLOOD))
            self.ink("M %.1f %.1f q %.1f %.1f %.1f 0" % (hx - 14 * s, hy - 7 * s, 14 * s, -26 * s, 28 * s), 1.6 * s, INK)
        self.add("</g>")
        return (hx, hy, hr)

    def fers(self, x, y, s=1.0):
        """Une paire de fers ouverts, jetée dans l'herbe."""
        r = 13 * s
        for k in (-1, 1):
            cx = x + k * 30 * s
            self.ink("M %.1f %.1f a %.1f %.1f 0 1 1 %.1f %.1f"
                     % (cx - r, y, r, r * .82, 1.85 * r, -r * .42), 3.2 * s)
        for i in range(4):
            self.cercle(x - 13 * s + i * 9 * s, y + 3 * s, 3.6 * s, "none", self.st["encre"], 2.1 * s)

    def epee(self, x, y, ang, L=90, s=1.0):
        """Une epee bien effilee, tenue a la main."""
        a = math.radians(ang)
        ex, ey = x + math.cos(a) * L, y + math.sin(a) * L
        self.ink("M %.1f %.1f L %.1f %.1f" % (x, y, ex, ey), 6.0 * s, SILVER)
        self.ink("M %.1f %.1f L %.1f %.1f" % (x, y, ex, ey), 1.9 * s, INK, op=.9)
        px, py = -math.sin(a), math.cos(a)
        self.ink("M %.1f %.1f L %.1f %.1f" % (x + px * 11 * s, y + py * 11 * s,
                                              x - px * 11 * s, y - py * 11 * s), 4.0 * s, INK_SOFT)
        self.ink("M %.1f %.1f L %.1f %.1f" % (x, y, x - math.cos(a) * 15 * s, y - math.sin(a) * 15 * s), 5.0 * s, BROWN)
        gx, gy = x + math.cos(a) * L * .62, y + math.sin(a) * L * .62     # le reflet qui court sur la lame
        self.add('<g%s>' % self.cls("scintille", 4.4))
        self.etoile(gx, gy, 7 * s, "#FFFDF6", .95)
        self.add('</g>')

    def armure_miroirs(self, x, y, s=1.0, n=46, tete=True, corps_col=SILVER, anim=True):
        """Le costume fantastique : une silhouette pavée d'éclats qui accrochent le jour."""
        # jambes
        for k in (-1, 1):
            self.ink("M %.1f %.1f L %.1f %.1f" % (x + k * 8 * s, y - 20 * s, x + k * 10 * s, y - 3 * s), 4.4 * s, INK)
            self.ink("M %.1f %.1f q %.1f 0 %.1f -1" % (x + k * 8.5 * s, y - 2 * s, k * 9 * s, k * 9 * s), 4.0 * s, INK)
        corps = blob(x, y - 50 * s, 23 * s, 31 * s, int(abs(x) + abs(y)), 15, .09)
        self.aplat(corps, corps_col, .9)
        self.ink(corps, 2.6 * s, INK)
        # bras
        for k in (-1, 1):
            d = ("M %.1f %.1f Q %.1f %.1f %.1f %.1f"
                 % (x + k * 18 * s, y - 66 * s, x + k * 32 * s, y - 50 * s, x + k * 28 * s, y - 28 * s))
            self.ink(d, 6.6 * s, INK)
            self.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" '
                     'filter="url(#%s-ink)"/>' % (d, corps_col, 4.2 * s, self.slug))
        for i in range(n):
            a = self.rnd.uniform(0, 6.3)
            rr = self.rnd.uniform(0, 1) ** .5
            self.eclat(x + math.cos(a) * rr * 20 * s, y - 50 * s + math.sin(a) * rr * 28 * s,
                       self.rnd.uniform(2.8, 6.0) * s, a, SILVER, .95,
                       anim="scintille" if (anim and i % 4 == 0) else None)
        if tete:
            # le heaume, avec sa fente de visée
            self.cercle(x, y - 94 * s, 13 * s, corps_col, INK, 2.5 * s, .92)
            self.ink("M %.1f %.1f l %.1f 0" % (x - 8 * s, y - 96 * s, 16 * s), 2.2 * s, INK, op=.7)
            for i in range(max(4, n // 6)):
                a = self.rnd.uniform(0, 6.3)
                rr = self.rnd.uniform(0, 1) ** .5
                self.eclat(x + math.cos(a) * rr * 10 * s, y - 94 * s + math.sin(a) * rr * 10 * s,
                           self.rnd.uniform(2.2, 4.2) * s, a, SILVER, .95,
                           anim="scintille" if (anim and i % 3 == 0) else None)

    # ---- le serpent ---------------------------------------------------------
    def serpent(self, pts, w_max=46, w_min=5, couleur=MOSS, ombre=DEEPGRN,
                ecailles=True, tete=True, oeil=OCHRE, op=0.92):
        n = len(pts)
        widths = [w_min + (w_max - w_min) * (math.sin(math.pi * (i / (n - 1)) ** .78) ** .6) for i in range(n)]
        widths[-1] = w_min * .6
        corps = ribbon(pts, widths)
        self.aplat(corps, couleur, op)
        self.add('<path d="%s" fill="%s" opacity="0.45" filter="url(#%s-wc)" style="mix-blend-mode:multiply"/>'
                 % (ribbon([(x, y + 4) for x, y in pts], [w * .4 for w in widths]), SAND, self.slug))
        self.ink(corps, 2.4, INK, op=.92)
        if ecailles:
            for i in range(3, n - 4, 2):
                x, y = pts[i]
                w = widths[i] * .34
                self.ink("M %.1f %.1f Q %.1f %.1f %.1f %.1f"
                         % (x - w, y - w * .5, x, y + w * .55, x + w, y - w * .5), 1.2, ombre, op=.6)
        if tete:
            self.tete_serpent(pts[0], pts[1], widths[0] * 2.5, couleur, oeil)

    def tete_serpent(self, p, q, taille, couleur=MOSS, oeil=OCHRE, langue=True, vivant=True, mort=False):
        a = math.degrees(math.atan2(p[1] - q[1], p[0] - q[0]))
        k = max(taille, 26) / 46.0
        self.add('<g transform="translate(%.1f,%.1f) rotate(%.1f) scale(%.2f)">' % (p[0], p[1], a, k))
        enc = self.st["encre"]
        ew = self.st["encre_w"]
        d = ("M -44 -25 Q -4 -32 28 -22 Q 50 -14 55 -3 Q 56 7 46 12 "
             "Q 18 25 -44 25 Q -56 0 -44 -25 Z")
        self.add('<path d="%s" fill="%s" opacity="0.96" filter="url(#%s-wcb)"/>' % (d, couleur, self.slug))
        self.add('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linejoin="round" filter="url(#%s-inkb)"/>'
                 % (d, enc, 2.6 * ew, self.slug))
        # machoire et arcade
        self.add('<path d="M 52 4 Q 20 15 -26 17" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.55" stroke-linecap="round"/>' % (enc, 1.7 * ew))
        self.add('<path d="M 30 -24 Q 14 -30 -4 -27" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.4" stroke-linecap="round"/>' % (enc, 1.5 * ew))
        # oeil
        if mort:
            # l'oeil est éteint et barré, la gueule pend
            self.add('<circle cx="14" cy="-9" r="10.5" fill="#D6D3C8"/>')
            self.add('<circle cx="14" cy="-9" r="10.5" fill="none" stroke="%s" stroke-width="%.1f"/>' % (enc, 2.2 * ew))
            self.add('<path d="M 7.5 -16 L 20.5 -2 M 7.5 -2 L 20.5 -16" fill="none" stroke="%s" '
                     'stroke-width="%.1f" stroke-linecap="round"/>' % (enc, 2.8 * ew))
            self.add('<path d="M 55 6 Q 40 20 22 20" fill="none" stroke="%s" stroke-width="%.1f" '
                     'stroke-linecap="round" opacity="0.8"/>' % (enc, 2.0 * ew))
        else:
            self.add('<circle cx="14" cy="-9" r="10.5" fill="%s"/>' % oeil)
            self.add('<circle cx="14" cy="-9" r="10.5" fill="none" stroke="%s" stroke-width="%.1f"/>' % (enc, 2.2 * ew))
            self.add('<ellipse cx="15" cy="-9" rx="2.9" ry="7.6" fill="%s"%s/>'
                     % (enc, self.cls("oeil") if vivant else ""))
            self.add('<circle cx="10.2" cy="-12.8" r="2.7" fill="#FFFDF6" opacity="0.95"%s/>'
                     % (self.cls("scintille") if vivant else ""))
        self.add('<circle cx="47" cy="-7" r="1.9" fill="%s" opacity="0.7"/>' % enc)
        if langue:
            self.add('<path d="M 55 3 Q 74 5 82 -5 M 74 5 Q 82 10 86 19" fill="none" stroke="%s" '
                     'stroke-width="2.4" stroke-linecap="round"%s/>' % (OXBLOOD, self.cls("dardille")))
        self.add("</g>")

    CSS = """<style>
  @keyframes flamme{0%,100%{transform:scaleY(1) rotate(0deg)}28%{transform:scaleY(1.14) rotate(-3.5deg)}
    55%{transform:scaleY(.92) rotate(2.5deg)}78%{transform:scaleY(1.06) rotate(-1.5deg)}}
  @keyframes lueur{0%,100%{opacity:.26}50%{opacity:.48}}
  @keyframes cligne{0%,91%,100%{transform:scaleY(1)}95.5%{transform:scaleY(.06)}}
  @keyframes scintille{0%,100%{opacity:.22}50%{opacity:1}}
  @keyframes derive{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
  @keyframes onde{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}
  @keyframes respire{0%,100%{transform:scale(1)}50%{transform:scale(1.035)}}
  @keyframes balance{0%,100%{transform:rotate(-2.6deg)}50%{transform:rotate(2.6deg)}}
  @keyframes souffle{0%,100%{transform:rotate(-2deg)}50%{transform:rotate(2.4deg)}}
  @keyframes dardille{0%,74%,100%{opacity:0;transform:scaleX(.45)}80%,92%{opacity:1;transform:scaleX(1)}}
  @keyframes glisse{0%{transform:translate(0,0)}50%{transform:translate(14px,-7px)}100%{transform:translate(0,0)}}
  @keyframes rayon{0%,100%{opacity:.18}50%{opacity:.48}}
  @keyframes bascule{0%,100%{transform:rotate(-1.5deg)}50%{transform:rotate(1.5deg)}}
  @keyframes file{to{stroke-dashoffset:-34}}
  @keyframes gigote{0%,100%{transform:rotate(-1.6deg) translateY(0)}50%{transform:rotate(1.6deg) translateY(-3px)}}
  .flamme{animation:flamme 1.7s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
  .lueur{animation:lueur 2.8s ease-in-out infinite}
  .oeil{animation:cligne 6.5s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 50%}
  .scintille{animation:scintille 3.6s ease-in-out infinite}
  .derive{animation:derive 6.5s ease-in-out infinite;transform-box:fill-box}
  .onde{animation:onde 7.5s ease-in-out infinite;transform-box:fill-box}
  .respire{animation:respire 9s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 50%}
  .balance{animation:balance 4.4s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 0}
  .souffle{animation:souffle 5.2s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
  .dardille{animation:dardille 3.8s ease-in-out infinite;transform-box:fill-box;transform-origin:0 50%}
  .glisse{animation:glisse 13s ease-in-out infinite;transform-box:fill-box}
  .rayon{animation:rayon 5.5s ease-in-out infinite}
  .bascule{animation:bascule 7.5s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 50%}
  .file{animation:file 2.6s linear infinite}
  .gigote{animation:gigote 4.6s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 50%}
  @media (prefers-reduced-motion:reduce){
    .flamme,.lueur,.oeil,.scintille,.derive,.onde,.respire,
    .balance,.souffle,.dardille,.glisse,.rayon,.bascule,.file,.gigote{animation:none}}
</style>"""

    def cls(self, nom, duree=None):
        """Attribut de classe animee, avec un dephasage propre a chaque element."""
        # le déphasage couvre tout le cycle : sinon les clignements se groupent
        d = ' style="animation-delay:-%.2fs%s"' % (
            self.rnd.uniform(0, duree if duree else 4),
            ";animation-duration:%.2fs" % duree if duree else "")
        return ' class="%s"%s' % (nom, d)

    def chandelle(self, x, y, h=58, w=19, halo=38):
        """Une chandelle : le suif, la mèche, la flamme qui bouge, le halo qui respire."""
        s_ = self
        s_.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" opacity="0.95"/>'
               % (x - w / 2, y - h, w, h, w * .27, self.C("mur", "#EFE7D6")))
        s_.ink("M %.1f %.1f l 0 %.1f q %.1f -7 %.1f 0 l 0 %.1f" % (x - w / 2, y, -(h - 6), w / 2, w, h - 6), 2.0)
        s_.ink("M %.1f %.1f L %.1f %.1f" % (x, y - h, x, y - h - 7), 1.6)
        s_.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="0.30"%s/>'
               % (x, y - h - 16, halo, halo * .95, self.C("soleil", "#F0E0B4"), self.cls("lueur")))
        s_.add('<path d="M %.1f %.1f q %.1f %.1f %.1f %.1f q %.1f %.1f %.1f %.1f Z" fill="%s"%s/>'
               % (x, y - h - 30, 13, 15, 2, 24, -13, -8, -2, -24,
                  self.C("soleil", "#F0E0B4"), self.cls("flamme")))

    # ---- serialisation ------------------------------------------------------
    def defs(self):
        """Les filtres, en coordonnees utilisateur : une region en pourcentage
        de la boite englobante s'annule sur un trait parfaitement vertical."""
        a, b, c = self.rnd.randint(1, 99), self.rnd.randint(1, 99), self.rnd.randint(1, 99)
        reg = 'filterUnits="userSpaceOnUse" x="-80" y="-80" width="%d" height="%d"' % (self.w + 160, self.h + 160)
        return """<defs>
  <filter id="S-wc" REG>
    <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="4" seed="%d" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="0.7"/>
  </filter>
  <filter id="S-wc2" REG>
    <feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="4" seed="%d" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="15" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="2.4"/>
  </filter>
  <filter id="S-ink" REG>
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="%d" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="TREMBLE" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <!-- Variantes en unités de boîte : à l'intérieur d'un groupe transformé, une
       région en coordonnées utilisateur est tournée et décalée avec lui, et rogne. -->
  <filter id="S-wcb" x="-30%%" y="-30%%" width="160%%" height="160%%">
    <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="4" seed="%d" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="0.7"/>
  </filter>
  <filter id="S-inkb" x="-25%%" y="-25%%" width="150%%" height="150%%">
    <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="%d" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="TREMBLE" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="S-bord" REG>
    <feTurbulence type="fractalNoise" baseFrequency="0.0055" numOctaves="4" seed="%d" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="BORD_D" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="BORD_B"/>
  </filter>
  <mask id="S-marge" maskUnits="userSpaceOnUse" x="0" y="0" width="MW" height="MH">
    <rect x="BORD_I" y="BORD_J" width="MW2" height="MH2" fill="#fff" filter="url(#S-bord)"/>
  </mask>
  <filter id="S-grain" REG>
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="%d" result="t"/>
    <feColorMatrix in="t" type="saturate" values="0"/>
  </filter>
</defs>""".replace("S-", self.slug + "-").replace("REG", reg) \
           .replace("TREMBLE", "%.1f" % self.st["tremble"]) \
           .replace("BORD_D", "%.0f" % self.bord[0]).replace("BORD_B", "%.0f" % self.bord[1]) \
           .replace("BORD_I", "%.0f" % self.bord[2]).replace("BORD_J", "%.0f" % (self.bord[2] * .8)) \
           .replace("MW2", "%.0f" % (self.w - 2 * self.bord[2])) \
           .replace("MH2", "%.0f" % (self.h - 1.6 * self.bord[2])) \
           .replace("MW", str(self.w)).replace("MH", str(self.h)) % (a, b, c, a, a, a, c)

    def render(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
                'aria-labelledby="%s-t">\n<title id="%s-t">%s</title>\n%s\n%s\n'
                '<g mask="url(#%s-marge)">\n%s\n'
                '<rect width="%d" height="%d" filter="url(#%s-grain)" opacity="0.05" '
                'style="mix-blend-mode:multiply" pointer-events="none"/>\n</g>\n</svg>\n'
                % (self.w, self.h, self.slug, self.slug, self.titre, self.CSS, self.defs(),
                   self.slug, "\n".join(self.body), self.w, self.h, self.slug))
