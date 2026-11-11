
from dataclasses import dataclass

from models.card import Card


@dataclass(frozen=True)
class CardEffect:
    """Describes the time effect of a special card."""

    seconds_delta: int

    def __post_init__(self):
        if not isinstance(self.seconds_delta, int) or isinstance(
            self.seconds_delta, bool
        ):
            raise TypeError("seconds_delta must be an integer.")

        if self.seconds_delta == 0:
            raise ValueError("An effect cannot have zero seconds.")

    def get_description(self) -> str:
        """Returns a readable description of the effect."""
        if self.seconds_delta > 0:
            return f"Adds {self.seconds_delta} seconds."

        return f"Removes {abs(self.seconds_delta)} seconds."


class SpecialCard(Card):
    """Base class for special cards."""

    def __init__(self, card_id: str, title: str, effect: CardEffect):
        super().__init__(card_id)
        self.title = title
        self.effect = effect

    @property
    def label(self) -> str:
        return self.title


class CoffeeCard(SpecialCard):
    """Special card that adds 10 seconds."""

    def __init__(self, card_id: str):
        effect = CardEffect(seconds_delta=10)
        super().__init__(card_id, "Coffee", effect)


class CriticalCard(SpecialCard):
    """Special card that removes 10 seconds."""

    def __init__(self, card_id: str):
        effect = CardEffect(seconds_delta=-10)
        super().__init__(card_id, "Critical", effect)