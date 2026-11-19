"""Écran de fin : bandeau de résultat, personnage sur son socle et carte de statistiques."""

import random

import pygame

from ui.drawing import draw_text, render_outlined_text
from ui.floating_sprite import FloatingSprite, load_image
from ui.gold_style import GOLD, draw_gold_frame, render_gold_title
from ui.screens.game_screen import format_time
from ui.screens.base import Screen
from ui.section_button import SectionButton
from ui.settings import WINDOW_HEIGHT, WINDOW_WIDTH

CENTER_X = WINDOW_WIDTH // 2
BANNER_RECT = pygame.Rect(40, 28, WINDOW_WIDTH - 80, 78)
BUTTONS_TOP, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_GAP = 120, 260, 56, 20
PODIUM_X, PEDESTAL_TOP, PEDESTAL_WIDTH = 350, 600, 420     # personnage à gauche
CARD_RECT = pygame.Rect(680, 232, 560, 530)                # grande carte des scores à droite
CHARACTER_HEIGHT = 390

# Personnage selon le résultat : (image préférée, image de secours, amplitude, période)
CHARACTERS = {
    True: ("end_happy.png", "character_laptop_top.png", 14, 0.8),    # il saute de joie
    False: ("end_sad.png", "character_laptop_top.png", 3, 3.0),      # il bouge à peine
}
END_COLORS = {
    "banner_left": (34, 40, 96),
    "banner_right": (86, 96, 170),
    "veil": (20, 24, 60, 60),
    "pedestal": (78, 88, 140),
    "pedestal_dark": (52, 60, 104),
    "pedestal_rim": (120, 132, 190),
    "glow": (64, 210, 240),
    "win": (255, 206, 84),
    "lose": (232, 84, 96),
    "stat_title": (64, 210, 240),
    "outline": (14, 16, 40),
}
TEXT_OUTLINE = [(END_COLORS["outline"], 3)]       # contour bleu foncé de 3 pixels autour du texte
CONFETTI_COLORS = [(255, 206, 84), (64, 210, 240), (232, 84, 96), (120, 220, 120), (180, 120, 255)]
CONFETTI_COUNT = 70


