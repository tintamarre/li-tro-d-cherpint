# Relevé à soumettre à Henri Grandry

Henri Grandry signale, le 2 novembre 2026, « quelques fautes d'orthographe et de typographie » dans la reprise de sa traduction. Le texte wallon de ce livre a été ressaisi à la main depuis la photo de *Sprimont Infos* (octobre 2026, p. 24) : les fautes sont donc les nôtres, pas les siennes.

Ce fichier liste ce qui est **douteux à la relecture interne** — un même mot écrit de deux façons d'une page à l'autre, une accentuation qui saute, une typographie incertaine. Ce n'est pas une liste de corrections : c'est une liste de questions. La réponse d'Henri Grandry fait foi, et lui seul tranche.

Une fois tranché : corriger `texte/pages.json` (source unique), puis `python3 outils/site.py` pour regénérer `assets/livre-data.js`. `texte/transcription.md` est à corriger en parallèle.

---

## 1. Un mot, deux graphies

| Page | Écrit | Ailleurs | Question |
|---|---|---|---|
| 02 | `chérpint` (titre et corps) | `chèrpint` (01, 03, 07) | è ou é ? |
| 12 | `tchèrpint` | `chèrpint` | avec ou sans t initial ? |
| 13 | `chantwér` | `tchantwér` (01, 02, 10) | idem |
| 13 | `logis'` | `lodjis'` (02) | dj ou g ? |
| 09 | `l'îdêye` | `idèye` (06, titre et corps) | quelle forme ? |
| 12 | `ewèrer` | `èwarèye` (13) | même racine, deux vocalismes |
| 08 | `tower` | `touwer` (03), `touwerèyes` (05) | ou / o ? |
| 10 | `epèye` | `èpèyes` (11, 12) | accent manquant ? |
| 11 | `lêus-z-èpèyes` | `leûs-z-èpèyes` (12) | ê ou eû ? |
| 13 | `â d' fêt` | `Â-d-fêt` (01) | traits d'union ou apostrophe ? |
| 13 | `s-trô` | `s' trô` (02) | trait d'union ou apostrophe ? |

## 2. Accents probablement tombés à la saisie

| Page | Écrit | Attendu ailleurs |
|---|---|---|
| 13 | `Li pus' esteût vûde` (titre **et** corps) | `èsteût` (02, 12) |
| 04 | `âvît stu` | `avît` (03) |
| 06 | `spagnereût deus vèyes` | `deûs` (01, 03, 09, 10, 11) |
| 06 | `Come coula` | `çoula` (02, 07, 09) |
| 04 | `so leu fôrfèt` | `leû` (passim) |
| 04 | `cis dès ban de Sprimont` | `dè` (passim) |
| 10 | `l' vôye de tchantwér` | `dè` |
| 04 | `Min n'alons nin trop reû` | `Mins` (03) |

## 3. La page 08, à relire en entier

C'est le seul paragraphe où apparaît le **å** (`drossårt`, `D'ôte på`, `vårè`), alors que tout le reste du texte emploie **â** (`pâ` en 05). Soit le bulletin change de système à cet endroit, soit nous avons mal lu. Même page : `crèyeû`, `vinit`, `lêu-z-ovrèdje`, `'lzî acwète` sont incertains.

## 4. Passages dont la lecture n'est pas sûre

- **05** — « Tavlê pâ ahâyan qui n' donreut rin d' bon tins âs manants. » La phrase ne se laisse pas lire ; `Tavlê` est probablement mal lu.
- **06** — « i alît so l' pote là qui lès prîzonîrs wêtît leû dièrin.ne heure » : `pote` ou `pôte` (la porte) ?
- **03** — « on n'èlz' avît mây vèyou rim'ni » contre **13** « on 'lzès libèra » et « èlzès sûvît ». Trois graphies du même pronom.
- **09** — « lès deûs k'péres » : compères ?
- **10** — « Leû moussemints djouwa » : singulier ou pluriel ?

## 5. Typographie

- **07** — guillemets emboîtés : `« Dimin, vos d'vez-t-èsse sitronlé avou l' « hart » come l'a dit… »`. Il faudrait des guillemets intérieurs d'un autre dessin, ou aucun.
- **01** — `l'loume` : espace manquante après l'élision (`l' loume`), partout ailleurs l'élision est suivie d'une espace.
- **10** — « ine epèye bin tchèrpèye, I s' ènn' alît » : virgule suivie d'une majuscule, c'est sans doute un point.
- **03** — `d' leû tchèsse !… ` : point d'exclamation suivi de points de suspension, à confirmer.
- Les apostrophes sont toutes saisies en apostrophe droite `'`. Faut-il l'apostrophe courbe `’` ?

## 6. Note 2 incomplète

> « Pindârds fotches : fourches patibulaires, gibet à plusieurs potences **que les seigneurs des lieux.** »

La phrase s'arrête net : il manque la fin dans notre saisie (… *avaient le droit d'élever* ?). Et le titre de la page 05, « Lès pindârds fotches », reprend l'ordre des mots de la note — à vérifier.

## 7. Le prénom

Le bulletin imprime « Henry GRANDRY » en tête d'article et « Henri GRANDRY » sous la colonne wallonne. Nous avons retenu **Henri**, confirmé par l'intéressé. Le colophon le mentionne ; lui demander s'il veut qu'on garde cette mention ou qu'on la retire.
