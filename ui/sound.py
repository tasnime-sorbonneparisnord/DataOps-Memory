"""Musique d'ambiance et effets sonores, avec les volumes choisis dans les paramètres."""

import pygame

from ui.settings import SOUNDS_DIR

EFFECTS = ("flip", "match", "mismatch", "coffee", "critical", "win", "lose", "click")
MUSIC_FILE = "music.ogg"


class SoundManager:
    """Joue la musique en boucle et les effets (retourner une carte, bonne paire...).

    Si l'ordinateur n'a pas de son ou qu'un fichier manque, le jeu continue
    en silence : aucune méthode ne plante.
    """

    def __init__(self, settings):
        self._settings = settings
        self._enabled = self._init_mixer()
        self._effects = self._load_effects() if self._enabled else {}
        self.apply_volumes()

    @staticmethod
    def _init_mixer() -> bool:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            return True
        except pygame.error:
            return False

    @staticmethod
    def _load_effects() -> dict:
        effects = {}
        for name in EFFECTS:
            try:
                effects[name] = pygame.mixer.Sound(str(SOUNDS_DIR / f"{name}.ogg"))
            except (pygame.error, FileNotFoundError):
                pass
        return effects

    @property
    def effects_volume(self) -> float:
        """Volume des effets entre 0 et 1 (aussi utilisé pour la vidéo)."""
        return self._settings.effects_volume / 100

    def apply_volumes(self):
        """À appeler quand un volume change dans les paramètres."""
        if not self._enabled:
            return
        pygame.mixer.music.set_volume(self._settings.music_volume / 100)
        for sound in self._effects.values():
            sound.set_volume(self.effects_volume)

    def play(self, name: str):
        sound = self._effects.get(name)
        if sound is not None:
            sound.play()

    def start_music(self):
        if not self._enabled:
            return
        try:
            pygame.mixer.music.load(str(SOUNDS_DIR / MUSIC_FILE))
            pygame.mixer.music.play(loops=-1, fade_ms=1500)
        except pygame.error:
            pass

    def pause_music(self):
        if self._enabled:
            pygame.mixer.music.pause()

    def resume_music(self):
        if self._enabled:
            pygame.mixer.music.unpause()
