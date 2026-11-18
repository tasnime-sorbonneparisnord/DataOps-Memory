"""Écran de jeu : la grille au centre, le temps, les essais et le record à gauche, la mission à droite."""

import math

import pygame

from game.enums import SelectionOutcome
from ui.card_renderer import CardRenderer
from ui.drawing import draw_panel, draw_text, wrap_text
from ui.effects import MatchEffect
from ui.grid_layout import GridLayout
from ui.hud import (HUD_COLORS, RoundButton, draw_effect_badge, draw_player_bar,
                    draw_progress_bar, draw_stat_panel)
from ui.screens.base import Screen
from ui.settings import (COLORS, END_DELAY, MESSAGE_DURATION, MISMATCH_DELAY,
                         SPECIAL_FLASH_DURATION, WINDOW_WIDTH)

LOW_TIME_SECONDS = 10
EXPLANATION_DURATION = 3.5          # temps d'affichage de l'explication après une paire

# Disposition : colonne de gauche, grille au centre, colonne de droite
LEFT_X, COLUMN_WIDTH = 24, 220
STAT_PANELS_TOP, STAT_PANEL_HEIGHT, STAT_PANEL_GAP = 130, 132, 16
GRID_AREA = pygame.Rect(276, 124, 724, 652)
RIGHT_X = 1032
MISSION_RECT = pygame.Rect(RIGHT_X, 130, COLUMN_WIDTH, 250)
BOARD_COLORS = {"frame": (58, 36, 92), "border": (130, 92, 190), "slot": (40, 26, 66)}
BACKGROUND_VEIL = (20, 30, 70, 70)
TOAST_CENTER_X, TOAST_TOP, TOAST_TEXT_WIDTH = 805, 14, 560   # message en haut, sans cacher les cartes


def format_time(seconds: float) -> str:
    """Transforme un nombre de secondes en texte « mm:ss »."""
    total = max(0, math.ceil(seconds))
    return f"{total // 60:02d}:{total % 60:02d}"


