
from enum import Enum


class Difficulty(Enum):
    """The three difficulty levels of the game."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameState(Enum):
    """Lifecycle of a game; it controls which actions are allowed."""

    READY = "ready"            # created, no game started yet
    PLAYING = "playing"        # waiting for the player to turn a card
    COMPARING = "comparing"    # two different cards shown, waiting for the delay
    WON = "won"                # every incident resolved
    LOST = "lost"              # countdown reached zero

    def is_over(self) -> bool:
        return self in (GameState.WON, GameState.LOST)

    def is_running(self) -> bool:
        return self in (GameState.PLAYING, GameState.COMPARING)


class SelectionOutcome(Enum):
    """What happened after the player selected a card (read by the UI)."""

    REJECTED = "rejected"              # selection not allowed, nothing changed
    FIRST_CARD = "first_card"          # first card of the turn revealed
    MATCH = "match"                    # incident and its solution found
    MISMATCH = "mismatch"              # wrong pair, call resolve_mismatch() later
    SPECIAL_ACTIVATED = "special"      # Coffee / Critical card applied
