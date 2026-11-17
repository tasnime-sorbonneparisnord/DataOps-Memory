"""Application Pygame : la fenêtre, la boucle de jeu et le passage d'un écran à l'autre."""

import pygame

from game.memory_game import MemoryGame
from ui.drawing import FontBook, draw_vertical_gradient
from ui.icons import IconLoader
from ui.screens.credits_screen import CreditsScreen
from ui.screens.end_screen import EndScreen
from ui.screens.game_screen import GameScreen
from ui.screens.level_intro_screen import LevelIntroScreen
from ui.screens.levels_screen import LevelsScreen
from ui.screens.menu_screen import MenuScreen
from ui.screens.pseudo_screen import PseudoScreen
from ui.screens.rules_screen import RulesScreen
from ui.screens.scores_screen import ScoresScreen
from ui.screens.settings_screen import SettingsScreen
from ui.screens.splash_screen import SplashScreen
from ui.settings import (COLORS, FPS, MENU_BACKGROUND_FILE, WINDOW_HEIGHT, WINDOW_TITLE,
                         WINDOW_WIDTH)
from ui.transition import FadeTransition


class App:
    """Crée la fenêtre, fait tourner la boucle et affiche l'écran en cours.

    La logique du jeu (MemoryGame), les incidents, les scores et le profil du
    joueur sont reçus de l'extérieur (injection de dépendances) : l'interface
    ne lit aucun fichier de données elle-même.
    """

    def __init__(self, library, scores, profile):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        self.library = library
        self.scores = scores
        self.profile = profile
        self.game = MemoryGame(library)
        self.fonts = FontBook()
        self.icons = IconLoader()
        self.background = self._create_background()
        self.menu_background = self._load_menu_background()

        self._current = SplashScreen(self)      # le jeu commence par l'écran de démarrage
        self._running = True
        self._transition = None                 # fondu au noir en cours, ou None

    # ------------------------------------------------------------------
    # Navigation entre les écrans (appelée par les écrans eux-mêmes)
    # ------------------------------------------------------------------

    def show_pseudo(self):
        self._current = PseudoScreen(self)

    def show_menu(self):
        self._current = MenuScreen(self)

    def show_levels(self):
        self._current = LevelsScreen(self)

    def show_level_intro(self, difficulty):
        self._current = LevelIntroScreen(self, difficulty)

    def show_rules(self):
        self._current = RulesScreen(self)

    def show_scores(self):
        self._current = ScoresScreen(self)

    def show_settings(self):
        self._current = SettingsScreen(self)

    def show_credits(self):
        self._current = CreditsScreen(self)

    def start_game(self, difficulty):
        self.game.start(difficulty)
        self._current = GameScreen(self)

    def show_end(self, result):
        is_record = self.scores.submit(result)
        self._current = EndScreen(self, result, is_record)

    def fade_to(self, action):
        """Assombrit l'écran, exécute action (changer d'écran) dans le noir, puis éclaircit."""
        if self._transition is None:
            self._transition = FadeTransition(action)

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
                elif self._transition is None:      # pas de clic pendant un fondu
                    self._current.handle_event(event)
            if self._transition is None:
                self._current.update(delta_seconds)
            else:                                    # l'écran est figé pendant le fondu :
                self._transition.update(delta_seconds)   # le chrono ne tourne pas encore
            self._current.draw(self.screen)
            if self._transition is not None:
                self._transition.draw(self.screen)
                if self._transition.finished:
                    self._transition = None
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
