"""Page « Comment jouer » : les règles expliquées simplement."""

import pygame

from ui.drawing import draw_text
from ui.gold_style import GOLD
from ui.screens.page import CENTER_X, MenuPage

PANEL_RECT = pygame.Rect(CENTER_X - 470, 150, 940, 480)



class RulesScreen(MenuPage):
    """Affiche les règles numérotées dans un cadre doré."""

    def __init__(self, app):
        super().__init__(app, app.t("rules.title"))

    def draw_content(self, surface):
        inner = self.draw_content_panel(surface, PANEL_RECT)
        fonts = self.app.fonts
        for number, rule in enumerate(self.app.t.raw("rules.lines")):
            y = inner.top + 50 + number * 62
            draw_text(surface, f"{number + 1}.", fonts.get(28), GOLD["title"],
                      midleft=(inner.left + 36, y))
            draw_text(surface, rule, fonts.get(24), GOLD["text"], midleft=(inner.left + 80, y))
