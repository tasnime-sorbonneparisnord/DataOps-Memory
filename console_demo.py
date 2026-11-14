
"""Text version of DataOps Memory, to play the game logic without Pygame.

Usage:  python console_demo.py
"""

import time
from pathlib import Path

from game.enums import Difficulty, SelectionOutcome
from game.memory_game import MemoryGame
from models.card import Card
from storage.incident_library import IncidentLibrary, IncidentLibraryError
from storage.score_repository import ScoreRepository

DATA_DIR = Path(__file__).parent / "data"
INCIDENTS_FILE = DATA_DIR / "incidents.json"
SCORES_FILE = DATA_DIR / "best_scores.json"
CELL_WIDTH = 24
DIFFICULTY_CHOICES = {"1": Difficulty.EASY, "2": Difficulty.MEDIUM, "3": Difficulty.HARD}


def card_text(index: int, card: Card) -> str:
    if card.is_removed():
        text = ""
    elif card.is_selectable():
        text = "?"
    else:
        text = card.label
    return f"[{index:2}] {text}"[:CELL_WIDTH].ljust(CELL_WIDTH)


def show_board(game: MemoryGame):
    cards = game.board.get_cards()
    columns = game.level.columns

    for start in range(0, len(cards), columns):
        row = cards[start:start + columns]
        print(" ".join(card_text(start + i, card) for i, card in enumerate(row)))

    print(f"\nTemps : {game.remaining_time:5.1f} s | Tentatives : {game.attempts}"
          f" | Résolus : {game.resolved_count}/{game.level.incident_count}")


def ask_difficulty() -> Difficulty:
    while True:
        choice = input("Niveau ? 1 = Facile, 2 = Moyen, 3 = Difficile : ").strip()
        if choice in DIFFICULTY_CHOICES:
            return DIFFICULTY_CHOICES[choice]


def ask_position(game: MemoryGame):
    answer = input("Carte n° : ").strip()
    if not answer.isdigit() or int(answer) >= len(game.board.get_cards()):
        print("Position invalide.")
        return None
    return int(answer)


def describe(outcome: SelectionOutcome, game: MemoryGame):
    messages = {
        SelectionOutcome.REJECTED: "Carte non sélectionnable.",
        SelectionOutcome.MATCH: f"Incident résolu ! {game.last_explanation}",
        SelectionOutcome.MISMATCH: "Pas la bonne paire...",
        SelectionOutcome.SPECIAL_ACTIVATED: "Carte spéciale activée !",
    }
    if outcome in messages:
        print(messages[outcome])


def play_turns(game: MemoryGame):
    last_time = time.monotonic()

    while not game.is_over():
        print()
        show_board(game)
        position = ask_position(game)

        now = time.monotonic()
        game.update(now - last_time)
        last_time = now

        if position is None or game.is_over():
            continue

        outcome = game.select_card(position)
        describe(outcome, game)

        if outcome == SelectionOutcome.MISMATCH:
            show_board(game)
            input("Entrée pour cacher les cartes...")
            game.resolve_mismatch()


def show_end(game: MemoryGame, scores: ScoreRepository):
    result = game.result()
    print("\n=== VICTOIRE ===" if result.won else "\n=== TEMPS ÉCOULÉ ===")
    print(f"Temps restant : {result.time_left} s | Tentatives : {result.attempts}")

    if scores.submit(result):
        print("Nouveau record !")

    best = scores.get_best(result.difficulty)
    if best:
        print(f"Record du niveau : {best.time_left} s, {best.attempts} tentatives")


def main():
    try:
        library = IncidentLibrary.from_json(INCIDENTS_FILE)
    except IncidentLibraryError as error:
        print(f"Impossible de charger les incidents : {error}")
        return

    scores = ScoreRepository(SCORES_FILE)
    game = MemoryGame(library)
    game.start(ask_difficulty())

    while True:
        play_turns(game)
        show_end(game, scores)
        if input("\nRejouer ? (o/n) : ").strip().lower() != "o":
            break
        game.restart()


if __name__ == "__main__":
    main()
