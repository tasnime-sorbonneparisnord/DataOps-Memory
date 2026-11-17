"""Écran d'accueil animé : choix du niveau, règles du jeu et meilleurs scores."""

import pygame

from game.enums import Difficulty
from ui.button import Button
from ui.drawing import draw_database_icon, draw_text
from ui.floating_sprite import FloatingSprite, load_image, wave
from ui.screens.base import Screen
from ui.settings import COLORS, LEVEL_NAMES, WINDOW_WIDTH

CENTER_X = WINDOW_WIDTH // 2

# Boutons de niveau empilés au centre, pour laisser de la place aux personnages
BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_GAP = 320, 80, 14
FIRST_BUTTON_TOP = 262
SMALL_BUTTON_TOP = 556

# Personnages : (fichier, hauteur affichée, position du bas, amplitude, période)
CHARACTERS = [
    ("character_laptop_top.png", 215, (205, 475), 10, 3.4),
    ("character_coder_left.png", 230, (300, 785), 4, 2.6),
    ("character_designer_lying.png", 130, (CENTER_X, 790), 3, 3.0),
    ("character_team_right.png", 320, (1105, 790), 4, 2.8),
]

# Icônes qui flottent autour des boutons : (fichier, centre, période)
FLOATING_ICONS = [
    ("cloud_solution.png", (395, 300), 3.2),
    ("database_solution.png", (890, 300), 2.7),
    ("network_solution.png", (385, 470), 2.9),
    ("pipeline_solution.png", (895, 470), 3.5),
]
ICON_BUBBLE_SIZE = 58


class MenuScreen(Screen):
    """Affiche le titre, un bouton par niveau, puis « Comment jouer » et « Quitter ».

    Les personnages, les icônes et le titre flottent doucement grâce à update(dt).
    """

    def __init__(self, app):
        super().__init__(app)
        self._time = 0.0
        self._level_buttons = self._create_level_buttons()
        self._rules_button = Button((CENTER_X - 230, SMALL_BUTTON_TOP, 220, 56),
                                    "Comment jouer", primary=False)
        self._quit_button = Button((CENTER_X + 10, SMALL_BUTTON_TOP, 220, 56),
                                   "Quitter", primary=False)
        self._sprites = self._create_characters() + self._create_floating_icons()

    # ------------------------------------------------------------------
    # Création des éléments
    # ------------------------------------------------------------------

    def _create_level_buttons(self) -> dict:
        left = CENTER_X - BUTTON_WIDTH // 2
        buttons = {}
        for position, difficulty in enumerate(Difficulty):
            top = FIRST_BUTTON_TOP + position * (BUTTON_HEIGHT + BUTTON_GAP)
            buttons[difficulty] = Button((left, top, BUTTON_WIDTH, BUTTON_HEIGHT),
                                         LEVEL_NAMES[difficulty.value],
                                         sublabel=self._record_text(difficulty))
        return buttons

    def _record_text(self, difficulty: Difficulty) -> str:
        best = self.app.scores.get_best(difficulty)
        if best is None:
            return "Pas encore de record"
        return f"Record : {best.time_left} s · {best.attempts} essais"

    def _create_characters(self) -> list:
        sprites = []
        for index, (file_name, height, midbottom, amplitude, period) in enumerate(CHARACTERS):
            image = load_image(file_name, height)
            if image is not None:      # image absente : on l'ignore, sans planter
                sprites.append(FloatingSprite(image, midbottom, amplitude=amplitude,
                                              period=period, phase=index))
        return sprites

    def _create_floating_icons(self) -> list:
        sprites = []
        for index, (file_name, center, period) in enumerate(FLOATING_ICONS):
            bubble = self._icon_bubble(file_name)
            midbottom = (center[0], center[1] + ICON_BUBBLE_SIZE // 2)
            sprites.append(FloatingSprite(bubble, midbottom, amplitude=8,
                                          period=period, phase=index * 1.3))
        return sprites

    def _icon_bubble(self, file_name: str) -> pygame.Surface:
        """Une icône blanche dans un rond violet, pour qu'elle se voie sur le fond clair."""
        size = ICON_BUBBLE_SIZE
        bubble = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(bubble, COLORS["card_back"], (size // 2, size // 2), size // 2)
        icon = self.app.icons.get(file_name, size - 22)
        bubble.blit(icon, icon.get_rect(center=(size // 2, size // 2)))
        return bubble

    # ------------------------------------------------------------------
    # Boucle : événements, animation, dessin
    # ------------------------------------------------------------------

    def handle_event(self, event):
        for difficulty, button in self._level_buttons.items():
            if button.is_clicked(event):
                self.app.start_game(difficulty)
                return
        if self._rules_button.is_clicked(event):
            self.app.show_rules()
        elif self._quit_button.is_clicked(event):
            self.app.quit()

    def update(self, delta_seconds):
        self._time += delta_seconds
        for sprite in self._sprites:
            sprite.update(delta_seconds)

    def draw(self, surface):
        surface.blit(self.app.menu_background, (0, 0))
        for sprite in self._sprites:
            sprite.draw(surface)
        self._draw_texts(surface)
        for button in self._level_buttons.values():
            button.draw(surface, self.app.fonts)
        self._rules_button.draw(surface, self.app.fonts)
        self._quit_button.draw(surface, self.app.fonts)

    def _draw_texts(self, surface):
        fonts = self.app.fonts
        title_y = 105 + round(wave(self._time, 6, 3.0))     # le titre flotte
        title = draw_text(surface, "DataOps Memory", fonts.get(68, bold=True), COLORS["title"],
                          center=(CENTER_X + 45, title_y))
        draw_database_icon(surface, (title.left - 55, title.centery), 70, COLORS["title"],
                           COLORS["background_top"])

        draw_text(surface, "Associez chaque incident à sa solution avant la fin du temps !",
                  fonts.get(24), COLORS["text"], center=(CENTER_X, 180))

        pulse = (wave(self._time, 0.5, 2.0) + 0.5)       # entre 0 et 1 : le texte « respire »
        color = _mix(COLORS["text_muted"], COLORS["title"], pulse)
        draw_text(surface, "Choisissez un niveau", fonts.get(22, bold=True), color,
                  center=(CENTER_X, 232))


def _mix(color_a, color_b, ratio: float) -> tuple:
    """Couleur intermédiaire entre color_a (ratio 0) et color_b (ratio 1)."""
    return tuple(round(a + (b - a) * ratio) for a, b in zip(color_a, color_b))