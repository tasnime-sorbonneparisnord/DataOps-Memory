"""Point d'entrée du jeu DataOps Memory (version Pygame).

Lancement :  python main.py
"""

import sys

from storage.game_settings import GameSettings
from storage.incident_library import IncidentLibrary, IncidentLibraryError
from storage.player_profile import PlayerProfile
from storage.score_repository import ScoreRepository
from ui.app import App
from ui.settings import (INCIDENTS_EN_FILE, INCIDENTS_FILE, PLAYER_FILE, SCORES_FILE,
                         SETTINGS_FILE)


def load_libraries() -> dict:
    """Les incidents en français (obligatoires) et en anglais (facultatifs)."""
    libraries = {"fr": IncidentLibrary.from_json(INCIDENTS_FILE)}
    try:
        libraries["en"] = IncidentLibrary.from_json(INCIDENTS_EN_FILE)
    except IncidentLibraryError:
        pass  # pas de version anglaise valide : le jeu garde les incidents en français
    return libraries


def main():
    try:
        libraries = load_libraries()
    except IncidentLibraryError as error:
        print(f"Impossible de lancer le jeu : {error}")
        sys.exit(1)

    scores = ScoreRepository(SCORES_FILE)
    profile = PlayerProfile(PLAYER_FILE)
    settings = GameSettings(SETTINGS_FILE)
    App(libraries, scores, profile, settings).run()


if __name__ == "__main__":
    main()
