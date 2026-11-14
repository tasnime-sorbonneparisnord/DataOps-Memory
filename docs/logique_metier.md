# Étape 2 — Logique métier et données (Khoubeib)

## 1. Comment l'interface (Pygame) utilise la logique

L'interface n'applique **aucune règle** : elle appelle `MemoryGame`, puis affiche ce qu'elle lit.

```python
from pathlib import Path
from game import MemoryGame, Difficulty, SelectionOutcome
from storage import IncidentLibrary, ScoreRepository

library = IncidentLibrary.from_json(Path("data/incidents.json"))
scores = ScoreRepository(Path("data/best_scores.json"))
game = MemoryGame(library)          # option : MemoryGame(library, random.Random(42))

game.start(Difficulty.EASY)         # menu : choix du niveau
```

| Besoin de l'interface | Appel |
|---|---|
| À chaque image de la boucle | `game.update(dt_en_secondes)` |
| Clic sur la carte n° `i` (0 = en haut à gauche, ligne par ligne) | `outcome = game.select_card(i)` |
| Après `SelectionOutcome.MISMATCH`, une fois le délai écoulé (~1 s) | `game.resolve_mismatch()` |
| Afficher les cartes | `game.board.get_cards()` ; pour chaque carte : `card.label`, `card.icon`, `card.state` (`HIDDEN`, `REVEALED`, `MATCHED`, `REMOVED`) |
| Taille de la grille | `game.level.rows`, `game.level.columns` |
| HUD | `game.remaining_time`, `game.attempts`, `game.resolved_count`, `game.level.incident_count` |
| Explication après une paire | `game.last_explanation` (quand `outcome == SelectionOutcome.MATCH`) |
| Fin de partie | `game.is_over()`, `game.is_won()`, `game.is_lost()`, `game.result()` |
| Record | `scores.submit(game.result())` (renvoie `True` si nouveau record), `scores.get_best(Difficulty.EASY)` |
| Rejouer | `game.restart()` |

Valeurs de `SelectionOutcome` : `REJECTED` (clic refusé, rien ne change), `FIRST_CARD`, `MATCH`, `MISMATCH`, `SPECIAL_ACTIVATED`.

Un clic hors de la grille ne doit pas appeler `select_card()` : c'est l'interface qui convertit les pixels en numéro de carte. Une position qui n'existe pas lève `IndexError`.

`console_demo.py` montre l'utilisation complète, en version texte.

## 2. Règles appliquées (cahier des charges, section 6)

- Une tentative = la comparaison de deux cartes Incident ou Solution.
- Une carte spéciale s'active dès qu'elle est retournée (`activate()`), puis elle est retirée (`REMOVED`). Elle ne compte pas comme une tentative.
- Si une carte spéciale est retournée alors qu'une carte Incident ou Solution est déjà visible, cette carte est recachée, sans pénalité.
- Pendant une comparaison (`GameState.COMPARING`), les autres clics sont refusés. Le chronomètre continue de tourner.
- Le chronomètre ne descend jamais sous 0. Il s'arrête à la fin de la partie, et une carte Critique peut faire perdre la partie.
- Victoire quand tous les incidents sont résolus : les cartes spéciales ne comptent pas.
- Meilleur score : plus de temps restant ; en cas d'égalité, moins de tentatives. Seules les parties gagnées comptent. Cette règle est écrite à un seul endroit : `GameResult.is_better_than()`.

## 3. Ajouts faits aux modèles de l'étape 1 (à valider avec Tasnime)

Les ajouts sont compatibles avec le code existant : les 16 tests d'origine passent toujours, un seul a été adapté. Ils servent à coller à la documentation de conception.

| Fichier | Ajout | Pourquoi |
|---|---|---|
| `models/card.py` | `activate()` (abstraite), `is_special()`, `is_selectable()`, `remove()`, `is_removed()`, état `CardState.REMOVED`, attribut `icon`, propriété `explanation` | Polymorphisme `activate()` de la doc ; une carte spéciale doit être retirée |
| `models/effect.py` (nouveau) | `CardEffect` déplacé ici, plus `NO_EFFECT` et `DEFAULT_EFFECT_SECONDS` | Évite un import circulaire entre `card.py` et `card_effect.py` ; `card_effect.py` continue de l'exporter |
| `models/card_effect.py` | `SpecialCard.activate()`, `is_special()` ; `CoffeeCard(id, seconds=10)` et `CriticalCard(id, seconds=10)` | Durée de l'effet venant de la configuration des niveaux, pas en dur |
| `models/board.py` | `shuffle(rng=None)`, `get_card_at(index)`, `resolved_count()` | Mélange reproductible (graine) ; l'interface travaille par position |
| `tests/test_models.py` | `test_card_effect_rejects_zero` remplacé par deux tests | Un effet à 0 est désormais `NO_EFFECT` (cartes Incident et Solution) ; une carte spéciale à 0 seconde reste refusée |

Écarts restants par rapport à la doc :
- `Board.build()` est devenu la fonction `game/board_builder.py::build_board()`, pour que le modèle ne dépende pas de `LevelConfig`.
- La paire « de contenu » s'appelle `IncidentEntry` (dans `storage/`), parce que `IncidentPair` regroupe déjà deux cartes dans le code de Tasnime.
- Les états s'appellent `REVEALED` et `MATCHED` (dans la doc : `VISIBLE` et `RESOLVED`).

Il faudra mettre à jour l'UML en conséquence.
