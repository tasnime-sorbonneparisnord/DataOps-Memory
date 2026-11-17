import json

import pytest

from storage.game_settings import DEFAULTS, GameSettings


def test_defaults_without_file(tmp_path):
    settings = GameSettings(tmp_path / "settings.json")
    assert settings.music_volume == DEFAULTS["music_volume"]
    assert settings.language == "fr"


@pytest.mark.parametrize("raw, expected", [(150, 100), (-20, 0), ("70", 70), ("abc", 0)])
def test_volume_is_kept_between_0_and_100(tmp_path, raw, expected):
    settings = GameSettings(tmp_path / "settings.json")
    settings.effects_volume = raw
    assert settings.effects_volume == expected


def test_unknown_language_is_refused(tmp_path):
    settings = GameSettings(tmp_path / "settings.json")
    with pytest.raises(ValueError):
        settings.language = "de"


def test_settings_are_saved_and_reloaded(tmp_path):
    path = tmp_path / "settings.json"
    settings = GameSettings(path)
    settings.music_volume, settings.brightness, settings.language = 20, 80, "en"
    settings.save()

    reloaded = GameSettings(path)
    assert (reloaded.music_volume, reloaded.brightness, reloaded.language) == (20, 80, "en")


def test_corrupted_file_gives_defaults(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("[1, 2", encoding="utf-8")
    assert GameSettings(path).brightness == DEFAULTS["brightness"]


def test_bad_values_in_file_are_cleaned(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"music_volume": 999, "language": "xx"}), encoding="utf-8")
    settings = GameSettings(path)
    assert settings.music_volume == 100
    assert settings.language == "fr"
