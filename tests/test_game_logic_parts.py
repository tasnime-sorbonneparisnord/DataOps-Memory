
import json
import random

import pytest

from game.countdown_timer import CountdownTimer
from game.enums import Difficulty
from game.game_result import GameResult
from game.levels import LEVELS, LevelConfig, get_level
from storage.incident_library import IncidentLibrary, IncidentLibraryError
from storage.score_repository import ScoreRepository
from tests.conftest import make_entries


# LEVEL CONFIG

@pytest.mark.parametrize("difficulty", list(Difficulty))
def test_every_level_fills_its_grid(difficulty):
    level = get_level(difficulty)

    assert level.card_count == level.rows * level.columns


def test_level_rejects_wrong_grid():
    with pytest.raises(ValueError):
        LevelConfig(4, 0, 0, rows=3, columns=3, time_limit=60, effect_seconds=10)


def test_every_difficulty_has_a_level():
    assert set(LEVELS) == set(Difficulty)


# COUNTDOWN TIMER

def test_timer_decreases():
    timer = CountdownTimer(60)

    timer.tick(2.5)

    assert timer.remaining == 57.5


def test_timer_never_goes_below_zero():
    timer = CountdownTimer(5)

    timer.tick(10)
    timer.add(-10)

    assert timer.remaining == 0
    assert timer.is_expired()


def test_timer_bonus_and_penalty():
    timer = CountdownTimer(60)

    timer.add(10)
    timer.add(-5)

    assert timer.remaining == 65


def test_stopped_timer_is_frozen():
    timer = CountdownTimer(60)
    timer.stop()

    timer.tick(10)
    timer.add(10)

    assert timer.remaining == 60


def test_timer_rejects_negative_elapsed_time():
    with pytest.raises(ValueError):
        CountdownTimer(60).tick(-1)


# GAME RESULT

def test_more_time_left_is_better():
    best = GameResult(Difficulty.EASY, time_left=30, attempts=10)
    other = GameResult(Difficulty.EASY, time_left=20, attempts=4)

    assert best.is_better_than(other)
    assert not other.is_better_than(best)


def test_on_tie_fewer_attempts_is_better():
    best = GameResult(Difficulty.EASY, time_left=30, attempts=5)
    other = GameResult(Difficulty.EASY, time_left=30, attempts=8)

    assert best.is_better_than(other)


def test_any_win_beats_no_record():
    assert GameResult(Difficulty.EASY, 1, 50).is_better_than(None)


def test_lost_game_is_never_better():
    lost = GameResult(Difficulty.EASY, 0, 3, won=False)

    assert not lost.is_better_than(None)


# INCIDENT LIBRARY

def test_draw_returns_different_pairs():
    library = IncidentLibrary(make_entries(24))

    pairs = library.draw(12, random.Random(1))

    assert len({pair.pair_id for pair in pairs}) == 12


def test_draw_too_many_pairs_raises():
    library = IncidentLibrary(make_entries(3))

    with pytest.raises(IncidentLibraryError):
        library.draw(4)


def test_each_draw_creates_new_hidden_cards():
    library = IncidentLibrary(make_entries(1))
    first = library.draw(1)[0]
    first.mark_as_matched()

    second = library.draw(1)[0]

    assert not second.is_matched()


def test_duplicate_pair_ids_rejected():
    entries = make_entries(2) + make_entries(1)

    with pytest.raises(IncidentLibraryError):
        IncidentLibrary(entries)


def test_missing_file_gives_clear_error(tmp_path):
    with pytest.raises(IncidentLibraryError, match="not found"):
        IncidentLibrary.from_json(tmp_path / "absent.json")


def test_malformed_json_gives_clear_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{ not json", encoding="utf-8")

    with pytest.raises(IncidentLibraryError, match="Invalid JSON"):
        IncidentLibrary.from_json(path)


def test_pair_with_missing_field_rejected(tmp_path):
    path = tmp_path / "incomplete.json"
    path.write_text(json.dumps([{"pair_id": "X", "theme": "db"}]), encoding="utf-8")

    with pytest.raises(IncidentLibraryError, match="missing"):
        IncidentLibrary.from_json(path)


def test_real_content_file_is_valid():
    library = IncidentLibrary.from_json("data/incidents.json")

    assert len(library) >= 24
    assert library.themes == {"database", "network", "cloud", "pipeline"}


# SCORE REPOSITORY

def test_first_win_becomes_record(tmp_path):
    scores = ScoreRepository(tmp_path / "scores.json")
    result = GameResult(Difficulty.EASY, 30, 6)

    assert scores.submit(result)
    assert scores.get_best(Difficulty.EASY) == result


def test_better_result_replaces_record(tmp_path):
    scores = ScoreRepository(tmp_path / "scores.json")
    scores.submit(GameResult(Difficulty.EASY, 30, 6))

    assert scores.submit(GameResult(Difficulty.EASY, 40, 9))
    assert scores.get_best(Difficulty.EASY).time_left == 40


def test_worse_result_is_ignored(tmp_path):
    scores = ScoreRepository(tmp_path / "scores.json")
    scores.submit(GameResult(Difficulty.EASY, 30, 6))

    assert not scores.submit(GameResult(Difficulty.EASY, 10, 6))
    assert scores.get_best(Difficulty.EASY).time_left == 30


def test_each_level_has_its_own_record(tmp_path):
    scores = ScoreRepository(tmp_path / "scores.json")
    scores.submit(GameResult(Difficulty.EASY, 30, 6))

    assert scores.get_best(Difficulty.HARD) is None


def test_lost_game_never_saved(tmp_path):
    scores = ScoreRepository(tmp_path / "scores.json")

    assert not scores.submit(GameResult(Difficulty.EASY, 0, 6, won=False))


def test_records_survive_restart(tmp_path):
    path = tmp_path / "scores.json"
    ScoreRepository(path).submit(GameResult(Difficulty.MEDIUM, 25, 12))

    reloaded = ScoreRepository(path)

    assert reloaded.get_best(Difficulty.MEDIUM) == GameResult(Difficulty.MEDIUM, 25, 12)


@pytest.mark.parametrize("content", ["not json", "[1, 2]", '{"easy": {"time_left": "x"}}',
                                     '{"unknown": {"time_left": 1, "attempts": 1}}'])
def test_corrupted_file_starts_without_record(tmp_path, content):
    path = tmp_path / "scores.json"
    path.write_text(content, encoding="utf-8")

    scores = ScoreRepository(path)

    assert scores.get_best(Difficulty.EASY) is None
