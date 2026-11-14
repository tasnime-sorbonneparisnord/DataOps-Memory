
from dataclasses import dataclass

from game.enums import Difficulty


@dataclass(frozen=True)
class GameResult:
    """Outcome of a finished game."""

    difficulty: Difficulty
    time_left: int
    attempts: int
    won: bool = True

    def is_better_than(self, other: "GameResult") -> bool:
        """The only place where the score rule is written (DRY).

        More time left is better; on a tie, fewer attempts is better.
        A lost game is never better than anything.
        """
        if not self.won:
            return False

        if other is None or not other.won:
            return True

        if self.time_left != other.time_left:
            return self.time_left > other.time_left

        return self.attempts < other.attempts
