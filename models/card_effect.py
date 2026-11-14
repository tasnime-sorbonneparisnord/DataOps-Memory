
from models.card import Card
from models.effect import CardEffect, DEFAULT_EFFECT_SECONDS, NO_EFFECT

__all__ = [
    "CardEffect",
    "DEFAULT_EFFECT_SECONDS",
    "NO_EFFECT",
    "SpecialCard",
    "CoffeeCard",
    "CriticalCard",
]


class SpecialCard(Card):
    """Base class for special cards."""

    def __init__(
        self,
        card_id: str,
        title: str,
        effect: CardEffect,
        icon: str = ""
    ):
        super().__init__(card_id, icon)

        if not effect.has_effect():
            raise ValueError("A special card must change the timer.")

        self.title = title
        self.effect = effect

    @property
    def label(self) -> str:
        return self.title

    def activate(self) -> CardEffect:
        """Returns the time effect of the card (polymorphism)."""
        return self.effect

    def is_special(self) -> bool:
        return True


class CoffeeCard(SpecialCard):
    """Special card that adds time to the countdown."""

    def __init__(self, card_id: str, seconds: int = DEFAULT_EFFECT_SECONDS):
        _check_positive(seconds)
        effect = CardEffect(seconds_delta=seconds)
        super().__init__(card_id, "Café", effect, icon="coffee.png")


class CriticalCard(SpecialCard):
    """Special card that removes time from the countdown."""

    def __init__(self, card_id: str, seconds: int = DEFAULT_EFFECT_SECONDS):
        _check_positive(seconds)
        effect = CardEffect(seconds_delta=-seconds)
        super().__init__(card_id, "Critique", effect, icon="critical.png")


def _check_positive(seconds: int):
    if not isinstance(seconds, int) or isinstance(seconds, bool) or seconds <= 0:
        raise ValueError("Effect seconds must be a positive integer.")