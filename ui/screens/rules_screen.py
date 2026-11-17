"""Page « Comment jouer » : les règles expliquées simplement."""

import pygame

from ui.drawing import draw_text
from ui.gold_style import GOLD
from ui.screens.page import CENTER_X, MenuPage

PANEL_RECT = pygame.Rect(CENTER_X - 470, 150, 940, 480)

RULES = [
    "Il est 3 h du matin : la prod est en panne et tu es d'astreinte.",
    "Retourne deux cartes à la fois en cliquant dessus.",
    "Si c'est un incident et sa solution, l'incident est réparé !",
    "Sinon, les cartes se recachent : retiens bien leur place.",
    "Carte Café : +10 secondes.   Carte Critique : −10 secondes.",
    "Répare tous les incidents avant la fin du chrono pour gagner.",
    "Record : le plus de temps restant, puis le moins de tentatives.",
]


class RulesScreen(MenuPage):
    """Affiche les règles numérotées dans un cadre doré."""

    def __init__(self, app):
        super().__init__(app, "Comment jouer")

    def draw_content(self, surface):
        inner = self.draw_content_panel(surface, PANEL_RECT)
        fonts = self.app.fonts
        for number, rule in enumerate(RULES):
            y = inner.top + 50 + number * 62
            draw_text(surface, f"{number + 1}.", fonts.get(28), GOLD["title"],
                      midleft=(inner.left + 36, y))
            draw_text(surface, rule, fonts.get(24), GOLD["text"], midleft=(inner.left + 80, y))
