"""Bouton cliquable, réutilisé par tous les écrans."""

import pygame

from ui.drawing import draw_text
from ui.settings import COLORS


class Button:
    """Un rectangle arrondi avec un texte, qui sait s'il est survolé ou cliqué."""

    def __init__(self, rect, label, *, primary=True, sublabel=""):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.sublabel = sublabel
        self.primary = primary

    def contains(self, position) -> bool:
        return self.rect.collidepoint(position)

    def is_clicked(self, event) -> bool:
        """Vrai si l'événement est un clic gauche sur ce bouton."""
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.contains(event.pos))

    def draw(self, surface, fonts):
        hovered = self.contains(pygame.mouse.get_pos())
        fill, text_color = self._colors(hovered)
        pygame.draw.rect(surface, fill, self.rect, border_radius=14)
        if not self.primary:
            pygame.draw.rect(surface, COLORS["panel_border"], self.rect, 2, border_radius=14)

        if self.sublabel:
            draw_text(surface, self.label, fonts.get(26, bold=True), text_color,
                      center=(self.rect.centerx, self.rect.centery - 12))
            draw_text(surface, self.sublabel, fonts.get(17), text_color,
                      center=(self.rect.centerx, self.rect.centery + 18))
        else:
            draw_text(surface, self.label, fonts.get(24, bold=True), text_color,
                      center=self.rect.center)

    def _colors(self, hovered: bool):
        if self.primary:
            return COLORS["button_hover" if hovered else "button"], COLORS["text_light"]
        return (COLORS["button_secondary_hover" if hovered else "button_secondary"],
                COLORS["text"])