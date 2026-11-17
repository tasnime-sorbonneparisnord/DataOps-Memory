"""Grand bouton de menu au style « cadre doré », avec sous-titre, icône et badge."""

import pygame

from ui.drawing import draw_text, render_outlined_text
from ui.gold_style import GOLD, draw_gold_frame, render_gold_title, tint_icon


class SectionButton:
    """Une section du menu : titre doré, sous-titre au survol, icône à droite.

    always_show_subtitle=True affiche le sous-titre en permanence (utile pour
    les niveaux, où il donne la taille de la grille et le record).
    """

    def __init__(self, rect, title, *, subtitle="", icon=None, badge="",
                 title_size=34, always_show_subtitle=False):
        self.rect = pygame.Rect(rect)
        self.title = title
        self.subtitle = subtitle
        self.icon = icon                  # nom d'un fichier de assets/icons, ou None
        self.badge = badge
        self.title_size = title_size
        self.always_show_subtitle = always_show_subtitle

    def contains(self, position) -> bool:
        return self.rect.collidepoint(position)

    def is_clicked(self, event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.contains(event.pos))

    def draw(self, surface, fonts, icons):
        hovered = self.contains(pygame.mouse.get_pos())
        inner = draw_gold_frame(surface, self.rect, hovered=hovered)

        show_subtitle = bool(self.subtitle) and (hovered or self.always_show_subtitle)
        title = render_gold_title(self.title, fonts.get(self.title_size))
        title_y = inner.centery - (12 if show_subtitle else 0)
        surface.blit(title, title.get_rect(midleft=(inner.left + 14, title_y)))
        if show_subtitle:
            draw_text(surface, self.subtitle.upper(), fonts.get(16), GOLD["text"],
                      midleft=(inner.left + 20, inner.centery + 20))

        if self.icon:
            size = inner.height - 16
            icon = tint_icon(icons.get(self.icon, size), GOLD["title"])
            surface.blit(icon, icon.get_rect(midright=(inner.right - 14, inner.centery)))
        if self.badge:
            self._draw_badge(surface, fonts, inner)

    def _draw_badge(self, surface, fonts, inner):
        label = render_outlined_text(self.badge.upper(), fonts.get(18), GOLD["text"],
                                     [(GOLD["outline"], 2)])
        width, height = label.get_width() + 30, 26
        left = inner.right - width
        shape = [(left, inner.top), (inner.right, inner.top),
                 (inner.right, inner.top + height), (left + 14, inner.top + height)]
        pygame.draw.polygon(surface, GOLD["badge"], shape)
        surface.blit(label, label.get_rect(center=(left + width / 2 + 6, inner.top + height / 2)))
