
from dataclasses import dataclass

from game.enums import Difficulty


@dataclass(frozen=True)
class LevelConfig:
    """Parameters of one difficulty level (no hard-coded values in the game)."""

    incident_count: int
    coffee_count: int
    critical_count: int
    rows: int
    columns: int
    time_limit: int
    effect_seconds: int

    def __post_init__(self):
        if self.incident_count <= 0:
            raise ValueError("A level needs at least one incident.")

        if self.coffee_count < 0 or self.critical_count < 0:
            raise ValueError("Special card counts cannot be negative.")

        if self.time_limit <= 0 or self.effect_seconds <= 0:
            raise ValueError("Times must be positive.")

        if self.card_count != self.rows * self.columns:
            raise ValueError(
                f"{self.card_count} cards do not fit a "
                f"{self.rows}x{self.columns} grid."
            )

    @property
    def special_count(self) -> int:
        return self.coffee_count + self.critical_count

    @property
    def card_count(self) -> int:
        """Two cards per incident (incident + solution) plus special cards."""
        return 2 * self.incident_count + self.special_count


LEVELS = {
    Difficulty.EASY: LevelConfig(
        incident_count=4, coffee_count=0, critical_count=0,
        rows=2, columns=4, time_limit=60, effect_seconds=10,
    ),
    Difficulty.MEDIUM: LevelConfig(
        incident_count=8, coffee_count=1, critical_count=1,
        rows=3, columns=6, time_limit=90, effect_seconds=10,
    ),
    Difficulty.HARD: LevelConfig(
        incident_count=12, coffee_count=2, critical_count=2,
        rows=4, columns=7, time_limit=120, effect_seconds=10,
    ),
}


def get_level(difficulty: Difficulty) -> LevelConfig:
    """Returns the configuration of a difficulty level."""
    try:
        return LEVELS[difficulty]
    except KeyError:
        raise ValueError(f"Unknown difficulty: {difficulty}") from None
