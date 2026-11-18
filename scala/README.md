# Extension Scala : contrôle qualité des incidents

Petit programme Scala **indépendant du jeu** qui vérifie le contenu des fichiers
`data/incidents.json` (français) et `data/incidents_en.json` (anglais) avant qu'il
n'arrive dans le jeu. C'est un vrai réflexe DataOps : contrôler la qualité des
données avant de les utiliser.

## Ce qui est vérifié

| Contrôle | Pourquoi |
|---|---|
| JSON bien formé, champs obligatoires présents et non vides | sinon le jeu refuse de démarrer |
| Pas de `pair_id` en double | deux paires ne doivent pas se confondre |
| Au moins 12 paires par langue | le niveau Difficile en tire 12 |
| Textes de 32 caractères maximum | au-delà, le texte ne tient plus bien sur une carte |
| Toutes les icônes existent dans `assets/icons/` | sinon la carte affiche une icône par défaut |
| Mêmes paires en français et en anglais | aucune paire ne doit manquer dans une langue |
| Même thème et mêmes icônes dans les deux langues | une traduction ne change que le texte |

Le programme affiche un rapport (nombre de paires, paires par thème, problèmes)
et se termine avec le code `1` s'il trouve un problème : il peut donc bloquer
GitHub Actions avant qu'un fichier abîmé n'arrive dans `main`.

## Installation et lancement

Il faut [Scala CLI](https://scala-cli.virtuslab.org) (il télécharge Scala tout seul) :

```bash
brew install Virtuslab/scala-cli/scala-cli     # macOS
```

Depuis la racine du projet :

```bash
# contrôle des fichiers d'incidents
scala-cli run scala --main-class dataops.quality.checkIncidents

# tests de l'extension
scala-cli run scala --main-class dataops.quality.runQualityTests
```

## Organisation

| Fichier | Rôle |
|---|---|
| `src/FlatJson.scala` | lecture du JSON (liste d'objets dont les valeurs sont du texte), sans bibliothèque ; renvoie `Either` |
| `src/Incident.scala` | `case class Incident` immuable + construction validée depuis le JSON |
| `src/ContentChecks.scala` | **les règles, toutes en fonctions pures** |
| `src/Report.scala` | `case class Report` : chiffres, problèmes et affichage |
| `src/Main.scala` | lecture des fichiers et affichage : les effets de bord sont regroupés ici |
| `tests/ContentChecksTest.scala` | 10 tests avec `assert` |

## Notions du chapitre 5 appliquées

- **Immutabilité** : `val` partout, `case class` immuables, collections immuables
  (`List`, `Set`, `Map`). La seule variable (`var position`) est enfermée dans le
  lecteur JSON.
- **Fonctions pures** : toutes les règles de `ContentChecks` donnent toujours le même
  résultat pour les mêmes entrées, sans lire ni écrire de fichier.
- **Effets de bord au bord du programme** : seules les fonctions de `Main.scala`
  lisent les fichiers et affichent le résultat.
- **Transformations de collections** : `map`, `filter`, `flatMap`, `collect`,
  `groupBy`, `toSet`, différences d'ensembles (`diff`, `union`, `--`).
- **Cas limites explicites** : `Option` (`get`, `lift`) pour une valeur qui peut manquer,
  `Either` pour une erreur attendue (fichier introuvable, JSON invalide, champ manquant)
  au lieu d'une exception.
- **Clean Code** : noms métier (`duplicatePairIds`, `translationGaps`), petites
  fonctions, constantes nommées (`MaxLabelLength`, `MinimumPairs`), valeurs
  intermédiaires nommées plutôt qu'un long pipeline opaque.
