
from abc import ABC, abstractmethod
from enum import Enum

from models.effect import CardEffect, NO_EFFECT


class CardState(Enum):
    """Represents the state of a card."""

    HIDDEN = "hidden"
    REVEALED = "revealed"
    MATCHED = "matched"
    REMOVED = "removed"


class Card(ABC):
    """Abstract base class for all game cards."""

    def __init__(self, card_id: str, icon: str = ""):
        if not card_id:
            raise ValueError("Card ID cannot be empty.")

        self.card_id = card_id
        self.icon = icon
        self.state = CardState.HIDDEN

    @property
    @abstractmethod
    def label(self) -> str:
        """Returns the text displayed on the card."""
        pass

    @abstractmethod
    def activate(self) -> CardEffect:
        """Returns the effect triggered when the card is turned over."""
        pass

    def is_special(self) -> bool:
        """Tells whether the card is a special (time) card."""
        return False

    def is_selectable(self) -> bool:
        """A card can be chosen only while it is hidden."""
        return self.state == CardState.HIDDEN

    def reveal(self):
        """Reveals the card."""
        if self.is_selectable():
            self.state = CardState.REVEALED

    def hide(self):
        """Hides the card if it is still in play (not matched nor removed)."""
        if self.state == CardState.REVEALED:
            self.state = CardState.HIDDEN

    def remove(self):
        """Takes the card off the board (used by special cards)."""
        self.state = CardState.REMOVED

    def mark_as_matched(self):
        """Marks the card as successfully matched."""
        self.state = CardState.MATCHED

    def is_revealed(self) -> bool:
        return self.state == CardState.REVEALED

    def is_matched(self) -> bool:
        return self.state == CardState.MATCHED

    def is_removed(self) -> bool:
        return self.state == CardState.REMOVED


class PairCard(Card, ABC):
    """Abstract class for incident and solution cards."""

    def __init__(
        self,
        card_id: str,
        pair_id: str,
        title: str,
        description: str,
        icon: str = ""
    ):
        super().__init__(card_id, icon)

        if not pair_id:
            raise ValueError("Pair ID cannot be empty.")

        self.pair_id = pair_id
        self.title = title
        self.description = description

    @property
    def label(self) -> str:
        return self.title

    @property
    def explanation(self) -> str:
        """Text shown to the player when the pair is found."""
        return self.description

    def activate(self) -> CardEffect:
        """Incident and solution cards have no effect on the timer."""
        return NO_EFFECT

    @abstractmethod
    def get_pair_role(self) -> str:
        """Returns the type of card in the pair."""
        pass

    def matches(self, other: "PairCard") -> bool:
        """Checks whether two cards form a valid incident-solution pair."""

        return (
            isinstance(other, PairCard)
            and self.pair_id == other.pair_id
            and self.get_pair_role() != other.get_pair_role()
        )


class IncidentCard(PairCard):
    """Card representing an IT incident."""

    def get_pair_role(self) -> str:
        return "incident"


class SolutionCard(PairCard):
    """Card representing the solution to an incident."""

    def get_pair_role(self) -> str:
        return "solution"