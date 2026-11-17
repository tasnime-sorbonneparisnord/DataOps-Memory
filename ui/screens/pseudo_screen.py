"""Page « Ton pseudo » : le joueur écrit son nom avant d'arriver à l'accueil."""

import pygame

from storage.player_profile import MAX_PSEUDO_LENGTH, InvalidPseudoError
from ui.drawing import draw_text
from ui.gold_style import GOLD, draw_gold_frame
from ui.screens.page import CENTER_X, MenuPage
from ui.section_button import SectionButton

PANEL_RECT = pygame.Rect(CENTER_X - 360, 190, 720, 330)
INPUT_RECT = pygame.Rect(CENTER_X - 280, 300, 560, 76)
VALIDATE_RECT = pygame.Rect(CENTER_X - 160, 620, 320, 64)
ERROR_COLOR = (255, 120, 120)


class PseudoScreen(MenuPage):
    """Une case de saisie : on tape son pseudo, puis Entrée ou « Valider ».

    Le dernier pseudo utilisé est déjà écrit : il suffit d'appuyer sur Entrée.
    """

    def __init__(self, app):
        super().__init__(app, app.t("pseudo.title"), back_rect=None)
        self._text = app.profile.pseudo
        self._error = ""
        self._time = 0.0
        self._validate_button = SectionButton(VALIDATE_RECT, app.t("pseudo.validate"), icon="menu_play.png",
                                              title_size=30)

    def handle_page_event(self, event):
        if event.type == pygame.TEXTINPUT:                 # lettre tapée (accents compris)
            if len(self._text) < MAX_PSEUDO_LENGTH:
                self._text += event.text
                self._error = ""
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self._text = self._text[:-1]
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self._validate()
        elif self._validate_button.is_clicked(event):
            self._validate()

    def _validate(self):
        try:
            self.app.profile.set_pseudo(self._text)
        except InvalidPseudoError as error:
            self._error = self.app.t(f"pseudo.error.{error.code}", max=MAX_PSEUDO_LENGTH)
            return
        self.app.show_menu()

    def go_back(self):
        """Échap ne fait rien ici : il faut choisir un pseudo pour continuer."""

    def update(self, delta_seconds):
        self._time += delta_seconds

    def draw_content(self, surface):
        inner = draw_gold_frame(surface, PANEL_RECT)
        fonts = self.app.fonts
        draw_text(surface, self.app.t("pseudo.question"), fonts.get(28), GOLD["text"],
                  center=(inner.centerx, inner.top + 50))

        pygame.draw.rect(surface, GOLD["text"], INPUT_RECT, border_radius=10)
        pygame.draw.rect(surface, GOLD["frame"], INPUT_RECT, 4, border_radius=10)
        text_rect = draw_text(surface, self._text, fonts.get(40), GOLD["fill"],
                              midleft=(INPUT_RECT.left + 22, INPUT_RECT.centery))
        if int(self._time * 2) % 2 == 0:                  # curseur qui clignote
            x = text_rect.right + 4 if self._text else INPUT_RECT.left + 24
            pygame.draw.line(surface, GOLD["fill"], (x, INPUT_RECT.top + 16),
                             (x, INPUT_RECT.bottom - 16), 3)

        if self._error:
            message, color = self._error, ERROR_COLOR
        else:
            message, color = self.app.t("pseudo.hint", max=MAX_PSEUDO_LENGTH), GOLD["muted"]
        draw_text(surface, message, fonts.get(20), color, center=(inner.centerx, inner.bottom - 50))
        self._validate_button.draw(surface, fonts, self.app.icons)
