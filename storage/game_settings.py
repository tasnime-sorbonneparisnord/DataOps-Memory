import json
from pathlib import Path

LANGUAGES = ("fr", "en")
DEFAULTS = {"music_volume": 60, "effects_volume": 80, "brightness": 50, "language": "fr"}


def _clamp_percent(value) -> int:
    """A whole number between 0 and 100 (bad values become 0)."""
    try:
        return max(0, min(100, int(value)))
    except (TypeError, ValueError):
        return 0


class GameSettings:
    """Player settings (volumes, brightness, language) saved in a local JSON file.

    Values are always kept valid: volumes and brightness between 0 and 100,
    language "fr" or "en". A missing or corrupted file gives the defaults.
    """

    def __init__(self, path):
        self._path = Path(path)
        self._values = dict(DEFAULTS)
        self._load()

    @property
    def music_volume(self) -> int:
        return self._values["music_volume"]

    @music_volume.setter
    def music_volume(self, value):
        self._values["music_volume"] = _clamp_percent(value)

    @property
    def effects_volume(self) -> int:
        return self._values["effects_volume"]

    @effects_volume.setter
    def effects_volume(self, value):
        self._values["effects_volume"] = _clamp_percent(value)

    @property
    def brightness(self) -> int:
        """50 = normal, less = darker, more = lighter."""
        return self._values["brightness"]

    @brightness.setter
    def brightness(self, value):
        self._values["brightness"] = _clamp_percent(value)

    @property
    def language(self) -> str:
        return self._values["language"]

    @language.setter
    def language(self, value):
        if value not in LANGUAGES:
            raise ValueError(f"Unknown language: {value}")
        self._values["language"] = value

    def save(self):
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("w", encoding="utf-8") as file:
                json.dump(self._values, file, indent=2)
        except OSError:
            pass  # saving is a comfort: the game goes on without it

    def _load(self):
        try:
            with self._path.open(encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, ValueError):
            return
        if not isinstance(data, dict):
            return
        for name in ("music_volume", "effects_volume", "brightness"):
            if name in data:
                setattr(self, name, data[name])
        if data.get("language") in LANGUAGES:
            self.language = data["language"]
