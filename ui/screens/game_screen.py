"""Écran de jeu : la grille de cartes, la barre d'infos et le panneau « Mission »."""

import math

import pygame

from game.enums import SelectionOutcome
from ui.button import Button
from ui.card_renderer import CardRenderer
from ui.drawing import draw_database_icon, draw_panel, draw_text, wrap_text
from ui.grid_layout import GridLayout
from ui.settings import (COLORS, END_DELAY, GRID_AREA_WIDTH, HEADER_HEIGHT, MARGIN,
                         MESSAGE_DURATION, MISMATCH_DELAY, SIDE_PANEL_WIDTH,
                         SPECIAL_FLASH_DURATION, THEME_NAMES, WINDOW_HEIGHT, WINDOW_WIDTH)
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
        self._end_timer = None       
        self._flashing = {}          # numéro de carte -> temps d'affichage restant
        self._message = None         # (texte, couleur, temps restant)
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

    def _on_match(self, index):
        self._show_message("Incident réparé !", COLORS["success"])

    def _on_special(self, index):
        seconds = self.game.board.get_card_at(index).activate().seconds_delta
        self._flashing[index] = SPECIAL_FLASH_DURATION
        if seconds > 0:
            self._show_message(f"Pause café ! +{seconds} s", COLORS["success"])
        else:
            self._show_message(f"Incident critique ! −{-seconds} s", COLORS["danger"])

    def _show_message(self, text, color):
        self._message = (text, color, MESSAGE_DURATION)

    # ------------------------------------------------------------------
    # Temps
    # ------------------------------------------------------------------

    def update(self, delta_seconds: float):
        self.game.update(delta_seconds)
        self._update_mismatch(delta_seconds)
        self._update_flashing(delta_seconds)
        self._update_message(delta_seconds)
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
            text, color, remaining = self._message
            remaining -= delta_seconds
            self._message = (text, color, remaining) if remaining > 0 else None   


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

    def draw(self, surface):
        surface.blit(self.app.background, (0, 0))
        self._draw_header(surface)
        self._draw_cards(surface)
        self._draw_side_panel(surface)
        self._draw_message(surface)

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
              self._renderer.draw(surface, card, self._layout.rect_of(index),
                                force_face=index in self._flashing)

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

        if self.game.last_explanation:
            top = y + 48 + len(self.app.library.themes) * 26 + 14
            draw_text(surface, "Dernière réparation", fonts.get(20, bold=True),
                      COLORS["success"], topleft=(x, top))
            self._draw_paragraph(surface, self.game.last_explanation, x, top + 30, width, size=17)

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

    def _draw_message(self, surface):
        if not self._message:
            return
        text, color, _ = self._message
        font = self.app.fonts.get(28, bold=True)
        box = pygame.Rect(0, 0, font.size(text)[0] + 60, 60)
        box.midbottom = (self._grid_area.centerx, self._grid_area.bottom - 10)
        draw_panel(surface, box, border=color, radius=30, width=3)
        draw_text(surface, text, font, color, center=box.center)