# Étape 2 — Logique métier et gestion des données

## 1. Présentation

Cette étape consiste à développer la logique métier du jeu DataOps Memory indépendamment de son interface graphique.

L'objectif est de séparer les règles du jeu de leur représentation visuelle. La logique peut ainsi être utilisée aussi bien par l'interface Pygame que par la version console (`console_demo.py`).

Les principales responsabilités sont :

- Gérer les règles de sélection et de comparaison des cartes.
- Gérer les états du jeu et les conditions de victoire ou de défaite.
- Gérer le chronomètre et les effets des cartes spéciales.
- Construire les plateaux selon le niveau choisi.
- Charger et valider les données des incidents.
- Enregistrer et comparer les meilleurs scores.

## 2. Utilisation de la logique par l'interface

L'interface Pygame ne doit pas réimplémenter les règles métier. Elle appelle les méthodes de `MemoryGame` et affiche les informations retournées.

Exemple d'initialisation :

```python
from pathlib import Path
from game import MemoryGame, Difficulty, SelectionOutcome
from storage import IncidentLibrary, ScoreRepository

library = IncidentLibrary.from_json(Path("data/incidents.json"))
scores = ScoreRepository(Path("data/best_scores.json"))

game = MemoryGame(library)

game.start(Difficulty.EASY)
```

### 2.1 Principales interactions

| Besoin de l'interface | Appel ou propriété |
|---|---|
| Mise à jour à chaque image de la boucle | `game.update(dt)` |
| Sélection d'une carte | `game.select_card(index)` |
| Résolution d'une mauvaise combinaison après le délai d'affichage | `game.resolve_mismatch()` |
| Récupération des cartes du plateau | `game.board.get_cards()` |
| Affichage du contenu d'une carte | `card.label`, `card.icon`, `card.state` |
| Dimensions de la grille | `game.level.rows`, `game.level.columns` |
| Informations du HUD | `game.remaining_time`, `game.attempts`, `game.resolved_count` |
| Nombre d'incidents à résoudre | `game.level.incident_count` |
| Explication après une bonne combinaison | `game.last_explanation` |
| Vérification de la fin de partie | `game.is_over()` |
| Vérification de la victoire ou de la défaite | `game.is_won()`, `game.is_lost()` |
| Récupération du résultat | `game.result()` |
| Enregistrement d'un résultat | `scores.submit(game.result())` |
| Consultation du meilleur score | `scores.get_best(Difficulty.EASY)` |
| Recommencer une partie | `game.restart()` |

### 2.2 Résultats de sélection

La méthode `select_card(index)` retourne une valeur de l'énumération `SelectionOutcome` :

| Valeur | Signification |
|---|---|
| `REJECTED` | Sélection refusée, aucun changement dans le jeu |
| `FIRST_CARD` | Première carte d'une comparaison sélectionnée |
| `MATCH` | Une carte Incident et sa Solution correspondante ont été associées |
| `MISMATCH` | Les deux cartes sélectionnées ne correspondent pas |
| `SPECIAL_ACTIVATED` | Une carte spéciale a été activée |

Une position de carte inexistante provoque une exception `IndexError`.

La conversion des coordonnées de la souris en position de carte est de la responsabilité de l'interface graphique. Un clic en dehors de la grille ne doit donc pas appeler `select_card()`.

La version console du jeu, disponible dans `console_demo.py`, montre également comment utiliser la logique métier sans interface graphique.

## 3. Règles métier

### 3.1 Sélection et comparaison

- Une tentative correspond à la comparaison de deux cartes Incident ou Solution.
- Une sélection refusée ne modifie pas le jeu.
- La première carte sélectionnée reste visible en attendant la deuxième sélection.
- Si les deux cartes forment une paire valide, elles passent à l'état `MATCHED`.
- Si elles ne correspondent pas, elles restent temporairement visibles, puis sont recachées par `resolve_mismatch()`.

### 3.2 Cartes spéciales

Les cartes spéciales possèdent un comportement différent des cartes Incident et Solution.

- Une carte spéciale s'active immédiatement lorsqu'elle est retournée grâce à la méthode polymorphique `activate()`.
- Une carte Coffee ajoute du temps au chronomètre.
- Une carte Critical retire du temps au chronomètre.
- Après activation, la carte spéciale passe à l'état `REMOVED`.
- Une carte spéciale ne compte pas comme une tentative.
- Si une carte spéciale est sélectionnée alors qu'une carte Incident ou Solution est déjà visible, cette dernière est recachée sans pénalité.

Les effets temporels sont représentés par la classe `CardEffect`. Les cartes spéciales utilisent cette classe pour décrire la variation du temps.

### 3.3 État du jeu pendant une comparaison

Lorsque le jeu est dans l'état `GameState.COMPARING`, les nouvelles sélections sont refusées jusqu'à la résolution de la comparaison en cours.

Le chronomètre continue néanmoins de fonctionner pendant cette période.

### 3.4 Chronomètre

Le chronomètre respecte les règles suivantes :

- Le temps restant ne peut jamais être inférieur à zéro.
- Les effets positifs et négatifs des cartes spéciales modifient le temps restant.
- Une carte Critical peut provoquer une défaite si le temps atteint zéro.
- Le chronomètre s'arrête lorsque la partie est terminée.

### 3.5 Conditions de victoire et de défaite

La victoire est obtenue lorsque toutes les paires Incident-Solution ont été trouvées.

Les cartes spéciales ne sont pas prises en compte dans le calcul de la progression ni dans la condition de victoire.

La défaite survient lorsque le temps est écoulé avant que tous les incidents soient résolus.

## 4. Gestion des scores

