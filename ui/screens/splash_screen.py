"""Écran de démarrage : l'équipe panique devant un incident, le joueur clique pour entrer."""

import pygame

from ui.drawing import draw_text, render_outlined_text
from ui.floating_sprite import FloatingSprite, load_image, wave
from ui.screens.base import Screen
from ui.settings import WINDOW_HEIGHT, WINDOW_WIDTH

# Couleurs propres à cet écran sombre
SPLASH_COLORS = {
    "overlay": (12, 14, 40, 165),      # voile sombre posé sur le fond de l'accueil
    "logo": (255, 204, 61),
    "logo_outline": (28, 20, 58),
    "logo_border": (255, 255, 255),
    "welcome": (126, 176, 255),
    "slogan": (255, 204, 61),
    "hint": (225, 228, 245),
}


RIGHT_CENTER_X = 875       # centre de la zone à droite des personnages
LOGO_HEIGHT = 265


class SplashScreen(Screen):
    """Premier écran du jeu, comme l'écran titre d'un jeu vidéo.

    On y reste tant que le joueur ne clique pas (ou n'appuie pas sur une touche).
    """

    def __init__(self, app):
        super().__init__(app)
        self._time = 0.0
        self._background = self._create_background()
        self._logo = self._create_logo()
        self._welcome = self._create_welcome()
        self._team = self._create_team()

    # ------------------------------------------------------------------
    # Préparation (une seule fois)
    # ------------------------------------------------------------------

    def _create_background(self) -> pygame.Surface:
        background = self.app.menu_background.copy()
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(SPLASH_COLORS["overlay"])
        background.blit(overlay, (0, 0))
        return background

    def _create_logo(self) -> pygame.Surface:
        """Le logo dessiné (assets/images/logo.png), sinon un logo en texte."""
        image = load_image("logo.png", LOGO_HEIGHT)
        if image is not None:
            return image
        logo = render_outlined_text("DataOps Memory", self.app.fonts.display(78),
                                    SPLASH_COLORS["logo"],
                                    [(SPLASH_COLORS["logo_border"], 13),
                                     (SPLASH_COLORS["logo_outline"], 8)])
        return pygame.transform.rotozoom(logo, 3, 1)     # légèrement penché, plus dynamique

    def _create_welcome(self) -> pygame.Surface:
        return render_outlined_text(self.app.t("splash.welcome"),
                                    self.app.fonts.display(46), SPLASH_COLORS["welcome"],
                                    [(SPLASH_COLORS["logo_outline"], 5)])

    def _create_team(self):
        image = load_image("splash_team.png", 780)
        if image is None:          # image absente : l'écran s'affiche sans elle
            return None
        # petit tremblement rapide : ils stressent !
        return FloatingSprite(image, (265, WINDOW_HEIGHT + 30), amplitude=3, period=0.9)

    # ------------------------------------------------------------------
    # Boucle
    # ------------------------------------------------------------------

    def handle_event(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            self.app.show_pseudo()

    def update(self, delta_seconds):
        self._time += delta_seconds
        if self._team is not None:
            self._team.update(delta_seconds)

    def draw(self, surface):
        surface.blit(self._background, (0, 0))
        if self._team is not None:
            self._team.draw(surface)

        logo_y = 200 + round(wave(self._time, 5, 2.5))
        surface.blit(self._logo, self._logo.get_rect(center=(RIGHT_CENTER_X, logo_y)))

        # le message de bienvenue grossit et rétrécit doucement
        scale = 1 + wave(self._time, 0.04, 1.6)
        welcome = pygame.transform.rotozoom(self._welcome, 0, scale)
        surface.blit(welcome, welcome.get_rect(center=(RIGHT_CENTER_X, 440)))
        draw_text(surface, self.app.t("splash.slogan"), self.app.fonts.get(30), SPLASH_COLORS["slogan"],
                  center=(RIGHT_CENTER_X, 500))

        if int(self._time * 2) % 2 == 0:            # clignote deux fois par seconde
            draw_text(surface, self.app.t("splash.continue"), self.app.fonts.get(26),
                      SPLASH_COLORS["hint"], center=(RIGHT_CENTER_X, 620))
