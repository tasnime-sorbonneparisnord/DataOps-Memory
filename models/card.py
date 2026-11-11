
from abc import ABC, abstractmethod
from enum import Enum


class CardState(Enum):
    """Represents the state of a card."""

    HIDDEN = "hidden"
    REVEALED = "revealed"
    MATCHED = "matched"


class Card(ABC):
    """Abstract base class for all game cards."""

    def __init__(self, card_id: str):
        if not card_id:
            raise ValueError("Card ID cannot be empty.")

        self.card_id = card_id
        self.state = CardState.HIDDEN

    @property
    @abstractmethod
    def label(self) -> str:
        """Returns the text displayed on the card."""
        pass

    def reveal(self):
        """Reveals the card."""
        if self.state != CardState.MATCHED:
            self.state = CardState.REVEALED

    def hide(self):
        """Hides the card if it is not already matched."""
        if self.state != CardState.MATCHED:
            self.state = CardState.HIDDEN

    def mark_as_matched(self):
        """Marks the card as successfully matched."""
        self.state = CardState.MATCHED

    def is_revealed(self) -> bool:
        return self.state == CardState.REVEALED

    def is_matched(self) -> bool:
        return self.state == CardState.MATCHED


class PairCard(Card, ABC):
    """Abstract class for incident and solution cards."""

    def __init__(
        self,
        card_id: str,
        pair_id: str,
        title: str,
        description: str
    ):
        super().__init__(card_id)

        if not pair_id:
            raise ValueError("Pair ID cannot be empty.")

        self.pair_id = pair_id
        self.title = title
        self.description = description

    @property
    def label(self) -> str:
        return self.title

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