"""Page « Jouer » : choix du niveau, avec la taille de la grille, le temps et le record."""

import pygame

from game.enums import Difficulty
from game.levels import get_level
from ui.screens.page import CENTER_X, MenuPage
from ui.section_button import SectionButton
from ui.settings import LEVEL_NAMES

LEVEL_ICONS = {
    Difficulty.EASY: "coffee.png",
    Difficulty.MEDIUM: "database_incident.png",
    Difficulty.HARD: "critical.png",
}
LEVEL_WIDTH, LEVEL_HEIGHT, LEVEL_GAP, FIRST_LEVEL_TOP = 560, 110, 24, 170


class LevelsScreen(MenuPage):
    """Un grand bouton doré par niveau ; un clic lance la partie."""

    def __init__(self, app):
        super().__init__(app, "Choisis ton niveau")
        self._buttons = {}
        for position, difficulty in enumerate(Difficulty):
            top = FIRST_LEVEL_TOP + position * (LEVEL_HEIGHT + LEVEL_GAP)
            rect = pygame.Rect(CENTER_X - LEVEL_WIDTH // 2, top, LEVEL_WIDTH, LEVEL_HEIGHT)
            self._buttons[difficulty] = SectionButton(
                rect, LEVEL_NAMES[difficulty.value], subtitle=self._details(difficulty),
                icon=LEVEL_ICONS[difficulty], title_size=42, always_show_subtitle=True)

    def _details(self, difficulty: Difficulty) -> str:
        level = get_level(difficulty)
        text = f"{level.rows * level.columns} cartes · {level.time_limit} s"
        best = self.app.scores.get_best(difficulty)
        if best is None:
            return text + " · pas encore de record"
        return text + f" · record : {best.time_left} s, {best.attempts} essais"

    def handle_page_event(self, event):
        for difficulty, button in self._buttons.items():
            if button.is_clicked(event):
                self.app.start_game(difficulty)
                return

    def draw_content(self, surface):
        for button in self._buttons.values():
            button.draw(surface, self.app.fonts, self.app.icons)
