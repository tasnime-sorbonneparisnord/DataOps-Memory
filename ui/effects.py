"""Animation quand une paire est trouvée : les deux cartes grossissent, brillent et lancent des étincelles."""

import math
import random

import pygame

MATCH_DURATION = 0.9                 # durée totale de l'animation (secondes)
POP_DURATION = 0.35                  # durée du « pop » (la carte grossit puis revient)
POP_SCALE = 0.18                     # +18 % au plus gros
FLASH_DURATION = 0.2                 # éclair blanc sur les cartes au moment de la paire
PARTICLES_PER_CARD = 22
GRAVITY = 420                        # pixels par seconde², les étincelles retombent
GLOW_COLOR = (90, 230, 130)
PARTICLE_COLORS = [(90, 230, 130), (255, 214, 90), (255, 255, 255), (120, 210, 255)]


class Particle:
    """Une étincelle : elle part du centre de la carte, ralentit, retombe et s'efface."""

    def __init__(self, center, rng):
        angle = rng.uniform(0, 2 * math.pi)
        speed = rng.uniform(140, 300)
        self.x, self.y = center
        self.vx, self.vy = math.cos(angle) * speed, math.sin(angle) * speed - 120
        self.size = rng.randint(5, 10)
        self.color = rng.choice(PARTICLE_COLORS)

    def update(self, delta_seconds):
        self.vy += GRAVITY * delta_seconds
        self.x += self.vx * delta_seconds
        self.y += self.vy * delta_seconds

    def draw(self, surface, fade):
        size = max(1, round(self.size * fade))
        pygame.draw.circle(surface, self.color, (round(self.x), round(self.y)), size)


class MatchEffect:
    """L'animation d'une paire trouvée, pour les deux cartes (indices dans la grille)."""

    def __init__(self, indices, rects, rng=None):
        rng = rng or random.Random()
        self.indices = set(indices)
        self._time = 0.0
        self._particles = [Particle(rect.center, rng)
                           for rect in rects for _ in range(PARTICLES_PER_CARD)]

    @property
    def finished(self) -> bool:
        return self._time >= MATCH_DURATION

    @property
    def scale(self) -> float:
        """Taille des cartes : 1 = normale, un peu plus grande pendant le « pop »."""
        if self._time >= POP_DURATION:
            return 1.0
        return 1 + POP_SCALE * math.sin(math.pi * self._time / POP_DURATION)

    @property
    def _fade(self) -> float:
        """1 au début, 0 à la fin : tout s'efface progressivement."""
        return max(0.0, 1 - self._time / MATCH_DURATION)

    def update(self, delta_seconds):
        self._time += delta_seconds
        for particle in self._particles:
            particle.update(delta_seconds)

    def draw_card(self, surface, card_image, rect):
        """Dessine la carte agrandie, entourée d'un halo vert qui s'élargit et s'efface."""
        grow = round(10 + 24 * (1 - self._fade))
        halo = pygame.Surface((rect.width + 2 * grow, rect.height + 2 * grow), pygame.SRCALPHA)
        pygame.draw.rect(halo, (*GLOW_COLOR, round(240 * self._fade)), halo.get_rect(),
                         width=10, border_radius=22)
        surface.blit(halo, halo.get_rect(center=rect.center))

        size = (round(rect.width * self.scale), round(rect.height * self.scale))
        scaled = pygame.transform.smoothscale(card_image, size)
        surface.blit(scaled, scaled.get_rect(center=rect.center))
        flash = max(0.0, 1 - self._time / FLASH_DURATION)       # éclair blanc au tout début
        if flash:
            veil = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.rect(veil, (255, 255, 255, round(180 * flash)), veil.get_rect(),
                             border_radius=16)
            surface.blit(veil, veil.get_rect(center=rect.center))

    def draw_particles(self, surface):
        for particle in self._particles:
            particle.draw(surface, self._fade)
