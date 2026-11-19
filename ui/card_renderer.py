"""Dessin d'une carte selon son type et son état."""

import pygame

from models.card import CardState, IncidentCard, SolutionCard
from models.special_card import CoffeeCard, CriticalCard
from ui.drawing import draw_database_icon, draw_text, draw_wrapped_text, line_height
from ui.settings import COLORS, CORNER_RADIUS

# Couleur et badge de chaque type de carte : un dictionnaire plutôt qu'une suite de if/elif.
CARD_STYLES = {
    IncidentCard: ("incident", "INCIDENT"),
    SolutionCard: ("solution", "SOLUTION"),
    CoffeeCard: ("coffee", None),
    CriticalCard: ("critical", None),
}


def card_style(card):
    """Renvoie (nom de la couleur, texte du badge) pour une carte."""
    color_name, badge = CARD_STYLES[type(card)]
    if badge is None:  # carte spéciale : le badge affiche son effet, ex. « +10 s »
        seconds = card.activate().seconds_delta
        badge = f"{seconds:+d} s".replace("-", "−")
    return color_name, badge


class CardRenderer:
    """Dessine une carte : dos, face visible, carte trouvée ou emplacement vide."""

    def __init__(self, fonts, icons):
        self._fonts = fonts
        self._icons = icons

    def draw(self, surface, card, rect, force_face=False):
        if force_face:
            self._draw_face(surface, card, rect)
        elif card.state == CardState.HIDDEN:
            self._draw_back(surface, rect)
        elif card.state == CardState.REMOVED:
            self._draw_empty(surface, rect)
        else:
            self._draw_face(surface, card, rect)
            if card.state == CardState.MATCHED:
                self._draw_matched_veil(surface, rect)

    def _draw_back(self, surface, rect):
        pygame.draw.rect(surface, COLORS["card_back"], rect, border_radius=CORNER_RADIUS)
        draw_database_icon(surface, rect.center, rect.width // 2, COLORS["card_back_icon"],
                           COLORS["card_back"])

    def _draw_empty(self, surface, rect):
        pygame.draw.rect(surface, COLORS["empty_slot"], rect, 2, border_radius=CORNER_RADIUS)

    def _draw_face(self, surface, card, rect):
        color_name, badge = card_style(card)
        pygame.draw.rect(surface, COLORS[color_name], rect, border_radius=CORNER_RADIUS)

        icon_size = rect.width // 3
        icon = self._icons.get(card.icon, icon_size)
        surface.blit(icon, icon.get_rect(midtop=(rect.centerx, rect.top + 10)))

        text_size = max(13, rect.width // 9)
        text_area = pygame.Rect(rect.left + 8, rect.top + icon_size + 14,
                                rect.width - 16, rect.height - icon_size - 52)
        draw_wrapped_text(surface, card.label, self._fonts.get(text_size, bold=True),
                          COLORS["text_light"], text_area, line_spacing=1)
        self._draw_badge(surface, badge, rect)

    def _draw_badge(self, surface, text, rect):
        font = self._fonts.get(max(12, rect.width // 11), bold=True)
        badge = pygame.Rect(0, 0, rect.width - 20, line_height(font) + 4)
        badge.midbottom = (rect.centerx, rect.bottom - 8)
        pygame.draw.rect(surface, COLORS["badge"], badge, border_radius=badge.height // 2)
        draw_text(surface, text, font, COLORS["text"], center=badge.center)

    def _draw_matched_veil(self, surface, rect):
        veil = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(veil, (*COLORS["matched_overlay"], 110), veil.get_rect(),
                         border_radius=CORNER_RADIUS)
        surface.blit(veil, rect)
