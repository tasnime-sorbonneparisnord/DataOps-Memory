"""Chargement des icônes des cartes, avec une image par défaut si un fichier manque."""

import pygame

from ui.settings import COLORS, ICONS_DIR


class IconLoader:
    """Charge chaque icône une seule fois, à la bonne taille, et la garde en mémoire."""

    def __init__(self, folder=ICONS_DIR):
        self._folder = folder
        self._cache = {}

    def get(self, file_name: str, size: int) -> pygame.Surface:
        key = (file_name, size)
        if key not in self._cache:
            self._cache[key] = self._load(file_name, size)
        return self._cache[key]

    def _load(self, file_name: str, size: int) -> pygame.Surface:
        path = self._folder / file_name if file_name else None
        try:
            image = pygame.image.load(str(path)).convert_alpha()
            return pygame.transform.smoothscale(image, (size, size))
        except (FileNotFoundError, pygame.error, TypeError):
            return _default_icon(size)


def _default_icon(size: int) -> pygame.Surface:
    """Image de remplacement : un simple rond blanc, pour ne jamais planter."""
    icon = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(icon, COLORS["badge"], (size // 2, size // 2), size // 2 - 2, 4)
    return icon