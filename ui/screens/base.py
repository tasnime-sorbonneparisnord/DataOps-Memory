"""Contrat commun à tous les écrans (polymorphisme)."""

from abc import ABC, abstractmethod


class Screen(ABC):
    """Un écran reçoit les événements, avance dans le temps et se dessine.

    L'application appelle ces trois méthodes à chaque image, sans savoir
    de quel écran il s'agit : menu, règles, partie ou fin.
    """

    def __init__(self, app):
        self.app = app

    @abstractmethod
    def handle_event(self, event):
        """Réagit à un événement Pygame (clic, touche...)."""

    def update(self, delta_seconds: float):
        """Fait avancer l'écran dans le temps (rien par défaut)."""

    @abstractmethod
    def draw(self, surface):
        """Dessine l'écran."""
        