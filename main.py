"""Point d'entrée du jeu DataOps Memory (version Pygame).

Lancement :  python main.py
"""

import sys

from storage.incident_library import IncidentLibrary, IncidentLibraryError
from storage.game_settings import GameSettings
from storage.player_profile import PlayerProfile
from storage.score_repository import ScoreRepository
from ui.app import App
from ui.settings import INCIDENTS_FILE, PLAYER_FILE, SCORES_FILE, SETTINGS_FILE


def main():
    try:
        library = IncidentLibrary.from_json(INCIDENTS_FILE)
    except IncidentLibraryError as error:
        print(f"Impossible de lancer le jeu : {error}")
        sys.exit(1)

    scores = ScoreRepository(SCORES_FILE)
    profile = PlayerProfile(PLAYER_FILE)
    settings = GameSettings(SETTINGS_FILE)
    App(library, scores, profile, settings).run()


if __name__ == "__main__":
    main()
