
import pytest

from models.card import (
    CardState,
    IncidentCard,
    SolutionCard,
)
from models.card_effect import (
    CardEffect,
    CoffeeCard,
    CriticalCard,
)
from models.incident_pair import IncidentPair
from models.board import Board


# CARD TESTS

def test_incident_card_creation():
    card = IncidentCard(
        "C1", "INC001", "Server down", "Server unavailable"
    )

    assert card.card_id == "C1"
    assert card.pair_id == "INC001"
    assert card.state == CardState.HIDDEN


def test_card_reveal_and_hide():
    card = IncidentCard("C1", "INC001", "Server down", "Description")

    card.reveal()
    assert card.is_revealed()

    card.hide()
    assert card.state == CardState.HIDDEN


def test_matched_card_cannot_be_hidden():
    card = IncidentCard("C1", "INC001", "Server down", "Description")

    card.mark_as_matched()
    card.hide()

    assert card.is_matched()


def test_cards_match():
    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    solution = SolutionCard("C2", "INC001", "Restart server", "Description")

    assert incident.matches(solution)


def test_cards_do_not_match_with_different_ids():
    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    solution = SolutionCard("C2", "INC002", "Restart server", "Description")

    assert not incident.matches(solution)


# CARD EFFECT TESTS

def test_coffee_adds_ten_seconds():
    coffee = CoffeeCard("SP001")

    assert coffee.effect.seconds_delta == 10


def test_critical_removes_ten_seconds():
    critical = CriticalCard("SP002")

    assert critical.effect.seconds_delta == -10


def test_card_effect_rejects_zero():
    with pytest.raises(ValueError):
        CardEffect(0)


# INCIDENT PAIR TESTS

def test_incident_pair_creation():
    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    solution = SolutionCard("C2", "INC001", "Restart server", "Description")

    pair = IncidentPair(incident, solution)

    assert pair.pair_id == "INC001"
    assert not pair.is_matched()


def test_incident_pair_matching():
    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    solution = SolutionCard("C2", "INC001", "Restart server", "Description")

    pair = IncidentPair(incident, solution)
    pair.mark_as_matched()

    assert pair.is_matched()


def test_incident_pair_rejects_different_ids():
    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    solution = SolutionCard("C2", "INC002", "Restart server", "Description")

    with pytest.raises(ValueError):
        IncidentPair(incident, solution)


# BOARD TESTS

def test_board_creation():
    board = Board(2, 4)

    assert board.rows == 2
    assert board.columns == 4
    assert board.capacity == 8


def test_board_add_cards():
    board = Board(2, 2)
    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    coffee = CoffeeCard("SP001")

    board.add_card(incident)
    board.add_card(coffee)

    assert len(board.get_cards()) == 2
    assert len(board.get_pair_cards()) == 1
    assert len(board.get_special_cards()) == 1


def test_board_rejects_duplicate_ids():
    board = Board(2, 2)

    first = IncidentCard("C1", "INC001", "Server down", "Description")
    second = SolutionCard("C1", "INC001", "Restart server", "Description")

    board.add_card(first)

    with pytest.raises(ValueError):
        board.add_card(second)


def test_board_rejects_cards_when_full():
    board = Board(1, 1)
    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    solution = SolutionCard("C2", "INC001", "Restart server", "Description")

    board.add_card(incident)

    with pytest.raises(ValueError):
        board.add_card(solution)


def test_board_completion():
    board = Board(1, 2)

    incident = IncidentCard("C1", "INC001", "Server down", "Description")
    solution = SolutionCard("C2", "INC001", "Restart server", "Description")

    board.add_card(incident)
    board.add_card(solution)

    assert not board.is_complete()

    incident.mark_as_matched()
    solution.mark_as_matched()

    assert board.is_complete()