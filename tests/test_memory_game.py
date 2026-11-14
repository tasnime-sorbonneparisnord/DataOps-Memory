
import pytest

from game.enums import Difficulty, GameState, SelectionOutcome
from game.memory_game import GameNotStartedError, MemoryGame
from models.card import CardState
from tests.conftest import (
    matching_indexes,
    mismatching_indexes,
    pair_ids,
    special_index,
)


# START

@pytest.mark.parametrize("difficulty, cards, specials", [
    (Difficulty.EASY, 8, 0),
    (Difficulty.MEDIUM, 18, 2),
    (Difficulty.HARD, 28, 4),
])
def test_start_builds_board_of_level(make_game, difficulty, cards, specials):
    game = make_game(difficulty)

    assert len(game.board.get_cards()) == cards
    assert len(game.board.get_special_cards()) == specials
    assert game.state == GameState.PLAYING
    assert game.attempts == 0


def test_all_cards_hidden_at_start(make_game):
    game = make_game()

    assert all(card.state == CardState.HIDDEN for card in game.board.get_cards())


def test_each_incident_has_exactly_one_solution(make_game):
    game = make_game(Difficulty.HARD)

    for pair_id in pair_ids(game):
        roles = sorted(c.get_pair_role() for c in game.board.get_pair_cards()
                       if c.pair_id == pair_id)
        assert roles == ["incident", "solution"]


def test_same_seed_gives_same_board(make_game):
    first = [c.card_id for c in make_game(seed=7).board.get_cards()]
    second = [c.card_id for c in make_game(seed=7).board.get_cards()]

    assert first == second


def test_playing_before_start_raises(library):
    game = MemoryGame(library)

    with pytest.raises(GameNotStartedError):
        game.select_card(0)


# MATCHING

def test_matching_pair_is_resolved(make_game):
    game = make_game()
    incident, solution = matching_indexes(game, pair_ids(game)[0])

    assert game.select_card(incident) == SelectionOutcome.FIRST_CARD
    assert game.select_card(solution) == SelectionOutcome.MATCH

    assert game.board.get_card_at(incident).is_matched()
    assert game.board.get_card_at(solution).is_matched()
    assert game.resolved_count == 1
    assert game.last_explanation.startswith("Explanation")


def test_solution_then_incident_also_matches(make_game):
    game = make_game()
    incident, solution = matching_indexes(game, pair_ids(game)[0])

    game.select_card(solution)

    assert game.select_card(incident) == SelectionOutcome.MATCH


def test_mismatch_waits_then_hides_cards(make_game):
    game = make_game()
    first, second = mismatching_indexes(game)

    game.select_card(first)
    assert game.select_card(second) == SelectionOutcome.MISMATCH
    assert game.state == GameState.COMPARING

    game.resolve_mismatch()

    assert game.state == GameState.PLAYING
    assert game.board.get_card_at(first).state == CardState.HIDDEN
    assert game.board.get_card_at(second).state == CardState.HIDDEN


def test_two_incidents_do_not_match(make_game):
    game = make_game()
    first_id, second_id = pair_ids(game)[:2]
    first = matching_indexes(game, first_id)[0]
    second = matching_indexes(game, second_id)[0]

    game.select_card(first)

    assert game.select_card(second) == SelectionOutcome.MISMATCH


# ATTEMPTS

def test_each_comparison_counts_one_attempt(make_game):
    game = make_game()
    first, second = mismatching_indexes(game)
    incident, solution = matching_indexes(game, pair_ids(game)[2])

    game.select_card(first)
    game.select_card(second)
    game.resolve_mismatch()
    game.select_card(incident)
    game.select_card(solution)

    assert game.attempts == 2


def test_first_card_alone_is_not_an_attempt(make_game):
    game = make_game()

    game.select_card(0)

    assert game.attempts == 0


# FORBIDDEN SELECTIONS

def test_same_card_twice_is_rejected(make_game):
    game = make_game()

    game.select_card(0)

    assert game.select_card(0) == SelectionOutcome.REJECTED
    assert game.attempts == 0


