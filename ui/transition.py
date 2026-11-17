"""Transition en fondu au noir entre deux écrans, comme à la fin d'une vidéo."""

import pygame

FADE_OUT_DURATION = 0.7     # secondes pour que l'écran devienne noir
FADE_IN_DURATION = 0.5      # secondes pour que le nouvel écran réapparaisse


class FadeTransition:
    """L'écran s'assombrit, on change d'écran dans le noir, puis il s'éclaircit.

    action est la fonction qui change d'écran (par exemple lancer la partie).
    Elle est appelée une seule fois, au moment où l'écran est complètement noir.
    """

    def __init__(self, action):
        self._action = action
        self._time = 0.0
        self._action_done = False

    @property
    def finished(self) -> bool:
        return self._time >= FADE_OUT_DURATION + FADE_IN_DURATION

    @property
    def darkness(self) -> float:
        """0 = image normale, 1 = écran complètement noir."""
        if self._time < FADE_OUT_DURATION:
            return self._time / FADE_OUT_DURATION
        return max(0.0, 1 - (self._time - FADE_OUT_DURATION) / FADE_IN_DURATION)

    def update(self, delta_seconds: float):
        self._time += delta_seconds
        if not self._action_done and self._time >= FADE_OUT_DURATION:
            self._action_done = True
            self._action()                  # changement d'écran, dans le noir

    def draw(self, surface):
        veil = pygame.Surface(surface.get_size())
        veil.fill((0, 0, 0))
        veil.set_alpha(round(255 * self.darkness))
        surface.blit(veil, (0, 0))
