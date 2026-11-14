
import random

import pytest

from game.enums import Difficulty
from game.memory_game import MemoryGame
from storage.incident_library import IncidentEntry, IncidentLibrary


def make_entries(count: int) -> list:
    return [
        IncidentEntry(
            pair_id=f"P{number:02d}",
            theme="database" if number % 2 else "network",
            incident_label=f"Incident {number}",
            solution_label=f"Solution {number}",
            explanation=f"Explanation {number}",
        )
        for number in range(1, count + 1)
    ]


@pytest.fixture
def library():
    return IncidentLibrary(make_entries(24))


@pytest.fixture
def make_game(library):
    """Creates a started game with a fixed seed (reproducible board)."""

    def _make(difficulty=Difficulty.EASY, seed=42):
        game = MemoryGame(library, random.Random(seed))
        game.start(difficulty)
        return game

    return _make


# ----------------------------------------------------------------------
# Helpers to find card positions on a started board
# ----------------------------------------------------------------------

def index_of(game, predicate) -> int:
    for index, card in enumerate(game.board.get_cards()):
        if predicate(card):
            return index
    raise LookupError("No card matches the predicate.")


def matching_indexes(game, pair_id: str) -> tuple:
    incident = index_of(game, lambda c: not c.is_special() and c.pair_id == pair_id
                        and c.get_pair_role() == "incident")
    solution = index_of(game, lambda c: not c.is_special() and c.pair_id == pair_id
                        and c.get_pair_role() == "solution")
    return incident, solution


def pair_ids(game) -> list:
    return sorted({card.pair_id for card in game.board.get_pair_cards()})


def mismatching_indexes(game) -> tuple:
    first_id, second_id = pair_ids(game)[:2]
    return matching_indexes(game, first_id)[0], matching_indexes(game, second_id)[1]


def special_index(game, positive: bool) -> int:
    return index_of(
        game,
        lambda c: c.is_special() and (c.activate().seconds_delta > 0) == positive
        and c.is_selectable(),
    )