def test_resolved_card_cannot_be_selected(make_game):
    game = make_game()
    incident, solution = matching_indexes(game, pair_ids(game)[0])
    game.select_card(incident)
    game.select_card(solution)

    assert game.select_card(incident) == SelectionOutcome.REJECTED


def test_third_card_rejected_during_comparison(make_game):
    game = make_game()
    first, second = mismatching_indexes(game)
    third = matching_indexes(game, pair_ids(game)[3])[0]
    game.select_card(first)
    game.select_card(second)

    assert game.select_card(third) == SelectionOutcome.REJECTED
    assert game.board.get_card_at(third).state == CardState.HIDDEN


def test_invalid_position_raises(make_game):
    game = make_game()

    with pytest.raises(IndexError):
        game.select_card(99)


# SPECIAL CARDS

def test_coffee_card_adds_time_and_is_removed(make_game):
    game = make_game(Difficulty.MEDIUM)
    coffee = special_index(game, positive=True)

    outcome = game.select_card(coffee)

    assert outcome == SelectionOutcome.SPECIAL_ACTIVATED
    assert game.remaining_time == 100
    assert game.board.get_card_at(coffee).is_removed()
    assert game.attempts == 0


def test_critical_card_removes_time(make_game):
    game = make_game(Difficulty.MEDIUM)

    game.select_card(special_index(game, positive=False))

    assert game.remaining_time == 80


def test_special_card_hides_pending_pair_card_without_penalty(make_game):
    game = make_game(Difficulty.MEDIUM)
    incident = matching_indexes(game, pair_ids(game)[0])[0]

    game.select_card(incident)
    game.select_card(special_index(game, positive=True))

    assert game.board.get_card_at(incident).state == CardState.HIDDEN
    assert game.attempts == 0
    assert game.state == GameState.PLAYING


def test_removed_special_card_cannot_be_selected_again(make_game):
    game = make_game(Difficulty.MEDIUM)
    coffee = special_index(game, positive=True)
    game.select_card(coffee)

    assert game.select_card(coffee) == SelectionOutcome.REJECTED
    assert game.remaining_time == 100


def test_critical_card_can_end_the_game(make_game):
    game = make_game(Difficulty.MEDIUM)
    game.update(85)

    game.select_card(special_index(game, positive=False))

    assert game.is_lost()
    assert game.remaining_time == 0


# TIME, VICTORY AND DEFEAT

def test_update_moves_countdown(make_game):
    game = make_game()

    game.update(15)

    assert game.remaining_time == 45


def test_game_lost_when_time_runs_out(make_game):
    game = make_game()

    game.update(60)

    assert game.is_lost()
    assert game.result().won is False


def test_game_won_when_all_incidents_resolved(make_game):
    game = make_game()

    for pair_id in pair_ids(game):
        incident, solution = matching_indexes(game, pair_id)
        game.select_card(incident)
        game.select_card(solution)

    assert game.is_won()
    assert game.result().attempts == 4
    assert game.result().time_left == 60


def test_no_action_after_end(make_game):
    game = make_game()
    game.update(60)

    assert game.select_card(0) == SelectionOutcome.REJECTED

    game.update(10)
    assert game.remaining_time == 0


def test_result_before_end_raises(make_game):
    game = make_game()

    with pytest.raises(RuntimeError):
        game.result()


def test_restart_gives_fresh_game(make_game):
    game = make_game()
    game.select_card(0)
    game.update(30)

    game.restart()

    assert game.attempts == 0
    assert game.remaining_time == 60
    assert all(c.state == CardState.HIDDEN for c in game.board.get_cards())


# END-TO-END

def test_full_hard_game_with_specials_ends_in_victory(make_game):
    """Plays a whole game the way a player would, with a fixed seed."""
    game = make_game(Difficulty.HARD, seed=2026)

    game.select_card(special_index(game, positive=True))
    game.update(30)
    first, second = mismatching_indexes(game)
    game.select_card(first)
    game.select_card(second)
    game.resolve_mismatch()

    for pair_id in pair_ids(game):
        incident, solution = matching_indexes(game, pair_id)
        game.select_card(incident)
        game.select_card(solution)
        game.update(1)

    result = game.result()
    assert result.won
    assert result.attempts == 13
    assert result.time_left == 120 + 10 - 30 - 11
