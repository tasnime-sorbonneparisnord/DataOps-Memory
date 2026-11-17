"""Curseur réglable de 0 à 100 (volume, luminosité), avec boutons − et +."""

import pygame

from ui.drawing import draw_text
from ui.gold_style import GOLD

STEP = 10                  # pas des boutons − et +
KNOB_RADIUS = 13
BUTTON_SIZE = 38


class Slider:
    """On clique ou on fait glisser sur la barre, ou on utilise − et +.

    on_change(valeur) est appelé à chaque changement.
    """

    def __init__(self, rect, value, on_change):
        self.rect = pygame.Rect(rect)                 # zone complète : − barre +
        self.value = value
        self._on_change = on_change
        self._dragging = False
        self._minus = pygame.Rect(self.rect.left, 0, BUTTON_SIZE, BUTTON_SIZE)
        self._plus = pygame.Rect(0, 0, BUTTON_SIZE, BUTTON_SIZE)
        self._minus.centery = self._plus.centery = self.rect.centery
        self._plus.right = self.rect.right - 70           # place pour « 100 % » à droite
        self._track = pygame.Rect(self._minus.right + 22, 0,
                                  self._plus.left - self._minus.right - 44, 10)
        self._track.centery = self.rect.centery

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._minus.collidepoint(event.pos):
                self._set(self.value - STEP)
            elif self._plus.collidepoint(event.pos):
                self._set(self.value + STEP)
            elif self._track.inflate(0, 30).collidepoint(event.pos):
                self._dragging = True
                self._set_from_x(event.pos[0])
        elif event.type == pygame.MOUSEMOTION and self._dragging:
            self._set_from_x(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self._dragging = False

    def _set_from_x(self, x):
        ratio = (x - self._track.left) / self._track.width
        self._set(round(ratio * 100))

    def _set(self, value):
        value = max(0, min(100, value))
        if value != self.value:
            self.value = value
            self._on_change(value)

    def draw(self, surface, fonts):
        for button, label in ((self._minus, "-"), (self._plus, "+")):
            pygame.draw.rect(surface, GOLD["frame"], button, border_radius=8)
            pygame.draw.rect(surface, GOLD["fill"], button.inflate(-6, -6), border_radius=6)
            draw_text(surface, label, fonts.get(28), GOLD["title"], center=button.center)

        pygame.draw.rect(surface, GOLD["muted"], self._track, border_radius=5)
        filled = self._track.copy()
        filled.width = round(self._track.width * self.value / 100)
        if filled.width:
            pygame.draw.rect(surface, GOLD["title"], filled, border_radius=5)
        knob = (self._track.left + filled.width, self._track.centery)
        pygame.draw.circle(surface, GOLD["frame_dark"], knob, KNOB_RADIUS + 2)
        pygame.draw.circle(surface, GOLD["frame_light"], knob, KNOB_RADIUS)

        draw_text(surface, f"{self.value} %", fonts.get(24), GOLD["text"],
                  midleft=(self._plus.right + 14, self.rect.centery))
