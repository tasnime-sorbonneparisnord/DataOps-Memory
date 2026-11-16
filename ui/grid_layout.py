"""Calcul de la position des cartes à l'écran, et conversion d'un clic en numéro de carte.

Cette classe ne dessine rien : elle fait seulement des calculs, ce qui permet
de la tester avec pytest sans ouvrir de fenêtre.
"""

import pygame

from ui.settings import CARD_GAP, CARD_MAX_WIDTH, CARD_RATIO


class GridLayout:
    """Place rows x columns cartes, centrées dans une zone de l'écran."""

    def __init__(self, area, rows: int, columns: int,
                 gap: int = CARD_GAP, max_width: int = CARD_MAX_WIDTH, ratio: float = CARD_RATIO):
        if rows <= 0 or columns <= 0:
            raise ValueError("The grid needs at least one row and one column.")

        area = pygame.Rect(area)
        width_by_columns = (area.width - gap * (columns - 1)) / columns
        width_by_rows = (area.height - gap * (rows - 1)) / rows / ratio
        card_width = int(min(width_by_columns, width_by_rows, max_width))
        card_height = int(card_width * ratio)

        grid_width = columns * card_width + (columns - 1) * gap
        grid_height = rows * card_height + (rows - 1) * gap
        left = area.left + (area.width - grid_width) // 2
        top = area.top + (area.height - grid_height) // 2

        self.rows = rows
        self.columns = columns
        self.card_size = (card_width, card_height)
        self.rects = [
            pygame.Rect(left + col * (card_width + gap), top + row * (card_height + gap),
                        card_width, card_height)
            for row in range(rows) for col in range(columns)
        ]

    def rect_of(self, index: int) -> pygame.Rect:
        return self.rects[index]

    def index_at(self, position):
        """Renvoie le numéro de la carte sous la souris, ou None (clic hors des cartes)."""
        for index, rect in enumerate(self.rects):
            if rect.collidepoint(position):
                return index
        return None