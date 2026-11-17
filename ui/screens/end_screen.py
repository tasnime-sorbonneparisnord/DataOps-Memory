"""Écran de fin : victoire ou défaite, score, record et boutons pour rejouer."""

import pygame

from ui.button import Button
from ui.drawing import draw_panel, draw_text
from ui.screens.base import Screen
from ui.settings import COLORS, LEVEL_NAMES, WINDOW_WIDTH


class EndScreen(Screen):
    """Affiche le résultat d'une partie terminée."""

    def __init__(self, app, result, is_record: bool):
        super().__init__(app)
        self._result = result
        self._is_record = is_record
        center_x = WINDOW_WIDTH // 2
        self._replay_button = Button((center_x - 290, 600, 270, 70), "Rejouer")
        self._menu_button = Button((center_x + 20, 600, 270, 70), "Changer de niveau",
                                   primary=False)

    def handle_event(self, event):
        if self._replay_button.is_clicked(event):
            self.app.start_game(self._result.difficulty)
        elif self._menu_button.is_clicked(event):
            self.app.show_levels()

    def draw(self, surface):
        surface.blit(self.app.background, (0, 0))
        fonts, result = self.app.fonts, self._result
        center_x = WINDOW_WIDTH // 2

        panel = pygame.Rect(0, 0, 760, 420)
        panel.midtop = (center_x, 130)
        draw_panel(surface, panel)

        if result.won:
            title, color = "Production sauvée !", COLORS["success"]
            subtitle = "Tous les incidents sont réparés. Bravo !"
        else:
            title, color = "Temps écoulé...", COLORS["danger"]
            subtitle = "La prod est toujours en panne. Retente ta chance !"

        draw_text(surface, title, fonts.get(56, bold=True), color, center=(center_x, 200))
        draw_text(surface, subtitle, fonts.get(24), COLORS["text"], center=(center_x, 262))
        draw_text(surface, f"Niveau : {LEVEL_NAMES[result.difficulty.value]}", fonts.get(24),
                  COLORS["text_muted"], center=(center_x, 320))

        if result.won:
            draw_text(surface, f"Temps restant : {result.time_left} s   ·   "
                               f"Tentatives : {result.attempts}",
                      fonts.get(30, bold=True), COLORS["text"], center=(center_x, 385))
        self._draw_record(surface, center_x)

        self._replay_button.draw(surface, fonts)
        self._menu_button.draw(surface, fonts)

    def _draw_record(self, surface, center_x):
        fonts = self.app.fonts
        if self._is_record:
            draw_text(surface, "Nouveau record !", fonts.get(30, bold=True), COLORS["title"],
                      center=(center_x, 455))
            return
        best = self.app.scores.get_best(self._result.difficulty)
        if best:
            draw_text(surface, f"Record du niveau : {best.time_left} s · {best.attempts} tentatives",
                      fonts.get(22), COLORS["text_muted"], center=(center_x, 455))
