"""Point d'entrée du jeu DataOps Memory (version Pygame).

Lancement :  python main.py
"""

import pygame

from ui.settings import COLORS, FPS, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COLORS["background_top"])
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()