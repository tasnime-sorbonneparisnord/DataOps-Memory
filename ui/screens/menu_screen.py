"""Écran d'accueil animé : le logo, les personnages et les grandes sections du jeu."""

import pygame

from ui.drawing import draw_database_icon, draw_text
from ui.floating_sprite import FloatingSprite, load_image, wave
from ui.gold_style import draw_gold_frame, render_gold_title
from ui.screens.base import Screen
from ui.section_button import SectionButton
from ui.settings import COLORS, WINDOW_WIDTH

CENTER_X = WINDOW_WIDTH // 2

# Sections du menu, empilées au centre : (titre, sous-titre au survol, icône, action)
SECTIONS = [
    ("Jouer", "Choisis ton niveau et sauve la prod", "menu_play.png", "show_levels"),
    ("Comment jouer", "Les règles en une minute", "menu_rules.png", "show_rules"),
    ("Meilleurs scores", "Tes records pour chaque niveau", "menu_scores.png", "show_scores"),
    ("Paramètres", "Volume, luminosité et langue", "menu_settings.png", "show_settings"),
    ("Crédits", "L'équipe et les sources du jeu", "menu_credits.png", "show_credits"),
    ("Quitter", "À bientôt, d'astreinte !", "menu_quit.png", "quit"),
]
SECTION_WIDTH, SECTION_HEIGHT, SECTION_GAP = 420, 62, 10
FIRST_SECTION_TOP = 192

# Personnages : (fichier, hauteur affichée, position du bas, amplitude, période)
CHARACTERS = [
    ("character_laptop_top.png", 215, (205, 475), 10, 3.4),
    ("character_coder_left.png", 230, (300, 785), 4, 2.6),
    ("character_designer_lying.png", 130, (CENTER_X, 790), 3, 3.0),
    ("character_team_right.png", 320, (1105, 790), 4, 2.8),
]

# Icônes qui flottent autour des boutons : (fichier, centre, période)
FLOATING_ICONS = [
    ("cloud_solution.png", (365, 250), 3.2),
    ("database_solution.png", (915, 250), 2.7),
    ("network_solution.png", (360, 450), 2.9),
    ("pipeline_solution.png", (920, 450), 3.5),
]
ICON_BUBBLE_SIZE = 58


class MenuScreen(Screen):
    """Affiche le logo et un bouton par section (jouer, règles, scores, paramètres...).

    Chaque section appelle une méthode de l'application (show_levels, show_rules...).
    Les personnages, les icônes et le logo flottent doucement grâce à update(dt).
    """

    def __init__(self, app):
        super().__init__(app)
        self._time = 0.0
        self._sections = self._create_sections()
        self._sprites = self._create_characters() + self._create_floating_icons()
        self._logo = load_image("logo.png", 165)      # None si l'image manque

    # ------------------------------------------------------------------
    # Création des éléments
    # ------------------------------------------------------------------

    def _create_sections(self) -> list:
        """Liste de (bouton, action) ; l'action est le nom d'une méthode de App."""
        left = CENTER_X - SECTION_WIDTH // 2
        sections = []
        for position, (title, subtitle, icon, action) in enumerate(SECTIONS):
            top = FIRST_SECTION_TOP + position * (SECTION_HEIGHT + SECTION_GAP)
            button = SectionButton((left, top, SECTION_WIDTH, SECTION_HEIGHT), title,
                                   subtitle=subtitle, icon=icon, title_size=32)
            sections.append((button, action))
        return sections

    def _create_characters(self) -> list:
        sprites = []
        for index, (file_name, height, midbottom, amplitude, period) in enumerate(CHARACTERS):
            image = load_image(file_name, height)
            if image is not None:      # image absente : on l'ignore, sans planter
                sprites.append(FloatingSprite(image, midbottom, amplitude=amplitude,
                                              period=period, phase=index))
        return sprites

    def _create_floating_icons(self) -> list:
        sprites = []
        for index, (file_name, center, period) in enumerate(FLOATING_ICONS):
            bubble = self._icon_bubble(file_name)
            midbottom = (center[0], center[1] + ICON_BUBBLE_SIZE // 2)
            sprites.append(FloatingSprite(bubble, midbottom, amplitude=8,
                                          period=period, phase=index * 1.3))
        return sprites

    def _icon_bubble(self, file_name: str) -> pygame.Surface:
        """Une icône blanche dans un rond violet, pour qu'elle se voie sur le fond clair."""
        size = ICON_BUBBLE_SIZE
        bubble = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(bubble, COLORS["card_back"], (size // 2, size // 2), size // 2)
        icon = self.app.icons.get(file_name, size - 22)
        bubble.blit(icon, icon.get_rect(center=(size // 2, size // 2)))
        return bubble

    # ------------------------------------------------------------------
    # Boucle : événements, animation, dessin
    # ------------------------------------------------------------------

    def handle_event(self, event):
        for button, action in self._sections:
            if button.is_clicked(event):
                getattr(self.app, action)()        # ex. self.app.show_levels()
                return

    def update(self, delta_seconds):
        self._time += delta_seconds
        for sprite in self._sprites:
            sprite.update(delta_seconds)

    def draw(self, surface):
        surface.blit(self.app.menu_background, (0, 0))
        for sprite in self._sprites:
            sprite.draw(surface)
        self._draw_texts(surface)
        self._draw_player(surface)
        for button, _ in self._sections:
            button.draw(surface, self.app.fonts, self.app.icons)

    def _draw_player(self, surface):
        """Pseudo du joueur en haut à droite, dans un petit cadre doré."""
        pseudo = self.app.profile.pseudo
        if not pseudo:
            return
        label = render_gold_title(f"Salut, {pseudo} !", self.app.fonts.get(24))
        frame = label.get_rect().inflate(36, 22)
        frame.topright = (WINDOW_WIDTH - 24, 22)
        draw_gold_frame(surface, frame)
        surface.blit(label, label.get_rect(center=frame.center))

    def _draw_texts(self, surface):
        fonts = self.app.fonts
        offset = round(wave(self._time, 6, 3.0))          # le titre flotte
        if self._logo is not None:
            surface.blit(self._logo, self._logo.get_rect(center=(CENTER_X, 92 + offset)))
        else:                                              # logo absent : titre en texte
            title = draw_text(surface, "DataOps Memory", fonts.get(68, bold=True),
                              COLORS["title"], center=(CENTER_X + 45, 105 + offset))
            draw_database_icon(surface, (title.left - 55, title.centery), 70, COLORS["title"],
                               COLORS["background_top"])


