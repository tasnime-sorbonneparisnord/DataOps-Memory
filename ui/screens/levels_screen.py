"""Page « Jouer » : un grand bouton doré par niveau."""

import pygame

from game.enums import Difficulty
from ui.screens.page import CENTER_X, MenuPage
from ui.section_button import SectionButton

LEVEL_ICONS = {
    Difficulty.EASY: "coffee.png",
    Difficulty.MEDIUM: "database_incident.png",
    Difficulty.HARD: "critical.png",
}
LEVEL_WIDTH, LEVEL_HEIGHT, LEVEL_GAP, FIRST_LEVEL_TOP = 560, 110, 24, 170


class LevelsScreen(MenuPage):
    """Un grand bouton doré par niveau ; un clic ouvre la présentation du niveau."""

    def __init__(self, app):
        super().__init__(app, app.t("levels.title"))
        self._buttons = {}
        for position, difficulty in enumerate(Difficulty):
            top = FIRST_LEVEL_TOP + position * (LEVEL_HEIGHT + LEVEL_GAP)
            rect = pygame.Rect(CENTER_X - LEVEL_WIDTH // 2, top, LEVEL_WIDTH, LEVEL_HEIGHT)
            self._buttons[difficulty] = SectionButton(
                rect, app.t.level_name(difficulty), icon=LEVEL_ICONS[difficulty], title_size=46)

    def handle_page_event(self, event):
        for difficulty, button in self._buttons.items():
            if button.is_clicked(event):
                self.app.show_level_intro(difficulty)
                return

    def draw_content(self, surface):
        for button in self._buttons.values():
            button.draw(surface, self.app.fonts, self.app.icons)
