"""Page « Meilleurs scores » : le record de chaque niveau."""

import pygame

from game.enums import Difficulty
from ui.drawing import draw_text
from ui.gold_style import GOLD, render_gold_title, tint_icon
from ui.screens.page import CENTER_X, MenuPage

PANEL_RECT = pygame.Rect(CENTER_X - 380, 160, 760, 440)


class ScoresScreen(MenuPage):
    """Un tableau : niveau, temps restant et nombre d'essais du meilleur score."""

    def __init__(self, app):
        super().__init__(app, app.t("scores.title"))

    def draw_content(self, surface):
        inner = self.draw_content_panel(surface, PANEL_RECT)
        fonts = self.app.fonts
        columns = (inner.left + 80, inner.left + 390, inner.left + 590)

        headers = (self.app.t("scores.level"), self.app.t("scores.time_left"), self.app.t("scores.attempts"))
        for x, header in zip(columns, headers):
            draw_text(surface, header.upper(), fonts.get(22), GOLD["muted"], midleft=(x, inner.top + 45))
        pygame.draw.line(surface, GOLD["frame"], (inner.left + 40, inner.top + 75),
                         (inner.right - 40, inner.top + 75), 2)

        trophy = tint_icon(self.app.icons.get("menu_scores.png", 34), GOLD["title"])
        for row, difficulty in enumerate(Difficulty):
            y = inner.top + 145 + row * 95
            surface.blit(trophy, trophy.get_rect(center=(inner.left + 45, y)))
            name = render_gold_title(self.app.t.level_name(difficulty), fonts.get(36))
            surface.blit(name, name.get_rect(midleft=(columns[0], y)))
            best = self.app.scores.get_best(difficulty)
            if best is None:
                draw_text(surface, self.app.t("scores.none"), fonts.get(24), GOLD["muted"],
                          midleft=(columns[1], y))
            else:
                draw_text(surface, f"{best.time_left} s", fonts.get(30), GOLD["text"],
                          midleft=(columns[1], y))
                draw_text(surface, str(best.attempts), fonts.get(30), GOLD["text"],
                          midleft=(columns[2], y))
