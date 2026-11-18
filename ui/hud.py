"""Éléments d'affichage de la partie (HUD) : barre du joueur, panneaux de stats, boutons ronds."""

import pygame

from ui.drawing import draw_database_icon, draw_text, render_outlined_text

HUD_COLORS = {
    "panel": (176, 216, 246),
    "panel_border": (255, 255, 255),
    "panel_shadow": (40, 60, 110, 90),
    "header": (34, 52, 110),
    "box": (250, 252, 255),
    "box_border": (120, 170, 225),
    "value": (34, 52, 110),
    "danger": (232, 64, 80),
    "bar": (22, 34, 64, 215),
    "bar_text": (255, 255, 255),
    "level_pill": (64, 210, 230),
    "avatar": (92, 52, 190),
    "avatar_border": (190, 225, 225),
    "progress_back": (210, 228, 248),
    "progress": (76, 195, 106),
    "round": (150, 70, 230),
}


def _shadowed_panel(surface, rect, radius=18):
    shadow = pygame.Surface((rect.width + 8, rect.height + 8), pygame.SRCALPHA)
    pygame.draw.rect(shadow, HUD_COLORS["panel_shadow"], shadow.get_rect(), border_radius=radius)
    surface.blit(shadow, (rect.left + 2, rect.top + 5))
    pygame.draw.rect(surface, HUD_COLORS["panel"], rect, border_radius=radius)
    pygame.draw.rect(surface, HUD_COLORS["panel_border"], rect, 4, border_radius=radius)


def draw_stat_panel(surface, rect, fonts, title, value, *, value_color=None, detail=""):
    """Panneau arrondi bleu clair : un titre en haut, une grande valeur dans une case blanche."""
    rect = pygame.Rect(rect)
    _shadowed_panel(surface, rect)
    draw_text(surface, title.upper(), fonts.get(26), HUD_COLORS["header"],
              center=(rect.centerx, rect.top + 28))
    box = pygame.Rect(rect.left + 14, rect.top + 52, rect.width - 28, rect.height - 66)
    pygame.draw.rect(surface, HUD_COLORS["box"], box, border_radius=12)
    pygame.draw.rect(surface, HUD_COLORS["box_border"], box, 3, border_radius=12)
    value_y = box.centery - (10 if detail else 0)
    label = render_outlined_text(value, fonts.get(44), value_color or HUD_COLORS["value"],
                                 [(HUD_COLORS["panel_border"], 3)])
    surface.blit(label, label.get_rect(center=(box.centerx, value_y)))
    if detail:
        draw_text(surface, detail, fonts.get(18), HUD_COLORS["header"],
                  center=(box.centerx, box.bottom - 18))
    return box


def draw_player_bar(surface, topleft, fonts, pseudo, level_name):
    """Avatar carré + bandeau sombre en biseau avec le pseudo et le niveau (style profil de jeu)."""
    x, y = topleft
    avatar = pygame.Rect(x, y, 88, 88)
    pygame.draw.rect(surface, HUD_COLORS["avatar_border"], avatar, border_radius=16)
    pygame.draw.rect(surface, HUD_COLORS["avatar"], avatar.inflate(-10, -10), border_radius=12)
    draw_database_icon(surface, avatar.center, 42, HUD_COLORS["avatar_border"], HUD_COLORS["avatar"])

    bar_left, bar_top, bar_width, bar_height = avatar.right - 6, y + 14, 330, 40
    bar = pygame.Surface((bar_width + 20, bar_height), pygame.SRCALPHA)
    shape = [(0, 0), (bar_width + 20, 0), (bar_width, bar_height), (0, bar_height)]
    pygame.draw.polygon(bar, HUD_COLORS["bar"], shape)
    surface.blit(bar, (bar_left, bar_top))
    pygame.draw.rect(surface, HUD_COLORS["avatar_border"], avatar, 3, border_radius=16)

    draw_text(surface, pseudo or "Joueur", fonts.get(24), HUD_COLORS["bar_text"],
              midleft=(bar_left + 22, bar_top + bar_height // 2))
    pill_text = fonts.get(20).size(level_name)[0]
    pill = pygame.Rect(0, 0, pill_text + 28, 28)
    pill.midright = (bar_left + bar_width - 12, bar_top + bar_height // 2)
    pygame.draw.rect(surface, HUD_COLORS["level_pill"], pill, border_radius=8)
    draw_text(surface, level_name, fonts.get(20), HUD_COLORS["header"], center=pill.center)


def draw_progress_bar(surface, rect, done, total):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, HUD_COLORS["progress_back"], rect, border_radius=rect.height // 2)
    if total and done:
        filled = rect.copy()
        filled.width = max(rect.height, round(rect.width * done / total))
        pygame.draw.rect(surface, HUD_COLORS["progress"], filled, border_radius=rect.height // 2)


class RoundButton:
    """Bouton rond violet avec une icône blanche (comme le bouton réglages des jeux mobiles)."""

    def __init__(self, center, radius, icon):
        self.center = center
        self.radius = radius
        self.icon = icon

    def contains(self, position) -> bool:
        dx, dy = position[0] - self.center[0], position[1] - self.center[1]
        return dx * dx + dy * dy <= self.radius * self.radius

    def is_clicked(self, event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.contains(event.pos))

    def draw(self, surface, icons):
        hovered = self.contains(pygame.mouse.get_pos())
        radius = self.radius + (3 if hovered else 0)
        pygame.draw.circle(surface, HUD_COLORS["panel_border"], self.center, radius)
        pygame.draw.circle(surface, HUD_COLORS["round"], self.center, radius - 5)
        icon = icons.get(self.icon, radius)
        surface.blit(icon, icon.get_rect(center=self.center))


def draw_effect_badge(surface, center, fonts, icons, icon_file, text, count):
    """Rond avec une icône de carte spéciale, son effet en dessous et le nombre en pastille."""
    pygame.draw.circle(surface, HUD_COLORS["panel_border"], center, 34)
    pygame.draw.circle(surface, HUD_COLORS["round"], center, 29)
    icon = icons.get(icon_file, 34)
    surface.blit(icon, icon.get_rect(center=center))
    pastille = (center[0] + 26, center[1] + 24)
    pygame.draw.circle(surface, HUD_COLORS["header"], pastille, 14)
    draw_text(surface, str(count), fonts.get(18), HUD_COLORS["bar_text"], center=pastille)
    draw_text(surface, text, fonts.get(20), HUD_COLORS["header"], center=(center[0], center[1] + 52))
