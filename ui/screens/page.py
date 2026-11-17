"""Base commune des pages du menu (niveaux, règles, scores, paramètres, crédits)."""

from abc import abstractmethod

import pygame

from ui.gold_style import GOLD, draw_gold_frame, render_gold_title
from ui.screens.base import Screen
from ui.section_button import SectionButton
from ui.settings import WINDOW_HEIGHT, WINDOW_WIDTH

CENTER_X = WINDOW_WIDTH // 2
PAGE_OVERLAY = (12, 14, 40, 140)        # voile sombre sur le fond de l'accueil
BACK_RECT = pygame.Rect(CENTER_X - 160, WINDOW_HEIGHT - 100, 320, 60)


class MenuPage(Screen):
    """Une page du menu : fond assombri, grand titre doré, contenu, bouton « Retour ».

    Chaque page fille n'écrit que ce qui lui est propre :
    draw_content() et, si besoin, handle_page_event() et update().
    Échap ou le bouton « Retour » ramènent à l'accueil.
    """

    def __init__(self, app, title, back_rect=BACK_RECT):
        super().__init__(app)
        self.title = title
        self._background = self._create_background()
        self._back_button = None              # back_rect=None : page sans bouton « Retour »
        if back_rect is not None:
            self._back_button = SectionButton(back_rect, app.t("common.back"), icon="menu_back.png",
                                              title_size=30)

    def _create_background(self) -> pygame.Surface:
        background = self.app.menu_background.copy()
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(PAGE_OVERLAY)
        background.blit(overlay, (0, 0))
        return background

    def handle_event(self, event):
        escape = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        back_clicked = self._back_button is not None and self._back_button.is_clicked(event)
        if escape or back_clicked:
            self.go_back()
        else:
            self.handle_page_event(event)

    def go_back(self):
        """Page précédente : l'accueil par défaut."""
        self.app.show_menu()

    def handle_page_event(self, event):
        """Événements propres à la page (aucun par défaut)."""

    def draw(self, surface):
        surface.blit(self._background, (0, 0))
        title = render_gold_title(self.title, self.app.fonts.get(64))
        surface.blit(title, title.get_rect(center=(CENTER_X, 80)))
        self.draw_content(surface)
        if self._back_button is not None:
            self._back_button.draw(surface, self.app.fonts, self.app.icons)

    @abstractmethod
    def draw_content(self, surface):
        """Dessine le contenu de la page, entre le titre et le bouton « Retour »."""

    # ------------------------------------------------------------------
    # Outils pour les pages filles
    # ------------------------------------------------------------------

    def draw_content_panel(self, surface, rect):
        """Grand cadre doré où la page écrit son contenu ; renvoie la zone intérieure."""
        return draw_gold_frame(surface, rect)

    @staticmethod
    def text_color(muted=False):
        return GOLD["muted" if muted else "text"]
