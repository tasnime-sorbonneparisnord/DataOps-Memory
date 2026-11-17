"""Page « Paramètres » : volume de la musique et des effets, luminosité et langue."""

import pygame

from ui.drawing import draw_text
from ui.gold_style import GOLD, draw_gold_frame, render_gold_title, tint_icon
from ui.screens.page import CENTER_X, MenuPage
from ui.slider import Slider

PANEL_RECT = pygame.Rect(CENTER_X - 420, 150, 840, 500)
ROW_TOP, ROW_HEIGHT = PANEL_RECT.top + 70, 110
SLIDER_LEFT, SLIDER_WIDTH = PANEL_RECT.left + 380, 430
LANGUAGE_BUTTON_WIDTH, LANGUAGE_BUTTON_HEIGHT = 190, 52
LANGUAGES = [("fr", "Français"), ("en", "English")]     # chaque langue écrite dans sa langue


class SettingsScreen(MenuPage):
    """Chaque réglage s'applique tout de suite ; tout est sauvegardé en quittant la page."""

    def __init__(self, app):
        super().__init__(app, app.t("settings.title"))
        settings = app.settings
        rows = [
            ("music_volume", self._on_music_change),
            ("effects_volume", self._on_effects_change),
            ("brightness", self._on_brightness_change),
        ]
        self._sliders = []
        for number, (name, on_change) in enumerate(rows):
            rect = (SLIDER_LEFT, ROW_TOP + number * ROW_HEIGHT - 20, SLIDER_WIDTH, 40)
            self._sliders.append(Slider(rect, getattr(settings, name), on_change))
        self._language_buttons = self._create_language_buttons()

    def _create_language_buttons(self) -> list:
        top = ROW_TOP + 3 * ROW_HEIGHT - LANGUAGE_BUTTON_HEIGHT // 2
        buttons = []
        for number, (code, label) in enumerate(LANGUAGES):
            left = SLIDER_LEFT + number * (LANGUAGE_BUTTON_WIDTH + 20)
            buttons.append((code, label, pygame.Rect(left, top, LANGUAGE_BUTTON_WIDTH,
                                                     LANGUAGE_BUTTON_HEIGHT)))
        return buttons

    # ------------------------------------------------------------------
    # Réglages
    # ------------------------------------------------------------------

    def _on_music_change(self, value):
        self.app.settings.music_volume = value
        self.app.sound.apply_volumes()

    def _on_effects_change(self, value):
        self.app.settings.effects_volume = value
        self.app.sound.apply_volumes()
        self.app.sound.play("click")              # pour entendre le nouveau volume

    def _on_brightness_change(self, value):
        self.app.settings.brightness = value      # appliquée par App à chaque image

    def handle_page_event(self, event):
        for slider in self._sliders:
            slider.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for code, _, rect in self._language_buttons:
                if rect.collidepoint(event.pos):
                    self.app.settings.language = code
                    self.app.sound.play("click")

    def go_back(self):
        self.app.settings.save()
        super().go_back()

    # ------------------------------------------------------------------
    # Dessin
    # ------------------------------------------------------------------

    def draw_content(self, surface):
        draw_gold_frame(surface, PANEL_RECT)
        rows = [
            ("settings_volume.png", self.app.t("settings.music")),
            ("settings_volume.png", self.app.t("settings.effects")),
            ("settings_brightness.png", self.app.t("settings.brightness")),
            ("settings_language.png", self.app.t("settings.language")),
        ]
        for number, (icon_file, name) in enumerate(rows):
            y = ROW_TOP + number * ROW_HEIGHT
            icon = tint_icon(self.app.icons.get(icon_file, 42), GOLD["title"])
            surface.blit(icon, icon.get_rect(center=(PANEL_RECT.left + 60, y)))
            title = render_gold_title(name, self.app.fonts.get(32))
            surface.blit(title, title.get_rect(midleft=(PANEL_RECT.left + 100, y)))
        for slider in self._sliders:
            slider.draw(surface, self.app.fonts)
        self._draw_language_buttons(surface)

    def _draw_language_buttons(self, surface):
        for code, label, rect in self._language_buttons:
            selected = self.app.settings.language == code
            pygame.draw.rect(surface, GOLD["frame"], rect, border_radius=10)
            fill = GOLD["hover"] if selected else GOLD["fill"]
            pygame.draw.rect(surface, fill, rect.inflate(-6, -6), border_radius=8)
            color = GOLD["fill"] if selected else GOLD["title"]
            draw_text(surface, label, self.app.fonts.get(26), color, center=rect.center)