Le meilleur score est déterminé selon deux critères :

1. Le temps restant le plus élevé.
2. En cas d'égalité du temps restant, le nombre de tentatives le plus faible.

Seules les parties gagnées peuvent être enregistrées comme meilleurs scores.

La règle de comparaison est centralisée dans `GameResult.is_better_than()`. Cela évite de dupliquer la même logique dans plusieurs parties du programme.

La classe `ScoreRepository` est responsable de la consultation et de l'enregistrement des meilleurs scores.

## 5. Organisation des modules

### 5.1 Package `game/`

Ce package regroupe les règles et le déroulement de la partie.

| Module | Responsabilité |
|---|---|
| `memory_game.py` | Coordination de la partie, sélection, comparaison et conditions de fin |
| `countdown_timer.py` | Gestion du temps restant et des variations temporelles |
| `levels.py` | Configuration des niveaux de difficulté |
| `enums.py` | Énumérations utilisées par la logique métier |
| `game_result.py` | Représentation d'un résultat et comparaison des scores |
| `board_builder.py` | Construction du plateau à partir de la configuration du niveau |

La construction du plateau est réalisée par la fonction `build_board()` dans `game/board_builder.py`.

Cette responsabilité n'est pas placée dans `Board`, afin que le modèle du plateau reste indépendant de `LevelConfig`.

### 5.2 Package `models/`

Ce package contient les objets métier fondamentaux du jeu.

| Classe ou module | Responsabilité |
|---|---|
| `Card` | Classe abstraite définissant le comportement commun des cartes |
| `CardState` | États possibles d'une carte |
| `PairCard` | Classe abstraite commune aux cartes Incident et Solution |
| `IncidentCard` | Représentation d'une carte Incident |
| `SolutionCard` | Représentation d'une carte Solution |
| `CardEffect` | Description d'un effet temporel |
| `SpecialCard` | Classe de base des cartes spéciales |
| `CoffeeCard` | Carte spéciale qui ajoute du temps |
| `CriticalCard` | Carte spéciale qui retire du temps |
| `Board` | Gestion des cartes présentes sur le plateau |
| `IncidentPair` | Association entre une carte Incident et une carte Solution |

Les états d'une carte sont définis dans `CardState` :

- `HIDDEN` : carte cachée.
- `REVEALED` : carte retournée et visible.
- `MATCHED` : carte appartenant à une paire trouvée.
- `REMOVED` : carte retirée du plateau.

Les effets sont définis dans `models/effect.py`. Les cartes spéciales sont définies dans `models/special_card.py`.

### 5.3 Package `storage/`

Ce package est responsable du chargement et de la persistance des données.

| Classe | Responsabilité |
|---|---|
| `IncidentLibrary` | Chargement, validation et sélection des incidents depuis les fichiers JSON |
| `IncidentEntry` | Représentation d'une entrée de contenu décrivant un incident et sa solution |
| `ScoreRepository` | Gestion des meilleurs scores |
| `PlayerProfile` | Gestion du profil du joueur |
| `GameSettings` | Gestion des préférences de l'application |

Il est important de distinguer `IncidentEntry` et `IncidentPair` :

- `IncidentEntry` représente les données d'un incident dans le package `storage/`.
- `IncidentPair` représente l'association entre deux objets carte dans le package `models/`.

Cette distinction évite de mélanger la représentation des données et les objets utilisés pendant la partie.

## 6. Principes de conception appliqués

La conception repose sur plusieurs principes de programmation orientée objet et de Clean Code.

### 6.1 Séparation des responsabilités

Chaque package possède un rôle précis :

- `models/` représente les objets métier.
- `game/` applique les règles et coordonne le déroulement de la partie.
- `storage/` gère les données et leur persistance.
- `ui/` assure l'affichage et les interactions avec le joueur.

Cette organisation permet de faire évoluer l'interface sans modifier les règles du jeu.

### 6.2 Encapsulation

Les objets exposent des méthodes et propriétés pour gérer leurs données et leurs comportements.

Par exemple, le chronomètre est géré par `CountdownTimer`, plutôt que par plusieurs composants de l'interface.

### 6.3 Abstraction et polymorphisme

La classe abstraite `Card` définit un comportement commun à toutes les cartes.

La méthode `activate()` permet aux différentes catégories de cartes de fournir leur propre comportement :

- Les cartes Incident et Solution ne modifient pas le chronomètre.
- Les cartes spéciales appliquent un effet temporel.

### 6.4 DRY

Les règles communes sont centralisées pour éviter leur duplication.

Par exemple, la comparaison des meilleurs scores est définie dans `GameResult.is_better_than()` et les paramètres des niveaux sont regroupés dans `LEVELS`.

## 7. Tests

Les tests automatisés utilisent Pytest.

Ils couvrent notamment :

- Les modèles et les états des cartes.
- Le fonctionnement du plateau.
- Les règles de sélection et de comparaison.
- Les effets des cartes spéciales.
- Le chronomètre et les niveaux de difficulté.
- Les conditions de victoire et de défaite.
- La comparaison et la persistance des scores.
- Le chargement des incidents.
- Les profils et les paramètres du joueur.
- Les composants de l'interface graphique.

Pour lancer les tests depuis la racine du projet :

```bash
python -m pytest -v
```

Les tests permettent de vérifier les comportements importants et de limiter les régressions lors des évolutions du projet.

---

**Conclusion**

La séparation entre les modèles, la logique métier, le stockage et l'interface permet de maintenir une application modulaire et évolutive.

La logique du jeu peut être testée et utilisée indépendamment de Pygame, notamment grâce à la version console `console_demo.py`.