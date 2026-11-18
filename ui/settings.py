"""Réglages de l'interface : taille de la fenêtre, vitesse, couleurs et mise en page.

Toutes les valeurs d'affichage sont ici, pour ne rien écrire en dur ailleurs.
"""

from pathlib import Path

WINDOW_TITLE = "DataOps Memory"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
FPS = 60

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
INCIDENTS_FILE = DATA_DIR / "incidents.json"
INCIDENTS_EN_FILE = DATA_DIR / "incidents_en.json"
SCORES_FILE = DATA_DIR / "best_scores.json"
PLAYER_FILE = DATA_DIR / "player.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
ICONS_DIR = PROJECT_DIR / "assets" / "icons"
IMAGES_DIR = PROJECT_DIR / "assets" / "images"
FONTS_DIR = PROJECT_DIR / "assets" / "fonts"
CINEMATIC_DIR = PROJECT_DIR / "assets" / "cinematic"
SOUNDS_DIR = PROJECT_DIR / "assets" / "sounds"
DISPLAY_FONT_FILE = FONTS_DIR / "LuckiestGuy-Regular.ttf"
MENU_BACKGROUND_FILE = IMAGES_DIR / "menu_background.png"

COLORS = {
    # Fond et panneaux
    "background_top": (207, 227, 255),
    "background_bottom": (233, 228, 255),
    "panel": (246, 244, 255),
    "panel_border": (185, 178, 240),

    # Textes
    "title": (108, 60, 240),
    "text": (29, 42, 90),
    "text_muted": (95, 105, 150),
    "text_light": (255, 255, 255),

    # Cartes
    "card_back": (123, 79, 224),
    "card_back_icon": (185, 165, 245),
    "incident": (239, 79, 95),
    "solution": (76, 195, 106),
    "coffee": (247, 201, 72),
    "critical": (74, 94, 232),
    "badge": (255, 255, 255),
    "matched_overlay": (255, 255, 255),
    "empty_slot": (220, 215, 245),

    # Boutons
    "button": (108, 60, 240),
    "button_hover": (132, 92, 250),
    "button_secondary": (230, 226, 252),
    "button_secondary_hover": (214, 208, 250),

    # Messages
    "success": (46, 160, 90),
    "danger": (215, 60, 75),
}

FONT_NAMES = "arialroundedmtbold,arial,helvetica,dejavusans"

# Mise en page de l'écran de jeu (en pixels)
CARD_GAP = 14
CARD_MAX_WIDTH = 180
CARD_RATIO = 1.3          # hauteur = largeur x 1,3
CORNER_RADIUS = 16

# Durées (en secondes)
MISMATCH_DELAY = 1.0      # temps pendant lequel deux cartes différentes restent visibles
MESSAGE_DURATION = 1.6    # durée d'affichage d'un message (carte spéciale, etc.)
SPECIAL_FLASH_DURATION = 0.8   # durée d'affichage d'une carte spéciale retournée
END_DELAY = 1.0           # pause avant l'écran de fin

