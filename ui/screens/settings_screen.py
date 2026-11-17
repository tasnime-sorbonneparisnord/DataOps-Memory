"""Page « Paramètres » (première version) : les réglages arrivent à l'étape suivante."""

import pygame

from ui.drawing import draw_text
from ui.gold_style import GOLD, render_gold_title, tint_icon
from ui.screens.page import CENTER_X, MenuPage

PANEL_RECT = pygame.Rect(CENTER_X - 380, 160, 760, 420)

SETTINGS = [
    ("settings_volume.png", "Volume", "Musique et effets sonores"),
    ("settings_brightness.png", "Luminosité", "Plus clair ou plus sombre"),
    ("settings_language.png", "Langue", "Français / English"),
]


class SettingsScreen(MenuPage):
    """Montre les réglages prévus ; ils deviendront réglables à l'étape suivante."""

    def __init__(self, app):
        super().__init__(app, "Paramètres")

    def draw_content(self, surface):
        inner = self.draw_content_panel(surface, PANEL_RECT)
        fonts = self.app.fonts
        for row, (icon_file, name, description) in enumerate(SETTINGS):
            y = inner.top + 75 + row * 105
            icon = tint_icon(self.app.icons.get(icon_file, 46), GOLD["title"])
            surface.blit(icon, icon.get_rect(center=(inner.left + 60, y)))
            title = render_gold_title(name, fonts.get(34))
            surface.blit(title, title.get_rect(midleft=(inner.left + 110, y - 12)))
            draw_text(surface, description, fonts.get(20), GOLD["muted"],
                      midleft=(inner.left + 114, y + 22))
        draw_text(surface, "Bientôt réglable !", fonts.get(22), GOLD["title"],
                  center=(inner.centerx, inner.bottom - 30))
