"""Application Pygame : la fenêtre, la boucle de jeu et le passage d'un écran à l'autre."""

import pygame

from game.memory_game import MemoryGame
from ui.drawing import FontBook, draw_vertical_gradient
from ui.i18n import Translator
from ui.icons import IconLoader
from ui.screens.cinematic_screen import CinematicScreen
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
from ui.sound import SoundManager
from ui.transition import FadeTransition


class App:
    """Crée la fenêtre, fait tourner la boucle et affiche l'écran en cours.

    La logique du jeu (MemoryGame), les incidents, les scores, le profil du
    joueur et ses paramètres sont reçus de l'extérieur (injection de
    dépendances) : l'interface ne lit aucun fichier de données elle-même.

    libraries associe une langue à sa bibliothèque d'incidents : {"fr": ..., "en": ...}.
    """

    def __init__(self, libraries, scores, profile, settings):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        self.libraries = libraries
        self.scores = scores
        self.profile = profile
        self.settings = settings
        self.t = Translator(settings)            # self.app.t("clé") donne le texte traduit
        self.sound = SoundManager(settings)
        self._game_library = self.library
        self.game = MemoryGame(self._game_library)
        self.fonts = FontBook()
        self.icons = IconLoader()
        self.background = self._create_background()
        self.menu_background = self._load_menu_background()

        self._current = SplashScreen(self)      # le jeu commence par l'écran de démarrage
        self._running = True
        self._transition = None                 # fondu au noir en cours, ou None
        self._brightness_veil = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    # ------------------------------------------------------------------
    # Navigation entre les écrans (appelée par les écrans eux-mêmes)
    # ------------------------------------------------------------------

    @property
    def library(self):
        """Les incidents dans la langue choisie (en français si la langue n'existe pas)."""
        return self.libraries.get(self.settings.language, self.libraries["fr"])

    def show_pseudo(self):
        self._current = PseudoScreen(self)

    def show_menu(self):
        self._current = MenuScreen(self)

    def show_levels(self):
        self._current = LevelsScreen(self)

    def show_level_intro(self, difficulty):
        self._current = LevelIntroScreen(self, difficulty)

    def show_cinematic(self, difficulty):
        """La vidéo d'introduction, puis la partie du niveau choisi."""
        self._current = CinematicScreen(self, on_finish=lambda: self.start_game(difficulty))

    def show_rules(self):
        self._current = RulesScreen(self)

    def show_scores(self):
        self._current = ScoresScreen(self)

    def show_settings(self):
        self._current = SettingsScreen(self)

    def show_credits(self):
        self._current = CreditsScreen(self)

    def start_game(self, difficulty):
        self._game_library = self.library        # incidents dans la langue du moment
        self.game = MemoryGame(self._game_library)
        self.game.start(difficulty)
        self._current = GameScreen(self)

    def replay(self):
        """Rejouer le même niveau : game.restart(), sauf si la langue a changé entre-temps."""
        if self._game_library is not self.library:
            self.start_game(self.game.difficulty)
            return
        self.game.restart()
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
        self.sound.start_music()
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
            self._apply_brightness(self.screen)
            if self._transition is not None:
                self._transition.draw(self.screen)
                if self._transition.finished:
                    self._transition = None
            pygame.display.flip()
        pygame.quit()

    def _apply_brightness(self, surface):
        """Voile noir (plus sombre) ou blanc (plus clair) selon le réglage de luminosité."""
        level = self.settings.brightness              # 50 = normal
        if level == 50:
            return
        color = (0, 0, 0) if level < 50 else (255, 255, 255)
        alpha = round(abs(level - 50) * (4 if level < 50 else 2))   # max 200 / 100
        self._brightness_veil.fill(color)
        self._brightness_veil.set_alpha(alpha)
        surface.blit(self._brightness_veil, (0, 0))

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
