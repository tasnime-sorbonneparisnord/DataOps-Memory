"""Page « Crédits » : l'équipe du projet et le cadre du module."""

import pygame

from ui.drawing import draw_text
from ui.gold_style import GOLD, render_gold_title
from ui.screens.page import CENTER_X, MenuPage

PANEL_RECT = pygame.Rect(CENTER_X - 400, 150, 800, 470)

TEAM = ["Nirinah Vanilla Rafidison", "Khoubeib Bourbia", "Hakimi Tasnime"]


class CreditsScreen(MenuPage):
    """Les membres de l'équipe et le cadre du projet, sous forme de listes."""

    def __init__(self, app):
        super().__init__(app, app.t("credits.title"))

    def draw_content(self, surface):
        inner = self.draw_content_panel(surface, PANEL_RECT)
        fonts = self.app.fonts

        draw_text(surface, self.app.t("credits.heading"), fonts.get(28), GOLD["text"],
                  center=(inner.centerx, inner.top + 45))
        pygame.draw.line(surface, GOLD["frame"], (inner.left + 60, inner.top + 80),
                         (inner.right - 60, inner.top + 80), 2)

        y = inner.top + 125
        sections = [(self.app.t("credits.team"), TEAM),
                    (self.app.t("credits.frame"), [self.app.t("credits.master"), self.app.t("credits.course")])]
        for title, items in sections:
            heading = render_gold_title(title, fonts.get(32))
            surface.blit(heading, heading.get_rect(midleft=(inner.left + 60, y)))
            y += 48
            for item in items:
                pygame.draw.circle(surface, GOLD["title"], (inner.left + 95, y), 5)
                draw_text(surface, item, fonts.get(24), GOLD["text"], midleft=(inner.left + 115, y))
                y += 38
            y += 22
