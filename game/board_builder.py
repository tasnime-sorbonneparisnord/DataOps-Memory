
import random

from game.levels import LevelConfig
from models.board import Board
from models.card_effect import CoffeeCard, CriticalCard


def build_board(pairs: list, level: LevelConfig, rng: random.Random = None) -> Board:
    """Creates the shuffled board of a level from the drawn incident pairs.

    Kept outside Board so that the model does not depend on the level
    configuration (Board only manages a collection of cards).
    """
    if len(pairs) != level.incident_count:
        raise ValueError(
            f"Level expects {level.incident_count} pairs, got {len(pairs)}."
        )

    board = Board(level.rows, level.columns)

    for card in _pair_cards(pairs) + _special_cards(level):
        board.add_card(card)

    board.shuffle(rng)
    return board


def _pair_cards(pairs: list) -> list:
    return [card for pair in pairs for card in pair.get_cards()]


def _special_cards(level: LevelConfig) -> list:
    coffees = [
        CoffeeCard(f"COFFEE-{number}", level.effect_seconds)
        for number in range(1, level.coffee_count + 1)
    ]
    criticals = [
        CriticalCard(f"CRITICAL-{number}", level.effect_seconds)
        for number in range(1, level.critical_count + 1)
    ]
    return coffees + criticals
