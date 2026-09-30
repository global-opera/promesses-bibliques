# Le générateur des deux applications

Les deux applications — française et portugaise — sortent d'ici. C'est ce qui
garantit qu'elles restent identiques : même balisage, même feuille de style,
même script. Seules changent la langue et la version biblique.

## Lancer

```
python faire_promesses.py
```

Il écrit `promesses-bibliques/index.html` et `promessas-biblicas/index.html`,
les deux dépôts étant supposés côte à côte dans `C:\Users\...\Depots`.

## Les fichiers

| Fichier | Rôle |
|---|---|
| `modele_promesses.json` | Le modèle figé : 7 sections, 35 thèmes, 113 références. **La source de vérité.** |
| `promesses_data.py` | Lecture des deux bibles libres et résolution d'une référence en texte |
| `faire_promesses.py` | Le gabarit HTML/CSS/JS et les deux jeux de mots |
| `modele.py` | A servi une seule fois, à extraire le modèle de l'ancienne page |

## Les deux bibles, toutes deux libres

- français : `bible-chantee/bibles/fr_bible_segond1910.json` — Louis Segond 1910, domaine public
- portugais : `Promesses Vitamin (B)iblique/pt/bible/BLIVRE.json` — Bíblia Livre, CC BY 3.0 BR

## Ajouter un verset

Ajoutez sa référence dans `modele_promesses.json`, au thème voulu, puis relancez.
Le texte est cherché automatiquement dans les deux bibles, dans les deux langues.
Si une référence est introuvable, le script s'arrête et le dit : il ne publie
jamais une page incomplète.

## Un piège, déjà rencontré

`modele.py` lisait le modèle **dans** la page française, que le générateur
écrase. La première écriture détruisait donc la source. D'où le modèle figé
en JSON : le générateur ne dépend plus de ce qu'il produit.
