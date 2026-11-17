"""Petites animations de l'accueil : des images qui flottent doucement."""

import math
from functools import lru_cache

import pygame

from ui.settings import IMAGES_DIR


def wave(time: float, amplitude: float, period: float, phase: float = 0.0) -> float:
    """Décalage d'une oscillation douce (sinus), entre -amplitude et +amplitude.

    period est la durée d'un aller-retour complet, en secondes.
    """
    return amplitude * math.sin(2 * math.pi * time / period + phase)


@lru_cache(maxsize=None)
def load_image(file_name: str, height: int):
    """Charge une image de assets/images à la hauteur voulue (proportions gardées).

    Renvoie None si le fichier manque : l'accueil s'affiche alors sans cette image.
    L'image n'est chargée qu'une seule fois grâce au cache.
    """
    try:
        image = pygame.image.load(str(IMAGES_DIR / file_name)).convert_alpha()
    except (FileNotFoundError, pygame.error):
        return None
    width = round(image.get_width() * height / image.get_height())
    return pygame.transform.smoothscale(image, (width, height))


class FloatingSprite:
    """Une image posée à un endroit, qui monte et descend doucement.

    Chaque sprite a sa propre amplitude, sa période et son décalage (phase),
    pour que tous les éléments ne bougent pas en même temps.
    """

    def __init__(self, image, midbottom, *, amplitude=6, period=3.0, phase=0.0):
        self.image = image
        self.midbottom = midbottom
        self.amplitude = amplitude
        self.period = period
        self.phase = phase
        self._time = 0.0

    def update(self, delta_seconds: float):
        self._time += delta_seconds

    def draw(self, surface):
        offset = wave(self._time, self.amplitude, self.period, self.phase)
        rect = self.image.get_rect(midbottom=self.midbottom)
        rect.y += round(offset)
        surface.blit(self.image, rect)
