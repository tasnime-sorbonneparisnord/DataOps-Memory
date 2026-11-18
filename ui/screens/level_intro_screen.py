"""Présentation d'un niveau : un personnage explique, dans sa bulle, ce qui attend le joueur."""

import pygame

from game.enums import Difficulty
from game.levels import get_level
from ui.drawing import draw_text, wrap_text
from ui.floating_sprite import FloatingSprite, load_image
from ui.screens.page import CENTER_X, MenuPage
from ui.section_button import SectionButton

# Pour chaque niveau : image et zone de texte dans la bulle, en fractions de l'image
# (gauche, haut, largeur, hauteur). La phrase d'ambiance est la clé « intro.tagline.<niveau> ».
LEVEL_INTROS = {
    Difficulty.EASY: ("level_easy.png", (0.32, 0.14, 0.60, 0.40)),
    Difficulty.MEDIUM: ("level_medium.png", (0.38, 0.17, 0.54, 0.52)),
    Difficulty.HARD: ("level_hard.png", (0.27, 0.12, 0.64, 0.40)),
}

IMAGE_AREA = pygame.Rect(90, 135, 1100, 545)        # où l'image est posée
TEXT_COLOR = (29, 42, 90)
HIGHLIGHT_COLOR = (108, 60, 240)
BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT = 708, 320, 62
MAX_FONT_SIZE, MIN_FONT_SIZE = 34, 16


def level_description(difficulty: Difficulty, t) -> list:
    """Les spécificités d'un niveau, calculées depuis sa configuration (aucun chiffre en dur).

    t est le traducteur (Translator) : le texte suit la langue choisie.
    """
    level = get_level(difficulty)
    lines = [
        t("intro.incidents", count=level.incident_count),
        t("intro.cards", cards=level.card_count, seconds=level.time_limit),
    ]
    if level.special_count == 0:
        lines.append(t("intro.no_special"))
    else:
        for key, count in (("intro.coffee", level.coffee_count),
                           ("intro.critical", level.critical_count)):
            lines.append(t(key, count=count, s="s" if count > 1 else "",
                           seconds=level.effect_seconds))
    return lines


class LevelIntroScreen(MenuPage):
    """Le personnage du niveau et sa bulle ; « C'est parti ! » lance la partie."""

    def __init__(self, app, difficulty: Difficulty):
        back_rect = (CENTER_X - BUTTON_WIDTH - 20, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT)
        super().__init__(app, app.t("level.title", name=app.t.level_name(difficulty)),
                         back_rect=back_rect)
        self._difficulty = difficulty
        image_file, self._text_box = LEVEL_INTROS[difficulty]
        self._tagline = app.t(f"intro.tagline.{difficulty.value}")
        self._lines = level_description(difficulty, app.t)
        self._start_button = SectionButton((CENTER_X + 20, BUTTON_TOP, BUTTON_WIDTH, BUTTON_HEIGHT),
                                           app.t("intro.start"), icon="menu_play.png",
                                           title_size=30)
        self._sprite, self._image_rect = self._create_sprite(image_file)

    def _create_sprite(self, image_file):
        image = load_image(image_file, IMAGE_AREA.height)
        if image is None:
            return None, IMAGE_AREA
        if image.get_width() > IMAGE_AREA.width:        # image trop large : on la réduit
            height = round(IMAGE_AREA.height * IMAGE_AREA.width / image.get_width())
            image = load_image(image_file, height)
        rect = image.get_rect(midbottom=IMAGE_AREA.midbottom)
        return FloatingSprite(image, rect.midbottom, amplitude=4, period=3.2), rect

    def go_back(self):
        self.app.show_levels()

    def handle_page_event(self, event):
        if self._start_button.is_clicked(event):   # fondu au noir, vidéo, fondu, partie
            self.app.fade_to(lambda: self.app.show_cinematic(self._difficulty))

    def update(self, delta_seconds):
        if self._sprite is not None:
            self._sprite.update(delta_seconds)

    def draw_content(self, surface):
        if self._sprite is not None:
            self._sprite.draw(surface)
        self._draw_bubble_text(surface)
        self._start_button.draw(surface, self.app.fonts, self.app.icons)

    def _bubble_rect(self) -> pygame.Rect:
        left, top, width, height = self._text_box
        image = self._image_rect
        return pygame.Rect(image.left + left * image.width, image.top + top * image.height,
                           width * image.width, height * image.height)

    def _draw_bubble_text(self, surface):
        box = self._bubble_rect()
        font, rows = self._fit_text(box)
        step = font.get_linesize() + 4
        y = box.centery - (len(rows) * step) / 2 + step / 2
        for text, color in rows:
            draw_text(surface, text, font, color, center=(box.centerx, y))
            y += step

    def _fit_text(self, box):
        """La plus grande police pour laquelle tout le texte tient dans la bulle."""
        for size in range(MAX_FONT_SIZE, MIN_FONT_SIZE - 1, -2):
            font = self.app.fonts.get(size)
            rows = [(line, TEXT_COLOR) for line in self._lines]
            rows += [(line, HIGHLIGHT_COLOR) for line in wrap_text(self._tagline, font, box.width)]
            fits_width = all(font.size(text)[0] <= box.width for text, _ in rows)
            if fits_width and len(rows) * (font.get_linesize() + 4) <= box.height:
                return font, rows
        return font, rows