class EndScreen(Screen):
    """Affiche le résultat d'une partie terminée, façon podium de jeu vidéo.

    R : rejouer le même niveau · N : choisir un autre niveau · Échap : accueil.
    """

    def __init__(self, app, result, is_record: bool):
        super().__init__(app)
        self._result = result
        self._is_record = is_record
        self._time = 0.0
        self._background = self._create_background()
        self._buttons = self._create_buttons()
        self._character = self._create_character()
        self._confetti = self._create_confetti() if result.won else []
        app.sound.play("win" if result.won else "lose")

    # ------------------------------------------------------------------
    # Préparation
    # ------------------------------------------------------------------

    def _create_background(self) -> pygame.Surface:
        background = self.app.menu_background.copy()
        veil = pygame.Surface(background.get_size(), pygame.SRCALPHA)
        veil.fill(END_COLORS["veil"])
        background.blit(veil, (0, 0))
        return background

    def _create_buttons(self) -> list:
        """Liste de (bouton, touche, action)."""
        actions = [
            (self.app.t("end.replay"), "menu_play.png", pygame.K_r,
             lambda: self.app.fade_to(self.app.replay)),
            (self.app.t("end.levels"), "menu_rules.png", pygame.K_n, self.app.show_levels),
            (self.app.t("end.home"), "menu_back.png", pygame.K_ESCAPE, self.app.show_menu),
        ]
        buttons = []
        first_left = CENTER_X - (3 * BUTTON_WIDTH + 2 * BUTTON_GAP) // 2
        for number, (title, icon, key, action) in enumerate(actions):
            left = first_left + number * (BUTTON_WIDTH + BUTTON_GAP)
            button = SectionButton((left, BUTTONS_TOP, BUTTON_WIDTH, BUTTON_HEIGHT), title,
                                   icon=icon, title_size=28)
            buttons.append((button, key, action))
        return buttons

    def _create_character(self):
        preferred, fallback, amplitude, period = CHARACTERS[self._result.won]
        image = load_image(preferred, CHARACTER_HEIGHT) or load_image(fallback, CHARACTER_HEIGHT)
        if image is None:
            return None
        return FloatingSprite(image, (PODIUM_X, PEDESTAL_TOP + 14), amplitude=amplitude,
                              period=period)

    @staticmethod
    def _create_confetti() -> list:
        """Confettis : [x, y, vitesse de chute, couleur, taille]."""
        rng = random.Random()
        return [[rng.uniform(0, WINDOW_WIDTH), rng.uniform(-WINDOW_HEIGHT, 0),
                 rng.uniform(90, 200), rng.choice(CONFETTI_COLORS), rng.randint(6, 12)]
                for _ in range(CONFETTI_COUNT)]

    # ------------------------------------------------------------------
    # Boucle
    # ------------------------------------------------------------------

    def handle_event(self, event):
        for button, key, action in self._buttons:
            pressed = event.type == pygame.KEYDOWN and event.key == key
            if pressed or button.is_clicked(event):
                action()
                return

    def update(self, delta_seconds):
        self._time += delta_seconds
        if self._character is not None:
            self._character.update(delta_seconds)
        for piece in self._confetti:                # les confettis tombent puis recommencent
            piece[1] += piece[2] * delta_seconds
            if piece[1] > WINDOW_HEIGHT:
                piece[1] = -20

    def draw(self, surface):
        surface.blit(self._background, (0, 0))
        self._draw_banner(surface)
        for button, _, _ in self._buttons:
            button.draw(surface, self.app.fonts, self.app.icons)
        self._draw_pedestal(surface)
        if self._character is not None:
            self._character.draw(surface)
        self._draw_stats_card(surface)
        for x, y, _, color, size in self._confetti:
            pygame.draw.rect(surface, color, (x, y, size, size // 2 + 2))

    # ------------------------------------------------------------------
    # Dessin des parties
    # ------------------------------------------------------------------

    def _title(self) -> str:
        pseudo = self.app.profile.pseudo or self.app.t("end.default_player")
        return self.app.t("end.win", pseudo=pseudo) if self._result.won else self.app.t("end.lose")

    def _draw_banner(self, surface):
        banner = pygame.Surface(BANNER_RECT.size)
        left, right = END_COLORS["banner_left"], END_COLORS["banner_right"]
        for x in range(BANNER_RECT.width):          # dégradé horizontal
            ratio = abs(x / BANNER_RECT.width - 0.5) * 2
            color = [round(a + (b - a) * ratio) for a, b in zip(left, right)]
            pygame.draw.line(banner, color, (x, 0), (x, BANNER_RECT.height))
        surface.blit(banner, BANNER_RECT)
        title = render_outlined_text(self._title().upper(), self.app.fonts.get(48),
                                     (255, 255, 255), TEXT_OUTLINE)
        surface.blit(title, title.get_rect(center=BANNER_RECT.center))

    def _draw_pedestal(self, surface):
        column = pygame.Rect(0, PEDESTAL_TOP, PEDESTAL_WIDTH - 40, WINDOW_HEIGHT - PEDESTAL_TOP)
        column.centerx = PODIUM_X
        pygame.draw.rect(surface, END_COLORS["pedestal_dark"], column)
        pygame.draw.rect(surface, END_COLORS["pedestal"], column.inflate(-30, 0))
        top = pygame.Rect(0, 0, PEDESTAL_WIDTH, 70)
        top.center = (PODIUM_X, PEDESTAL_TOP)
        pygame.draw.ellipse(surface, END_COLORS["pedestal_dark"], top.move(0, 10))
        pygame.draw.ellipse(surface, END_COLORS["pedestal_rim"], top)
        glow = top.inflate(-60, -24)
        pygame.draw.ellipse(surface, END_COLORS["glow"], glow)
        pygame.draw.ellipse(surface, (255, 255, 255), glow, 3)

    def _draw_stats_card(self, surface):
        """La grande carte des scores : ruban, joueur, statistiques et record."""
        inner = draw_gold_frame(surface, CARD_RECT)
        self._draw_ribbon(surface)
        self._draw_player(surface, inner)
        self._draw_stat_rows(surface, inner)
        self._draw_record(surface, inner)

    def _draw_ribbon(self, surface):
        """Le ruban « VICTOIRE » ou « DÉFAITE » posé sur le haut de la carte."""
        won = self._result.won
        text = self.app.t("end.victory" if won else "end.defeat").upper()
        ribbon = render_outlined_text(text, self.app.fonts.get(36),
                                      END_COLORS["win" if won else "lose"], TEXT_OUTLINE)
        anchor = (CARD_RECT.centerx, CARD_RECT.top + 18)
        ribbon_box = ribbon.get_rect(midbottom=anchor).inflate(50, 12)
        draw_gold_frame(surface, ribbon_box)
        surface.blit(ribbon, ribbon.get_rect(center=ribbon_box.center))

    def _draw_player(self, surface, inner):
        """Le pseudo, le niveau joué et un trait de séparation."""
        fonts = self.app.fonts
        pseudo = self.app.profile.pseudo or self.app.t("common.player")
        name = render_gold_title(pseudo, fonts.get(40))
        surface.blit(name, name.get_rect(midleft=(inner.left + 26, inner.top + 58)))
        level = self.app.t("level.title", name=self.app.t.level_name(self._result.difficulty))
        draw_text(surface, level.upper(), fonts.get(22), END_COLORS["stat_title"],
                  midleft=(inner.left + 28, inner.top + 96))
        pygame.draw.line(surface, GOLD["frame"], (inner.left + 20, inner.top + 120),
                         (inner.right - 20, inner.top + 120), 2)

    def _draw_stat_rows(self, surface, inner):
        """Une ligne par statistique : le titre à gauche, la valeur à droite."""
        fonts = self.app.fonts
        for row, (label, value) in enumerate(self._stats()):
            y = inner.top + 165 + row * 72
            draw_text(surface, label.upper(), fonts.get(28), END_COLORS["stat_title"],
                      midleft=(inner.left + 28, y))
            value_image = render_outlined_text(value, fonts.get(48), GOLD["text"], TEXT_OUTLINE)
            surface.blit(value_image, value_image.get_rect(midright=(inner.right - 28, y)))

    def _draw_record(self, surface, inner):
        """« Nouveau record ! » qui clignote en bas de la carte."""
        if self._is_record and int(self._time * 2) % 2 == 0:
            draw_text(surface, self.app.t("end.new_record"), self.app.fonts.get(32),
                      END_COLORS["win"], center=(inner.centerx, inner.bottom - 28))

    def _stats(self) -> list:
        """Les lignes de la carte : (titre, valeur)."""
        result, game = self._result, self.app.game
        best = self.app.scores.get_best(result.difficulty)
        t = self.app.t
        record_label = t("end.record_with", count=best.attempts) if best else t("end.record")
        record = f"{best.time_left} s" if best else "—"
        return [
            (t("end.time_left"), format_time(result.time_left)),
            (t("end.attempts"), str(result.attempts)),
            (t("end.fixed"), f"{game.resolved_count} / {game.level.incident_count}"),
            (record_label, record),
        ]
