
from dataclasses import dataclass


DEFAULT_EFFECT_SECONDS = 10


@dataclass(frozen=True)
class CardEffect:
    """Describes the time effect of a special card."""

    seconds_delta: int

    def __post_init__(self):
        if not isinstance(self.seconds_delta, int) or isinstance(
            self.seconds_delta, bool
        ):
            raise TypeError("seconds_delta must be an integer.")

    def has_effect(self) -> bool:
        """Tells whether the effect changes the timer."""
        return self.seconds_delta != 0

NO_EFFECT = CardEffect(seconds_delta=0)
