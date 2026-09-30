# Le générateur des deux applications

**La page française est le modèle.** C'est elle qui fixe la mise en page, la
feuille de style et le script. La page portugaise en est la traduction exacte :
mêmes sections, mêmes thèmes, mêmes références, même code. Seuls changent les
mots et la version biblique.

## Lancer

```
python jumeler.py
```

Il écrit `promesses-bibliques/index.html` et `promessas-biblicas/index.html`,
les deux dépôts étant supposés côte à côte dans `Depots`.

## Les fichiers

| Fichier | Rôle |
|---|---|
| `fr_original.html` | **Le modèle.** La page française telle qu'elle était avant la mise en version libre. Toute évolution de la mise en page se fait ici. |
| `promesses_data.py` | Lecture des deux bibles libres, résolution d'une référence en texte |
| `jumeler.py` | Les substitutions : textes bibliques, titres, sous-titres, mots d'interface |

## Les deux bibles, toutes deux libres

- français : `bible-chantee/bibles/fr_bible_segond1910.json` — Louis Segond 1910, domaine public
- portugais : `Promesses Vitamin (B)iblique/pt/bible/BLIVRE.json` — Bíblia Livre, CC BY 3.0 BR

Les 113 références sont résolues automatiquement dans les deux langues. Si l'une
d'elles est introuvable, le script s'arrête et le dit : il ne publie jamais une
page incomplète.

## Ce qui vient de moi, et qu'il faut relire

Les **35 sous-titres portugais** (« Vida eterna pela fé », « Abrigo na
tempestade »…) sont des traductions faites par Claude. Les titres de sections et
les noms de thèmes, eux, sont ceux de Stéphane, repris tels quels de la version
portugaise précédente.

## Une erreur à ne pas refaire

Un premier essai avait reconstruit les **deux** pages depuis un gabarit neuf.
La parité était acquise, mais au prix de la mise en page française, qui
convenait. La consigne était : reprendre exactement la française, et la
traduire. D'où ce générateur-ci, qui part du fichier original et n'en change
que ce qui doit changer.
