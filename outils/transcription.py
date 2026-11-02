# -*- coding: utf-8 -*-
"""Regénère texte/transcription.md depuis texte/pages.json.

Le livre découpe la légende en treize pages ; le bulletin, lui, compte moins
de paragraphes — certaines pages y sont soudées. Les regroupements ci-dessous
rendent le découpage du bulletin, pour que la transcription reste une copie
de l'article et non de notre pagination.
"""
import json, io, re, os

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(io.open(os.path.join(ICI, 'texte/pages.json'), encoding='utf-8'))
M, P = D['meta'], {p['n']: p for p in D['pages']}

GROUPES_WA = [[1], [2], [3], [4, 5], [6], [7], [8], [9], [10, 11], [12], [13]]
GROUPES_FR = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10, 11], [12], [13]]


def para(groupe, cle):
    """Un paragraphe du bulletin, recollé depuis une ou deux pages du livre.
    Les appels de note passent de <sup> au renvoi Markdown."""
    t = " ".join(P[n][cle] for n in groupe)
    return re.sub(r'<sup data-note="(\d+)">\d+</sup>', r'[^\1]', t)


o = []
o.append("# " + M['serie'])
o.append("")
o.append("Henri GRANDRY a traduit en wallon une légende recueillie par Georges LAPORT "
         "(Fraiture 1898 – Dachau 1945).")
o.append("")
o.append("*" + M['source'].replace(', rubrique', ' — rubrique') + "*")
o.append("")
o.append("---")
o.append("")
o.append("## LI TRÔ D' CHERPINT")
o.append("")
for g in GROUPES_WA:
    o.append(para(g, 'wa'))
    o.append("")
o.append("*Henri GRANDRY*")
o.append("")
for n in D['notes']:
    o.append("[^%d]: %s" % (n['n'], n['texte']))
o.append("")
o.append("*(Dans le bulletin, la liste imprimée intervertit les notes 3 et 4 par rapport "
         "aux appels du texte : « hart » appelle la note 3 et « volahe » la note 4. Elles sont "
         "rétablies ici en regard de l'appel auquel elles répondent.)*")
o.append("")
o.append("*(Le bulletin imprime « Henry GRANDRY » dans le chapeau et « Henri GRANDRY » sous "
         "la colonne wallonne. La graphie exacte est Henri ; elle a été rétablie ici dans le "
         "chapeau.)*")
o.append("")
o.append("---")
o.append("")
o.append("## Le trou du serpent")
o.append("")
for g in GROUPES_FR:
    o.append(para(g, 'fr'))
    o.append("")
o.append("*Georges LAPORT*")

io.open(os.path.join(ICI, 'texte/transcription.md'), 'w', encoding='utf-8').write(
    "\n".join(o) + "\n")
print("texte/transcription.md : %d paragraphes wallons, %d français"
      % (len(GROUPES_WA), len(GROUPES_FR)))