class GameScreen(Screen):
    """Transmet les clics à MemoryGame et affiche l'état de la partie.

    Cet écran n'applique aucune règle du jeu : il se contente de demander
    à MemoryGame ce qui se passe, puis de l'afficher.
    """

    def __init__(self, app):
        super().__init__(app)
        self.game = app.game
        self._renderer = CardRenderer(app.fonts, app.icons)
        self._layout = GridLayout(GRID_AREA, self.game.level.rows, self.game.level.columns)
        cards = [self._layout.rect_of(i) for i in range(len(self.game.board.get_cards()))]
        self._grid_frame = cards[0].unionall(cards).inflate(36, 36)     # cadre ajusté aux cartes
        self._home_button = RoundButton((WINDOW_WIDTH - 60, 62), 34, "menu_back.png")
        self._background = self._create_background()

        self._mismatch_timer = None
        self._end_timer = None
        self._flashing = {}          # numéro de carte -> temps d'affichage restant
        self._message = None         # (titre, couleur, temps restant, détail)
        self._match_effects = []     # animations des paires trouvées en cours
        self._reactions = {
            SelectionOutcome.MATCH: self._on_match,
            SelectionOutcome.MISMATCH: self._on_mismatch,
            SelectionOutcome.SPECIAL_ACTIVATED: self._on_special,
        }

    # ------------------------------------------------------------------
    # Événements
    # ------------------------------------------------------------------

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.show_menu()
        elif self._home_button.is_clicked(event):
            self.app.show_menu()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._on_click(event.pos)

    def _on_click(self, position):
        index = self._layout.index_at(position)
        if index is None or self.game.is_over():
            return
        outcome = self.game.select_card(index)
        if outcome != SelectionOutcome.REJECTED:
            self.app.sound.play("flip")
        reaction = self._reactions.get(outcome)
        if reaction:
            reaction(index)

    def _on_match(self, index):
        self.app.sound.play("match")
        pair = self._pair_indices(index)
        self._match_effects.append(MatchEffect(pair, [self._layout.rect_of(i) for i in pair]))
        self._show_message(self.app.t("game.fixed"), COLORS["success"],
                           detail=self.game.last_explanation, duration=EXPLANATION_DURATION)

    def _pair_indices(self, index) -> list:
        """La carte cliquée et sa partenaire (même identifiant de paire)."""
        cards = self.game.board.get_cards()
        pair_id = getattr(cards[index], "pair_id", None)
        return [i for i, card in enumerate(cards) if getattr(card, "pair_id", None) == pair_id]

    def _on_mismatch(self, index):
        self.app.sound.play("mismatch")
        self._mismatch_timer = MISMATCH_DELAY

    def _on_special(self, index):
        seconds = self.game.board.get_card_at(index).activate().seconds_delta
        self._flashing[index] = SPECIAL_FLASH_DURATION
        self.app.sound.play("coffee" if seconds > 0 else "critical")
        if seconds > 0:
            self._show_message(self.app.t("game.coffee", seconds=seconds), COLORS["success"])
        else:
            self._show_message(self.app.t("game.critical", seconds=-seconds), COLORS["danger"])

    def _show_message(self, text, color, detail="", duration=MESSAGE_DURATION):
        self._message = (text, color, duration, detail)

    # ------------------------------------------------------------------
    # Temps
    # ------------------------------------------------------------------

    def update(self, delta_seconds: float):
        self.game.update(delta_seconds)
        self._update_mismatch(delta_seconds)
        self._update_flashing(delta_seconds)
        self._update_message(delta_seconds)
        self._update_match_effects(delta_seconds)
        self._update_end(delta_seconds)

    def _update_mismatch(self, delta_seconds):
        if self._mismatch_timer is None:
            return
        self._mismatch_timer -= delta_seconds
        if self._mismatch_timer <= 0:
            self.game.resolve_mismatch()
            self._mismatch_timer = None

    def _update_flashing(self, delta_seconds):
        self._flashing = {index: remaining - delta_seconds
                          for index, remaining in self._flashing.items()
                          if remaining - delta_seconds > 0}

    def _update_message(self, delta_seconds):
        if self._message:
            text, color, remaining, detail = self._message
            remaining -= delta_seconds
            self._message = (text, color, remaining, detail) if remaining > 0 else None

    def _update_match_effects(self, delta_seconds):
        for effect in self._match_effects:
            effect.update(delta_seconds)
        self._match_effects = [effect for effect in self._match_effects if not effect.finished]

    def _update_end(self, delta_seconds):
        if not self.game.is_over():
            return
        if self._end_timer is None:
            self._end_timer = END_DELAY
        self._end_timer -= delta_seconds
        if self._end_timer <= 0:
            self.app.show_end(self.game.result())

    # ------------------------------------------------------------------
    # Dessin
    # ------------------------------------------------------------------

    def _create_background(self) -> pygame.Surface:
        background = self.app.menu_background.copy()
        veil = pygame.Surface(background.get_size(), pygame.SRCALPHA)
        veil.fill(BACKGROUND_VEIL)
        background.blit(veil, (0, 0))
        return background

    def draw(self, surface):
        surface.blit(self._background, (0, 0))
        self._draw_left_column(surface)
        self._draw_board(surface)
        self._draw_right_column(surface)
        self._home_button.draw(surface, self.app.icons)
        self._draw_message(surface)

    def _draw_left_column(self, surface):
        fonts = self.app.fonts
        t = self.app.t
        level_name = t("level.title", name=t.level_name(self.game.difficulty))
        draw_player_bar(surface, (LEFT_X, 18), fonts,
                        self.app.profile.pseudo or t("common.player"), level_name)

        best = self.app.scores.get_best(self.game.difficulty)
        panels = [
            (t("game.time"), format_time(self.game.remaining_time), self._time_color(), ""),
            (t("game.attempts"), str(self.game.attempts), None, ""),
            (t("game.record"), f"{best.time_left} s" if best else "—", None,
             t("game.record_detail", count=best.attempts) if best else t("game.to_beat")),
        ]
        for number, (title, value, color, detail) in enumerate(panels):
            top = STAT_PANELS_TOP + number * (STAT_PANEL_HEIGHT + STAT_PANEL_GAP)
            draw_stat_panel(surface, (LEFT_X, top, COLUMN_WIDTH, STAT_PANEL_HEIGHT), fonts,
                            title, value, value_color=color, detail=detail)

    def _time_color(self):
        low = self.game.remaining_time <= LOW_TIME_SECONDS
        return HUD_COLORS["danger"] if low else None

    def _draw_board(self, surface):
        pygame.draw.rect(surface, BOARD_COLORS["frame"], self._grid_frame, border_radius=20)
        pygame.draw.rect(surface, BOARD_COLORS["border"], self._grid_frame, 5, border_radius=20)
        animated = {}                                  # numéro de carte -> son animation
        for effect in self._match_effects:
            animated.update({index: effect for index in effect.indices})
        for index, card in enumerate(self.game.board.get_cards()):
            rect = self._layout.rect_of(index)
            pygame.draw.rect(surface, BOARD_COLORS["slot"], rect.inflate(6, 6), border_radius=14)
            if index not in animated:
                self._renderer.draw(surface, card, rect, force_face=index in self._flashing)
        for index, effect in animated.items():        # dessinées en dernier : au-dessus des autres
            effect.draw_card(surface, self._card_image(index), self._layout.rect_of(index))
        for effect in self._match_effects:
            effect.draw_particles(surface)

    def _card_image(self, index) -> pygame.Surface:
        """La face de la carte dessinée sur une image à part, pour pouvoir l'agrandir."""
        rect = self._layout.rect_of(index)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        self._renderer.draw(image, self.game.board.get_card_at(index), image.get_rect(),
                            force_face=True)
        return image

    def _draw_right_column(self, surface):
        fonts, level = self.app.fonts, self.game.level
        draw_stat_panel(surface, MISSION_RECT, fonts, self.app.t("game.mission"),
                        f"{self.game.resolved_count} / {level.incident_count}",
                        detail=self.app.t("game.fixed_count"))
        draw_progress_bar(surface, (MISSION_RECT.left + 18, MISSION_RECT.bottom + 14,
                                    COLUMN_WIDTH - 36, 16),
                          self.game.resolved_count, level.incident_count)

        effects = [("coffee.png", f"+{level.effect_seconds} s", level.coffee_count),
                   ("critical.png", f"-{level.effect_seconds} s", level.critical_count)]
        y = MISSION_RECT.bottom + 100
        for icon_file, text, count in effects:
            if count:
                draw_effect_badge(surface, (MISSION_RECT.centerx, y), fonts, self.app.icons,
                                  icon_file, text, count)
                y += 130

    def _draw_message(self, surface):
        if not self._message:
            return
        text, color, _, detail = self._message
        title_font, detail_font = self.app.fonts.get(30), self.app.fonts.get(18)
        lines = wrap_text(detail, detail_font, TOAST_TEXT_WIDTH)[:3] if detail else []
        width = max([title_font.size(text)[0]] + [detail_font.size(line)[0] for line in lines]) + 60
        box = pygame.Rect(0, 0, width, 62 + 24 * len(lines))
        box.midtop = (TOAST_CENTER_X, TOAST_TOP)
        draw_panel(surface, box, border=color, radius=24, width=4)
        draw_text(surface, text, title_font, color, center=(box.centerx, box.top + 30))
        for number, line in enumerate(lines):
            draw_text(surface, line, detail_font, COLORS["text"],
                      center=(box.centerx, box.top + 64 + number * 24))
