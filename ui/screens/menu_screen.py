"""Écran d'accueil : choix du niveau, règles du jeu et meilleurs scores."""

import pygame

from game.enums import Difficulty
from ui.button import Button
from ui.drawing import draw_database_icon, draw_text
from ui.screens.base import Screen
from ui.settings import COLORS, LEVEL_NAMES, WINDOW_WIDTH

BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_GAP = 300, 92, 30


class MenuScreen(Screen):
    """Affiche le titre, un bouton par niveau, puis « Comment jouer » et « Quitter »."""

    def __init__(self, app):
        super().__init__(app)
        self._level_buttons = self._create_level_buttons()
        center_x = WINDOW_WIDTH // 2
        self._rules_button = Button((center_x - 230, 560, 220, 60), "Comment jouer", primary=False)
        self._quit_button = Button((center_x + 10, 560, 220, 60), "Quitter", primary=False)

    def _create_level_buttons(self) -> dict:
        total_width = 3 * BUTTON_WIDTH + 2 * BUTTON_GAP
        left = (WINDOW_WIDTH - total_width) // 2
        buttons = {}
        for position, difficulty in enumerate(Difficulty):
            rect = (left + position * (BUTTON_WIDTH + BUTTON_GAP), 400, BUTTON_WIDTH, BUTTON_HEIGHT)
            buttons[difficulty] = Button(rect, LEVEL_NAMES[difficulty.value],
                                         sublabel=self._record_text(difficulty))
        return buttons

    def _record_text(self, difficulty: Difficulty) -> str:
        best = self.app.scores.get_best(difficulty)
        if best is None:
            return "Pas encore de record"
        return f"Record : {best.time_left} s · {best.attempts} essais"

    def handle_event(self, event):
        for difficulty, button in self._level_buttons.items():
            if button.is_clicked(event):
                self.app.start_game(difficulty)
                return
        if self._rules_button.is_clicked(event):
            self.app.show_rules()
        elif self._quit_button.is_clicked(event):
            self.app.quit()

    def draw(self, surface):
        surface.blit(self.app.menu_background, (0, 0))
        fonts = self.app.fonts
        center_x = WINDOW_WIDTH // 2

        title = draw_text(surface, "DataOps Memory", fonts.get(68, bold=True), COLORS["title"],
                          center=(center_x + 45, 200))
        draw_database_icon(surface, (title.left - 55, title.centery), 70, COLORS["title"],
                           COLORS["background_top"])
        draw_text(surface, "Associez chaque incident à sa solution avant la fin du temps !",
                  fonts.get(24), COLORS["text"], center=(center_x, 290))
        draw_text(surface, "Choisissez un niveau", fonts.get(22, bold=True), COLORS["text_muted"],
                  center=(center_x, 365))

        for button in self._level_buttons.values():
            button.draw(surface, fonts)
        self._rules_button.draw(surface, fonts)
        self._quit_button.draw(surface, fonts)