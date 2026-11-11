
import random

from models.card import Card, PairCard
from models.card_effect import SpecialCard


class Board:
    """Represents the game board containing all cards."""

    def __init__(self, rows: int, columns: int):
        if not isinstance(rows, int) or isinstance(rows, bool) or rows <= 0:
            raise ValueError("Rows must be a positive integer.")

        if not isinstance(columns, int) or isinstance(columns, bool) or columns <= 0:
            raise ValueError("Columns must be a positive integer.")

        self.rows = rows
        self.columns = columns
        self.cards = []

    @property
    def capacity(self) -> int:
        """Returns the maximum number of cards on the board."""
        return self.rows * self.columns

    def add_card(self, card: Card):
        """Adds a card to the board."""
        if not isinstance(card, Card):
            raise TypeError("Only Card objects can be added.")

        if len(self.cards) >= self.capacity:
            raise ValueError("The board is full.")

        if any(existing.card_id == card.card_id for existing in self.cards):
            raise ValueError("Card IDs must be unique.")

        self.cards.append(card)

    def shuffle(self):
        """Randomly shuffles the cards."""
        random.shuffle(self.cards)

    def get_card(self, card_id: str) -> Card:
        """Returns a card using its ID."""
        for card in self.cards:
            if card.card_id == card_id:
                return card

        raise KeyError(f"No card found with ID: {card_id}")

    def get_cards(self) -> tuple:
        """Returns all cards on the board."""
        return tuple(self.cards)

    def get_pair_cards(self) -> tuple:
        """Returns only incident and solution cards."""
        return tuple(
            card for card in self.cards
            if isinstance(card, PairCard)
        )

    def get_special_cards(self) -> tuple:
        """Returns only special cards."""
        return tuple(
            card for card in self.cards
            if isinstance(card, SpecialCard)
        )

    def is_complete(self) -> bool:
        """Checks whether all incident-solution pairs are matched."""
        pair_cards = self.get_pair_cards()

        return (
            len(pair_cards) > 0
            and all(card.is_matched() for card in pair_cards)
        )