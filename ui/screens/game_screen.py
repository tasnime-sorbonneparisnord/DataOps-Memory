"""Écran de jeu : la grille de cartes, la barre d'infos et le panneau « Mission »."""

import math

import pygame

from game.enums import SelectionOutcome
from ui.button import Button
from ui.card_renderer import CardRenderer
from ui.drawing import draw_database_icon, draw_panel, draw_text, wrap_text
from ui.grid_layout import GridLayout
from ui.settings import (COLORS, GRID_AREA_WIDTH, HEADER_HEIGHT, MARGIN, MISMATCH_DELAY,
                         SIDE_PANEL_WIDTH, THEME_NAMES, WINDOW_HEIGHT, WINDOW_WIDTH)
from ui.screens.base import Screen

HUD_BOX_WIDTH, HUD_BOX_HEIGHT, HUD_GAP = 200, 74, 16
LOW_TIME_SECONDS = 10


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
        self._grid_area = pygame.Rect(MARGIN, HEADER_HEIGHT + 30, GRID_AREA_WIDTH,
                                      WINDOW_HEIGHT - HEADER_HEIGHT - 30 - MARGIN)
        self._grid_frame = self._grid_area.inflate(24, 24)
        self._panel = pygame.Rect(self._grid_frame.right + 18, self._grid_frame.top,
                                  SIDE_PANEL_WIDTH, self._grid_frame.height)
        self._layout = GridLayout(self._grid_area, self.game.level.rows, self.game.level.columns)
        self._menu_button = Button((self._panel.left + 20, self._panel.bottom - 76,
                                    self._panel.width - 40, 56), "Retour au menu", primary=False)

        
        self._mismatch_timer = None
        self._reactions = {
            SelectionOutcome.MISMATCH: self._on_mismatch,
        }

    # ------------------------------------------------------------------
    # Événements
    # ------------------------------------------------------------------

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.show_menu()
        elif self._menu_button.is_clicked(event):
            self.app.show_menu()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._on_click(event.pos)

    def _on_click(self, position):
        index = self._layout.index_at(position)
        if index is None or self.game.is_over():
            return
        outcome = self.game.select_card(index)
        reaction = self._reactions.get(outcome)
        if reaction:
            reaction(index)

    def _on_mismatch(self, index):
        self._mismatch_timer = MISMATCH_DELAY

    # ------------------------------------------------------------------
    # Temps
    # ------------------------------------------------------------------

    def update(self, delta_seconds: float):
        self.game.update(delta_seconds)
        self._update_mismatch(delta_seconds)

    def _update_mismatch(self, delta_seconds):
        if self._mismatch_timer is None:
            return
        self._mismatch_timer -= delta_seconds
        if self._mismatch_timer <= 0:
            self.game.resolve_mismatch()
            self._mismatch_timer = None

    # ------------------------------------------------------------------
    # Dessin
    # ------------------------------------------------------------------

    def draw(self, surface):
        surface.blit(self.app.background, (0, 0))
        self._draw_header(surface)
        self._draw_cards(surface)
        self._draw_side_panel(surface)

    def _draw_header(self, surface):
        fonts = self.app.fonts
        draw_database_icon(surface, (MARGIN + 26, 60), 44, COLORS["title"],
                           COLORS["background_top"])
        draw_text(surface, "DataOps Memory", fonts.get(40, bold=True), COLORS["title"],
                  midleft=(MARGIN + 66, 60))

        best = self.app.scores.get_best(self.game.difficulty)
        boxes = [
            ("Temps restant", format_time(self.game.remaining_time), self._time_color()),
            ("Tentatives", str(self.game.attempts), COLORS["text"]),
            ("Meilleur", f"{best.time_left} s" if best else "—", COLORS["text"]),
        ]
        left = WINDOW_WIDTH - MARGIN - 3 * HUD_BOX_WIDTH - 2 * HUD_GAP
        for number, (title, value, color) in enumerate(boxes):
            rect = pygame.Rect(left + number * (HUD_BOX_WIDTH + HUD_GAP), 24,
                               HUD_BOX_WIDTH, HUD_BOX_HEIGHT)
            draw_panel(surface, rect)
            draw_text(surface, title, fonts.get(18), COLORS["text_muted"],
                      center=(rect.centerx, rect.top + 22))
            draw_text(surface, value, fonts.get(32, bold=True), color,
                      center=(rect.centerx, rect.top + 52))

    def _time_color(self):
        low = self.game.remaining_time <= LOW_TIME_SECONDS
        return COLORS["danger"] if low else COLORS["text"]

    def _draw_cards(self, surface):
        draw_panel(surface, self._grid_frame)
        for index, card in enumerate(self.game.board.get_cards()):
            self._renderer.draw(surface, card, self._layout.rect_of(index))

    def _draw_side_panel(self, surface):
        fonts, panel = self.app.fonts, self._panel
        draw_panel(surface, panel)
        x, width = panel.left + 22, panel.width - 44

        draw_text(surface, "Mission DataOps", fonts.get(26, bold=True), COLORS["title"],
                  topleft=(x, panel.top + 20))
        y = self._draw_paragraph(surface, "Associez chaque incident à sa solution pour "
                                 "remettre les services en ligne !", x, panel.top + 62, width)

        level = self.game.level
        y = self._draw_progress(surface, x, y + 16, width,
                                self.game.resolved_count, level.incident_count)

        draw_text(surface, "Thèmes", fonts.get(20, bold=True), COLORS["text"], topleft=(x, y + 18))
        for number, theme in enumerate(sorted(self.app.library.themes)):
            draw_text(surface, f"•  {THEME_NAMES.get(theme, theme)}", fonts.get(19),
                      COLORS["text"], topleft=(x + 6, y + 48 + number * 26))

        self._menu_button.draw(surface, fonts)

    def _draw_paragraph(self, surface, text, x, y, width, size=19):
        font = self.app.fonts.get(size)
        for line in wrap_text(text, font, width):
            draw_text(surface, line, font, COLORS["text"], topleft=(x, y))
            y += font.get_linesize()
        return y

    def _draw_progress(self, surface, x, y, width, done, total):
        draw_text(surface, f"Incidents réparés : {done} / {total}", self.app.fonts.get(19, bold=True),
                  COLORS["text"], topleft=(x, y))
        bar = pygame.Rect(x, y + 30, width, 14)
        pygame.draw.rect(surface, COLORS["empty_slot"], bar, border_radius=7)
        filled = bar.copy()
        filled.width = round(width * done / total) if total else 0
        if filled.width:
            pygame.draw.rect(surface, COLORS["success"], filled, border_radius=7)
        return bar.bottom