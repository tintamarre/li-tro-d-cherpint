# Li trô d' chèrpint — Le trou du serpent

Livre illustré bilingue **wallon / français** d'une légende du pays d'Ourthe-Amblève : le serpent du chantoir de Xhignez, à Sprimont. Une page par paragraphe, les deux langues en regard, quatorze planches dessinées en SVG. On tourne les pages au clic.

Le contexte de la légende, les sources et les notes sont dans le colophon du livre (dernière page) — c'est ce que lit le lecteur. Ce fichier-ci ne décrit que la fabrication.

## Lancer

Aucune dépendance, aucune compilation. Le site est statique :

```sh
open index.html          # le texte est figé dans assets/livre-data.js, file:// suffit
python3 -m http.server 8000   # ou un serveur local, http://localhost:8000
```

## Structure

```
index.html               la page unique
assets/livre.css         mise en page, palette, zones de clic
assets/livre.js          feuilletage, clavier, glissement tactile, choix de langue
assets/livre-data.js     texte figé — ENGENDRÉ, ne pas éditer
texte/pages.json         la source du texte : 13 pages, 4 notes
texte/transcription.md   la transcription continue des deux colonnes du bulletin
illustrations/*.svg      14 planches — ENGENDRÉES, ne pas éditer
outils/dessin.py         bibliothèque de dessin : géométrie, trait, lavis, personnages
outils/styles.py         la direction graphique (palette, trait, densité)
outils/planches.py       les 14 compositions
outils/site.py           fige texte/pages.json dans assets/livre-data.js
```

## Reconstruire

```sh
python3 outils/planches.py   # redessine illustrations/*.svg
python3 outils/site.py       # regénère assets/livre-data.js depuis texte/pages.json
```

`texte/pages.json` est la seule source du texte : corriger là, puis relancer `site.py`.

`site.py` calcule aussi une empreinte des quatorze planches et l'ajoute en paramètre d'URL aux images. Sans elle, le navigateur continue de servir les planches qu'il a en cache après une régénération, puisque les noms de fichiers ne changent pas — et l'on croit regarder une correction qui n'est pas affichée. **Relancer `site.py` après `planches.py`**, sinon l'empreinte est périmée.

## Les illustrations

Tout est engendré par du Python qui écrit du SVG — pas d'image matricielle, pas d'emprunt. Le dessin repose sur trois filtres SVG : un déplacement par bruit fractal qui ronge les bords des lavis, un autre plus large pour les fonds, et un troisième, très léger, qui fait trembler le trait.

Les planches n'ont pas de bord franc : un masque en déplacement de bruit puis flou gaussien fait que le lavis s'arrête là où le pinceau se serait levé, et se fond dans le papier de la page. Le fondu tient sur une vingtaine de pixels : au-delà il mange le dessin. Le réglage est la constante `BORD` de `outils/dessin.py` — `(7, 2.5, 5)` est plus discret encore, `(0, 0.01, -2)` revient au bord net.

Les filtres existent en deux jeux. Ceux en `filterUnits="userSpaceOnUse"` servent partout, et **c'est nécessaire** : avec le défaut en pourcentage de la boîte englobante, un trait parfaitement vertical a une boîte de largeur nulle, donc une région de filtre nulle, et disparaît purement et simplement. Mais une région en coordonnées utilisateur est tournée et décalée avec le groupe qui la contient : à l'intérieur d'un groupe transformé — la tête du serpent — elle rogne et laisse un rectangle visible. Ces cas-là utilisent les variantes `-wcb` et `-inkb`, en unités de boîte.

Les planches s'animent discrètement : flammes de chandelle et de torche, lueurs qui respirent, yeux qui clignent — chacun à son rythme propre —, éclats de miroir, langue du serpent, cordes du gibet qui se balancent, épées qui se balancent au poing des chasseurs, fleurs au vent, reflets qui courent sur les lames, oiseaux qui s'éloignent. Le serpent mort de la dernière planche, lui, ne bouge plus : son œil est fixe. L'animation est en CSS *à l'intérieur* de chaque SVG, ce qui la conserve même quand le fichier est chargé via `<img>`, et la désactive sous `prefers-reduced-motion`.

## Une note sur les apostrophes wallonnes

Le texte wallon mêle deux usages de l'apostrophe, et les deux sont voulus.

- **Élision suivie d'une espace** — `li trô d' chèrpint`, `l' intrèye`, `s' trô`. L'apostrophe remplace la voyelle tombée et le mot suivant reste séparé. 47 occurrences.
- **Apostrophe lettre du mot** — `on pus'`, `li song'`, `tote li nut'`, `li lodjis'`. Elle note une consonne finale prononcée, à la manière du système Feller ; l'espace qui suit est une espace-mot ordinaire. Les supprimer souderait deux mots.

Le livre **ne touche donc à aucune espace**. Il resserre seulement de 0,13 cadratin le blanc après les élisions d'une ou deux lettres, en enveloppant l'apostrophe dans un `span`. Le texte reste identique au caractère près : vérifié en comparant le `textContent` rendu à `texte/pages.json` pour les treize pages.

## Droits

Quatre régimes cohabitent ; ils ne se confondent pas.

| Quoi | Régime |
|---|---|
| Le **code** (`outils/`, `assets/`, `index.html`, `impression.html`) | Licence libre **MIT** — voir `LICENSE` |
| Les **illustrations** (`illustrations/`) | Licence libre **CC BY-SA 4.0** — voir `LICENSE-ILLUSTRATIONS.md` |
| Le **texte français** de **Georges Laport** (Fraiture 1898 – Dachau 1945) | **Domaine public** depuis le 1ᵉʳ janvier 2016 |
| La **traduction wallonne** d'**Henri Grandry** (2026) | **Tous droits réservés à son auteur** |

Les deux licences libres portent sur ce que j'ai fabriqué, et sur cela seulement. Elles ne s'étendent à aucun des deux textes. La traduction wallonne appartient à Henri Grandry et ne peut être reprise, publiée ni rediffusée sans son accord.

Source du texte : *Sprimont Infos*, octobre 2026, p. 24, rubrique « Patrimoine ».

> Ce dépôt est **privé** tant que l'accord d'Henri Grandry n'a pas été obtenu pour la diffusion du texte wallon.

## Deux corrections au bulletin imprimé

Signalées ici parce qu'elles écartent la version en ligne de la page imprimée :

1. Le bulletin écrit « Henry GRANDRY » dans le chapeau et « Henri GRANDRY » sous la colonne wallonne. La graphie exacte est **Henri** ; elle a été rétablie.
2. La liste des notes imprimée intervertit les notes 3 et 4 par rapport aux appels du texte (« hart » appelle 3, « volahe » appelle 4). Elles ont été remises en regard de leur appel.
