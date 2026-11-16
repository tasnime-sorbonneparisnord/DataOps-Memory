"""Application Pygame : la fenêtre, la boucle de jeu et le passage d'un écran à l'autre."""

import pygame

from game.memory_game import MemoryGame
from ui.drawing import FontBook, draw_vertical_gradient
from ui.screens.menu_screen import MenuScreen
from ui.settings import (COLORS, FPS, MENU_BACKGROUND_FILE, WINDOW_HEIGHT, WINDOW_TITLE,
                         WINDOW_WIDTH)


class App:
    """Crée la fenêtre, fait tourner la boucle et affiche l'écran en cours.

    La logique du jeu (MemoryGame), les incidents et les scores sont reçus de
    l'extérieur (injection de dépendances) : l'interface ne lit aucun fichier
    de données elle-même.
    """

    def __init__(self, library, scores):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        self.library = library
        self.scores = scores
        self.game = MemoryGame(library)
        self.fonts = FontBook()
        self.background = self._create_background()
        self.menu_background = self._load_menu_background()

        self._current = MenuScreen(self)
        self._running = True

    # ------------------------------------------------------------------
    # Navigation entre les écrans (appelée par les écrans eux-mêmes)
    # ------------------------------------------------------------------

    def show_menu(self):
        self._current = MenuScreen(self)

    def show_rules(self):
        print("Écran des règles : à venir")

    def start_game(self, difficulty):
        print(f"Lancement d'une partie : {difficulty.name} (écran de jeu à venir)")

    def quit(self):
        self._running = False

    # ------------------------------------------------------------------
    # Boucle de jeu
    # ------------------------------------------------------------------

    def run(self):
        while self._running:
            delta_seconds = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self._current.handle_event(event)
            self._current.update(delta_seconds)
            self._current.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    # ------------------------------------------------------------------
    # Images de fond, préparées une seule fois
    # ------------------------------------------------------------------

    def _create_background(self) -> pygame.Surface:
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        draw_vertical_gradient(background, COLORS["background_top"], COLORS["background_bottom"])
        return background

    def _load_menu_background(self) -> pygame.Surface:
        """Illustration de l'accueil si elle existe, sinon le dégradé habituel."""
        try:
            image = pygame.image.load(str(MENU_BACKGROUND_FILE)).convert()
            return pygame.transform.smoothscale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except (FileNotFoundError, pygame.error):
            return self.background