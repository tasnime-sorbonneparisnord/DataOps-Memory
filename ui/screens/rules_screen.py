"""Écran « Comment jouer » : les règles expliquées simplement."""

import pygame

from ui.button import Button
from ui.drawing import draw_panel, draw_text
from ui.screens.base import Screen
from ui.settings import COLORS, WINDOW_WIDTH

RULES = [
    "Il est 3 h du matin : la prod est en panne et tu es d'astreinte.",
    "Retourne deux cartes à la fois en cliquant dessus.",
    "Si c'est un incident et sa solution, l'incident est réparé !",
    "Sinon, les cartes se recachent : retiens bien leur place.",
    "Carte Café : +10 secondes.   Carte Critique : −10 secondes.",
    "Répare tous les incidents avant la fin du chrono pour gagner.",
    "Record : le plus de temps restant, puis le moins de tentatives.",
]


class RulesScreen(Screen):
    """Affiche les règles et un bouton pour revenir au menu."""

    def __init__(self, app):
        super().__init__(app)
        self._back_button = Button((WINDOW_WIDTH // 2 - 140, 650, 280, 64), "Retour au menu")

    def handle_event(self, event):
        if self._back_button.is_clicked(event):
            self.app.show_menu()

    def draw(self, surface):
        surface.blit(self.app.background, (0, 0))
        fonts = self.app.fonts
        panel = pygame.Rect(0, 0, 900, 470)
        panel.midtop = (WINDOW_WIDTH // 2, 140)
        draw_panel(surface, panel)

        draw_text(surface, "Comment jouer", fonts.get(48, bold=True), COLORS["title"],
                  center=(WINDOW_WIDTH // 2, 90))
        for number, rule in enumerate(RULES):
            draw_text(surface, f"{number + 1}.  {rule}", fonts.get(24), COLORS["text"],
                      midleft=(panel.left + 50, panel.top + 60 + number * 56))
        self._back_button.draw(surface, fonts)