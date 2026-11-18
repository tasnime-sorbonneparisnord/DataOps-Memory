"""Style « cadre doré » des menus : panneau bleu nuit, bordure dorée, coins carrés."""

import pygame

from ui.drawing import render_outlined_text

GOLD = {
    "frame": (214, 160, 64),
    "frame_dark": (150, 98, 30),
    "frame_light": (255, 214, 120),
    "fill": (14, 30, 50),
    "stripe": (255, 255, 255, 12),
    "hover": (64, 196, 222),
    "title": (255, 206, 84),
    "outline": (20, 14, 30),
    "text": (240, 244, 255),
    "muted": (170, 186, 214),
    "badge": (64, 196, 222),
}

FRAME_WIDTH = 4
CORNER_SIZE = 12


def draw_gold_frame(surface, rect, *, hovered=False):
    """Dessine un panneau bleu nuit encadré d'or, avec des rayures et des coins carrés."""
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, GOLD["frame"], rect, border_radius=4)
    inner = rect.inflate(-2 * FRAME_WIDTH, -2 * FRAME_WIDTH)
    pygame.draw.rect(surface, GOLD["fill"], inner)

    decoration = pygame.Surface(inner.size, pygame.SRCALPHA)
    if hovered:                                   # reflet turquoise de gauche à droite
        for x in range(inner.width):
            alpha = round(210 * max(0.0, 1 - x / (inner.width * 0.75)))
            pygame.draw.line(decoration, (*GOLD["hover"], alpha), (x, 0), (x, inner.height))
    slant = inner.height // 2
    for x in range(-slant, inner.width, 90):      # rayures obliques très légères
        band = [(x, inner.height), (x + slant, 0), (x + slant + 40, 0), (x + 40, inner.height)]
        pygame.draw.polygon(decoration, GOLD["stripe"], band)
    surface.blit(decoration, inner.topleft)

    pygame.draw.line(surface, GOLD["frame_light"], rect.topleft, rect.topright, 2)
    for corner in (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright):
        square = pygame.Rect(0, 0, CORNER_SIZE, CORNER_SIZE)
        square.center = corner
        square.clamp_ip(rect)
        pygame.draw.rect(surface, GOLD["frame_dark"], square)
        pygame.draw.rect(surface, GOLD["frame_light"], square.inflate(-6, -6))
    return inner


def render_gold_title(text, font) -> pygame.Surface:
    """Titre doré avec un contour sombre, comme sur les cadres des menus."""
    return render_outlined_text(text.upper(), font, GOLD["title"], [(GOLD["outline"], 3)])


def tint_icon(icon, color) -> pygame.Surface:
    """Recolore une icône blanche (par exemple en doré)."""
    tinted = icon.copy()
    tinted.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted
