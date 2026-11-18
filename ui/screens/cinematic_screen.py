"""Cinématique d'introduction : la data engineer réveillée à 3 h du matin par une panne."""

import pygame

from ui.drawing import render_outlined_text
from ui.screens.base import Screen
from ui.settings import CINEMATIC_DIR, WINDOW_HEIGHT, WINDOW_WIDTH

CINEMATIC_FPS = 12                       # images par seconde des fichiers frame_XXX.jpg
SOUND_FILE = "cinematic.ogg"
TYPING_SPEED = 30                        # lettres affichées par seconde

# Sous-titres : (début, fin, clé du texte, couleur), en secondes
SUBTITLES = [
    (0.3, 3.2, "cinematic.calm", (255, 255, 255)),
    (3.4, 5.6, "cinematic.alert", (255, 90, 90)),
    (5.8, 9.9, "cinematic.go", (255, 206, 84)),
]
SUBTITLE_Y = WINDOW_HEIGHT - 70
OUTLINE_COLOR = (10, 10, 20)


class CinematicScreen(Screen):
    """Fait défiler les images de la vidéo comme un film, avec le son et des sous-titres.

    Les images sont chargées une par une (jamais toutes en mémoire).
    À la fin, ou si le joueur clique, on passe à on_finish avec un fondu au noir.
    """

    def __init__(self, app, on_finish):
        super().__init__(app)
        self._on_finish = on_finish
        self._frames = sorted(CINEMATIC_DIR.glob("frame_*.jpg"))
        self._sound = self._load_sound()
        self._time = 0.0
        self._started = False
        self._finished = False
        self._frame_index = -1
        self._frame_image = None

    @staticmethod
    def _load_sound():
        """Le son de la vidéo, ou None (fichier absent, pas de carte son...)."""
        try:
            return pygame.mixer.Sound(str(CINEMATIC_DIR / SOUND_FILE))
        except (pygame.error, FileNotFoundError):
            return None

    @property
    def duration(self) -> float:
        return len(self._frames) / CINEMATIC_FPS

    # ------------------------------------------------------------------
    # Boucle
    # ------------------------------------------------------------------

    def handle_event(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):     # passer la vidéo
            self._finish()

    def update(self, delta_seconds):
        if not self._started:              # le son démarre avec la première image
            self._started = True
            self.app.sound.pause_music()   # la musique d'ambiance se tait pendant la vidéo
            if self._sound is not None:
                self._sound.set_volume(self.app.sound.effects_volume)
                self._sound.play()
        self._time += delta_seconds
        if self._time >= self.duration:
            self._finish()

    def _finish(self):
        if self._finished:
            return
        self._finished = True
        if self._sound is not None:
            self._sound.fadeout(600)
        self.app.sound.resume_music()
        self.app.fade_to(self._on_finish)

    def draw(self, surface):
        surface.fill((0, 0, 0))
        frame = self._current_frame()
        if frame is not None:
            surface.blit(frame, frame.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
        self._draw_subtitle(surface)

    # ------------------------------------------------------------------
    # Images et sous-titres
    # ------------------------------------------------------------------

    def _current_frame(self):
        if not self._frames:
            return None
        index = min(int(self._time * CINEMATIC_FPS), len(self._frames) - 1)
        if index != self._frame_index:                 # nouvelle image à charger
            self._frame_index = index
            try:
                self._frame_image = pygame.image.load(str(self._frames[index])).convert()
            except pygame.error:
                pass                                   # on garde l'image précédente
        return self._frame_image

    def _draw_subtitle(self, surface):
        for start, end, key, color in SUBTITLES:
            if start <= self._time < end:
                text = self.app.t(key)
                letters = int((self._time - start) * TYPING_SPEED)   # effet machine à écrire
                shown = text[:letters]
                if shown:
                    label = render_outlined_text(shown, self.app.fonts.get(34), color,
                                                 [(OUTLINE_COLOR, 4)])
                    full_width = self.app.fonts.get(34).size(text)[0]
                    left = (WINDOW_WIDTH - full_width) // 2      # le texte ne « glisse » pas
                    surface.blit(label, label.get_rect(midleft=(left - 4, SUBTITLE_Y)))
