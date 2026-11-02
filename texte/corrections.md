# Reprise du texte wallon sur le scan du bulletin

Le 2 novembre 2026, Henri Grandry nous a signalé des fautes d'orthographe et de typographie dans la reprise de sa traduction. Le texte avait été ressaisi depuis une photo de *Sprimont Infos* (octobre 2026, p. 24) : les fautes étaient les nôtres.

Le texte a été **entièrement relu sur un scan à 340 dpi** et corrigé dans `texte/pages.json`, qui reste la source unique. `texte/transcription.md` en est désormais regénéré par `outils/transcription.py`, pour que les deux ne puissent plus diverger.

---

## 1. La faute principale : le å

Henri Grandry écrit le **å** (a rond en chef, la « a-ring » du système Feller, qui note le son intermédiaire entre *a* et *o*). Nous l'avions rendu par **â** presque partout, sauf dans un paragraphe. Il y en a **38** dans le texte.

Corrigés : `måle`, `målureûs`, `målureûs'mint`, `måleurs`, `åtoû`, `å djins`, `Å-d'-fêt`, `måy`, `qu'on-åvahe`, `rin-n'-våts`, `åvît`, `condånés`, `condånåcion`, `fåtifs`, `cåse`, `å cis`, `ås` (3 fois), `pindårds`, `ahåyan`, `tribunål`, `Mågré`, `gråce`, `d'årmure`, `Å p'tit djoû`, `s'atårdjant`, `Leûs-z-årmures`, `lårdé`, `contrôler å d' fêt`, `s' no å chantwér`, `vårè`, `på`, `drossårt`, `pårt`.

Le bandeau de l'article porte lui aussi `Lédjinde **åtoû** d'Lincé Sprimont` : corrigé dans le titre de série.

Reste un seul `â` dans tout le texte, `l'ocâsion` (page 11), lu tel quel sur le scan — **à confirmer**.

## 2. Les autres fautes de saisie, corrigées

| Page | Nous avions | Le bulletin porte |
|---|---|---|
| 02 | `dès ans èt dès ra-z-ans` | `dès ans et dès ra-z-ans` |
| 03 | `d' leû tchèsse` | `d'leû tchèsse` |
| 03 | `d'ine djin` | `d' ine djin` |
| 03 | `novès` | `novês` |
| 04 | `al potence` | `al potince` |
| 04 | `qu'èstît fatifs` | `qu' èstît fåtifs` |
| 04 | `so leu fôrfèt` | `so leu fôrfêt` |
| 06 | `Li mèsse djudge` | `Li mêsse djudge` |
| 08 | `d' trop s'ègadjî` | `d' trop' s'ègadjî` |
| 09 | `d'acwèrds` | `d'acwérds` |
| 10 | `ine epèye` | `ine èpèye` |
| 10 | `l' vôye de tchantwér` | `l' vôye dè tchantwér` |
| 11 | `lî revoyève` | `lî rèvoyève` |
| 12 | `Lès djudjes èstît ewèrer` | `Lès djudjes estît ewèrer` |
| 12 | `leû libèrté` | `leû liberté` |
| 13 | `di viyèdjes` | `dè viyèdjes` |
| 13 | `d'Xhignez` | `d' Xhignez` |
| 13 | `storeye` | `storèye` |
| 13 | `Lès condånés avît` | `Lès condånés avit` |

Côté français, deux fautes seulement : `« li trô â serpint »` → `« li trô å serpint »` (page 1) et `Le « pus' » était désert` → `Le « pus » était désert` (page 13). Le reste de la colonne de Georges Laport était conforme.

Note 1 : le bulletin met un **point-virgule**, `Pwèrtéve hisse ; faisait horreur`, et non deux points.

## 3. Ce que nous avions cru fautif et qui ne l'est pas

Vérifié sur le scan, et donc laissé tel quel : `coula` (page 6) et `çoula` ailleurs, `deus vèyes` sans accent, `Li pus' esteût vûde` sans accent sur le premier *e*, `Min n'alons nin trop reû`, `chérpint` (page 2) à côté de `chèrpint` et de `tchèrpint` (page 12), `chantwér` (page 13) à côté de `tchantwér`, `logis'` (page 13) à côté de `lodjis'` (page 2), `s-trô`, `so l' pote`, `lès deûs k'péres`, `Tavlè på ahåyan`, `l'îdêye` à côté de `idèye`, `lêus-z-èpèyes` à côté de `leûs-z-èpèyes`, `de Sprimont` sans accent, et la virgule suivie d'une majuscule page 10 (`bin tchèrpèye, I s' ènn' alît`).

La note 2 s'arrête bien au milieu d'une phrase dans le bulletin — *« gibet à plusieurs potences que les seigneurs des lieux »* — ce n'est pas une coupure de notre fait.

Et la liste imprimée des notes intervertit bien 3 et 4 par rapport aux appels du texte.

---

## 4. Ce qui reste à lui demander

**Quatre corrections de composition** que nous avons appliquées parce qu'elles ressemblent à des accidents de mise en page, et qu'il faut lui faire confirmer :

1. Les guillemets. Le bulletin écrit `«on pus'»` serré au premier paragraphe et `« li trô d' chèrpint »` espacé trois lignes plus bas. Nous avons mis partout la forme espacée.
2. Page 7, `qu'on v's-aveût léhou .` — espace avant le point, supprimée.
3. Page 13, `on 'lzès libèra  rad'mint` — double espace, réduite à une.
4. Page 10, `i s 'moûssît` — l'apostrophe est collée au mot suivant au lieu du précédent ; rétablie en `i s' moûssît`.

**Deux questions de fond :**

5. `l'ocâsion` (page 11) est le seul `â` du texte. Faut-il lire `l'ocåsion` ?
6. Page 7, les guillemets s'emboîtent : `« Dimin, vos d'vez-t-èsse sitronlé avou l' « hart »… »`. Faut-il un autre dessin pour les intérieurs, ou aucun ?

**Et deux choses à lui signaler :**

7. Les apostrophes sont toutes saisies en apostrophe droite `'`. Le livre resserre typographiquement le blanc après les élisions d'une ou deux lettres (`l'`, `d'`, `s'`, `n'`, `qu'`), sans toucher au texte : les apostrophes qui sont des lettres du mot — `pus'`, `song'`, `nut'`, `lodjis'`, `trop'` — gardent leur espace entière.
8. Les treize titres de page (« Li lodjis' dè chérpint », « Å p'tit djoû », …) **sont de nous** : le bulletin n'en a pas. Ils servent à découper la légende en pages. À relire par lui, et à retirer s'il préfère.
