
import math
import random

from game.board_builder import build_board
from game.countdown_timer import CountdownTimer
from game.enums import Difficulty, GameState, SelectionOutcome
from game.game_result import GameResult
from game.levels import LevelConfig, get_level
from models.board import Board
from models.card import Card


class GameNotStartedError(RuntimeError):
    """Raised when the game is used before start()."""


class MemoryGame:
    """Applies the rules of DataOps Memory and coordinates one game.

    It never uses Pygame and never reads files: the incident library and
    the random generator are given from outside (dependency injection),
    and the UI tells it how much time has passed with update().
    """

    def __init__(self, library, rng: random.Random = None):
        self._library = library
        self._rng = rng or random.Random()
        self._state = GameState.READY
        self._difficulty = None
        self._level = None
        self._board = None
        self._timer = None
        self._attempts = 0
        self._selected = []
        self._last_explanation = ""

    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------

    def start(self, difficulty: Difficulty):
        """Draws new incidents, builds the board and starts the countdown."""
        level = get_level(difficulty)
        pairs = self._library.draw(level.incident_count, self._rng)

        self._difficulty = difficulty
        self._level = level
        self._board = build_board(pairs, level, self._rng)
        self._timer = CountdownTimer(level.time_limit)
        self._attempts = 0
        self._selected = []
        self._last_explanation = ""
        self._state = GameState.PLAYING

    def restart(self):
        """Starts a new game at the same level, with a new draw."""
        self._require_started()
        self.start(self._difficulty)

    def update(self, delta_seconds: float):
        """Moves the countdown forward; called by the UI at every frame."""
        if not self._state.is_running():
            return

        self._timer.tick(delta_seconds)
        self._check_time_over()

    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------

    def select_card(self, index: int) -> SelectionOutcome:
        """Handles the card chosen by the player at a board position."""
        self._require_started()
        card = self._board.get_card_at(index)

        if not self._can_select(card):
            return SelectionOutcome.REJECTED

        card.reveal()

        if card.is_special():
            return self._activate_special(card)

        self._selected.append(card)

        if len(self._selected) == 1:
            return SelectionOutcome.FIRST_CARD

        return self._compare_selected_cards()

    def resolve_mismatch(self):
        """Hides the two wrong cards once the UI delay is over."""
        if self._state != GameState.COMPARING:
            return

        self._hide_selected_cards()
        self._state = GameState.PLAYING

    # ------------------------------------------------------------------
    # Read-only information for the UI
    # ------------------------------------------------------------------

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def difficulty(self) -> Difficulty:
        return self._difficulty

    @property
    def level(self) -> LevelConfig:
        return self._level

    @property
    def board(self) -> Board:
        return self._board

    @property
    def attempts(self) -> int:
        return self._attempts

    @property
    def remaining_time(self) -> float:
        return self._timer.remaining if self._timer else 0.0

    @property
    def last_explanation(self) -> str:
        return self._last_explanation

    @property
    def resolved_count(self) -> int:
        return self._board.resolved_count() if self._board else 0

    def is_won(self) -> bool:
        return self._state == GameState.WON

    def is_lost(self) -> bool:
        return self._state == GameState.LOST

    def is_over(self) -> bool:
        return self._state.is_over()

    def result(self) -> GameResult:
        """Returns the result of a finished game."""
        if not self.is_over():
            raise RuntimeError("The game is not finished yet.")

        return GameResult(
            difficulty=self._difficulty,
            time_left=math.ceil(self._timer.remaining),
            attempts=self._attempts,
            won=self.is_won(),
        )

    # ------------------------------------------------------------------
    # Rules (private helpers, one rule each)
    # ------------------------------------------------------------------

    def _can_select(self, card: Card) -> bool:
        return self._state == GameState.PLAYING and card.is_selectable()

    def _activate_special(self, card: Card) -> SelectionOutcome:
        """A special card acts at once, then leaves the board.

        A pair card already turned in this turn is hidden again, without
        counting an attempt.
        """
        effect = card.activate()
        self._timer.add(effect.seconds_delta)
        card.remove()
        self._hide_selected_cards()
        self._check_time_over()
        return SelectionOutcome.SPECIAL_ACTIVATED

    def _compare_selected_cards(self) -> SelectionOutcome:
        self._attempts += 1
        first, second = self._selected

        if first.matches(second):
            self._resolve_pair(first, second)
            return SelectionOutcome.MATCH

        self._state = GameState.COMPARING
        return SelectionOutcome.MISMATCH

    def _resolve_pair(self, first: Card, second: Card):
        first.mark_as_matched()
        second.mark_as_matched()
        self._last_explanation = first.explanation
        self._selected = []

        if self._board.is_complete():
            self._finish(GameState.WON)

    def _hide_selected_cards(self):
        for card in self._selected:
            card.hide()
        self._selected = []

    def _check_time_over(self):
        if self._timer.is_expired() and not self.is_over():
            self._finish(GameState.LOST)

    def _finish(self, final_state: GameState):
        self._state = final_state
        self._timer.stop()

    def _require_started(self):
        if self._state == GameState.READY:
            raise GameNotStartedError("Call start() before playing.")
