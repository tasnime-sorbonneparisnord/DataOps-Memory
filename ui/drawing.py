"""Petites fonctions de dessin réutilisées par tous les écrans (DRY)."""

import pygame

from ui.settings import COLORS, CORNER_RADIUS, DISPLAY_FONT_FILE, FONT_NAMES


class FontBook:
    """Charge chaque police une seule fois et la garde en mémoire.

    Tout le jeu utilise la police Luckiest Guy (assets/fonts). Si le fichier
    manque, on prend une police du système pour ne pas planter.
    """

    def __init__(self, font_file=DISPLAY_FONT_FILE, fallback_names: str = FONT_NAMES):
        self._font_file = font_file
        self._fallback_names = fallback_names
        self._cache = {}

    def get(self, size: int, bold: bool = False) -> pygame.font.Font:
        """Police à la taille voulue (bold ne sert que pour la police de secours)."""
        key = (size, bold)
        if key not in self._cache:
            try:
                self._cache[key] = pygame.font.Font(str(self._font_file), size)
            except (FileNotFoundError, OSError):
                self._cache[key] = pygame.font.SysFont(self._fallback_names, size, bold=bold)
        return self._cache[key]

    def display(self, size: int) -> pygame.font.Font:
        """Police des grands titres (la même, gardée pour la lisibilité du code)."""
        return self.get(size, bold=True)


def line_height(font) -> int:
    """Hauteur d'une ligne de texte, la même que le texte ait des accents ou non."""
    return max(font.get_height(), font.size("ÉÀÇgjpy")[1])


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
    """Écrit un texte, positionné par son centre, son coin haut gauche ou son milieu gauche.

    Avec Luckiest Guy, l'image d'un texte est plus haute quand il y a des
    accents (É, À...). On place donc le texte dans une « boîte » de hauteur
    fixe, alignée en bas : toutes les lignes restent sur la même ligne de base.
    """
    image = font.render(text, True, color)
    rect = pygame.Rect(0, 0, image.get_width(), line_height(font))
    if center is not None:
        rect.center = center
    elif midleft is not None:
        rect.midleft = midleft
    else:
        rect.topleft = topleft or (0, 0)
    surface.blit(image, (rect.left, rect.bottom - image.get_height()))
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


def render_outlined_text(text, font, color, outlines) -> pygame.Surface:
    """Texte avec un ou plusieurs contours épais, comme un logo de jeu.

    outlines est une liste de (couleur, épaisseur), du contour extérieur
    vers l'intérieur. Exemple : [(blanc, 12), (noir, 7)].
    """
    margin = max((width for _, width in outlines), default=0)
    fill = font.render(text, True, color)
    surface = pygame.Surface((fill.get_width() + 2 * margin, fill.get_height() + 2 * margin),
                             pygame.SRCALPHA)
    for outline_color, width in outlines:
        outline = font.render(text, True, outline_color)
        for dx in range(-width, width + 1, 2):        # on décale le texte tout autour
            for dy in range(-width, width + 1, 2):
                if dx * dx + dy * dy <= width * width:
                    surface.blit(outline, (margin + dx, margin + dy))
    surface.blit(fill, (margin, margin))
    return surface


def draw_wrapped_text(surface, text, font, color, rect, line_spacing=4):
    """Écrit un texte sur plusieurs lignes, centré dans rect."""
    lines = wrap_text(text, font, rect.width)
    step = line_height(font) + line_spacing
    top = rect.centery - (len(lines) * step - line_spacing) / 2
    for number, line in enumerate(lines):
        draw_text(surface, line, font, color,
                  center=(rect.centerx, top + number * step + step / 2))


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
