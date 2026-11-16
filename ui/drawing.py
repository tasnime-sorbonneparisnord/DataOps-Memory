"""Petites fonctions de dessin réutilisées par tous les écrans (DRY)."""

import pygame

from ui.settings import COLORS, CORNER_RADIUS, FONT_NAMES


class FontBook:
    """Charge chaque police une seule fois et la garde en mémoire."""

    def __init__(self, names: str = FONT_NAMES):
        self._names = names
        self._cache = {}

    def get(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in self._cache:
            self._cache[key] = pygame.font.SysFont(self._names, size, bold=bold)
        return self._cache[key]


def draw_vertical_gradient(surface, top_color, bottom_color):
    """Remplit la surface avec un dégradé vertical."""
    width, height = surface.get_size()
    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = [round(a + (b - a) * ratio) for a, b in zip(top_color, bottom_color)]
        pygame.draw.line(surface, color, (0, y), (width, y))


def draw_panel(surface, rect, fill=None, border=None, radius=CORNER_RADIUS, width=2):
    """Dessine un rectangle arrondi avec une bordure."""
    pygame.draw.rect(surface, fill or COLORS["panel"], rect, border_radius=radius)
    pygame.draw.rect(surface, border or COLORS["panel_border"], rect, width, border_radius=radius)


def draw_text(surface, text, font, color, *, center=None, topleft=None, midleft=None):
    """Écrit un texte, positionné par son centre, son coin haut gauche ou son milieu gauche."""
    image = font.render(text, True, color)
    rect = image.get_rect()
    if center is not None:
        rect.center = center
    elif midleft is not None:
        rect.midleft = midleft
    else:
        rect.topleft = topleft or (0, 0)
    surface.blit(image, rect)
    return rect


def wrap_text(text: str, font, max_width: int) -> list:
    """Coupe un texte en plusieurs lignes pour qu'il tienne dans max_width pixels."""
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if font.size(candidate)[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped_text(surface, text, font, color, rect, line_spacing=4):
    """Écrit un texte sur plusieurs lignes, centré dans rect."""
    lines = wrap_text(text, font, rect.width)
    line_height = font.get_linesize() + line_spacing
    top = rect.centery - (len(lines) * line_height - line_spacing) / 2
    for number, line in enumerate(lines):
        draw_text(surface, line, font, color,
                  center=(rect.centerx, top + number * line_height + line_height / 2))


def draw_database_icon(surface, center, size, color, background):
    """Dessine l'icône « base de données » (un cylindre en trois parties), sans fichier image."""
    cx, cy = center
    width, disk = size, size * 0.3
    body = pygame.Rect(0, 0, width, size * 0.75)
    body.center = (cx, cy)
    top_disk = pygame.Rect(0, 0, width, disk)
    top_disk.center = body.midtop
    bottom_disk = pygame.Rect(0, 0, width, disk)
    bottom_disk.center = body.midbottom

    pygame.draw.ellipse(surface, color, bottom_disk)
    pygame.draw.rect(surface, color, body)
    line = max(2, size // 16)
    for ratio in (1 / 3, 2 / 3):  # deux lignes de séparation sur le corps du cylindre
        band = top_disk.move(0, body.height * ratio)
        pygame.draw.arc(surface, background, band, 3.3, 6.1, line)
    pygame.draw.ellipse(surface, background, top_disk.inflate(-line * 2, -line * 2))
    pygame.draw.ellipse(surface, color, top_disk, line)