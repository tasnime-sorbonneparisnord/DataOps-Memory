import pytest

from storage.player_profile import (MAX_PSEUDO_LENGTH, InvalidPseudoError, PlayerProfile,
                                    clean_pseudo)


def test_clean_pseudo_removes_extra_spaces():
    assert clean_pseudo("  Data   Queen  ") == "Data Queen"


def test_clean_pseudo_keeps_accents():
    assert clean_pseudo("Hélène_42") == "Hélène_42"


@pytest.mark.parametrize("raw", ["", "    ", "x" * (MAX_PSEUDO_LENGTH + 1), "rm -rf /*"])
def test_clean_pseudo_rejects_invalid_values(raw):
    with pytest.raises(InvalidPseudoError):
        clean_pseudo(raw)


def test_profile_starts_empty_without_file(tmp_path):
    assert PlayerProfile(tmp_path / "player.json").pseudo == ""


def test_profile_saves_and_reloads_pseudo(tmp_path):
    path = tmp_path / "player.json"
    PlayerProfile(path).set_pseudo("Vanilla")
    assert PlayerProfile(path).pseudo == "Vanilla"


def test_profile_ignores_corrupted_file(tmp_path):
    path = tmp_path / "player.json"
    path.write_text("{not json", encoding="utf-8")
    assert PlayerProfile(path).pseudo == ""


def test_invalid_pseudo_is_not_saved(tmp_path):
    profile = PlayerProfile(tmp_path / "player.json")
    profile.set_pseudo("Vanilla")
    with pytest.raises(InvalidPseudoError):
        profile.set_pseudo("   ")
    assert profile.pseudo == "Vanilla"


@pytest.mark.parametrize("raw, code", [("", "empty"), ("x" * (MAX_PSEUDO_LENGTH + 1), "too_long"),
                                       ("a/b", "characters")])
def test_invalid_pseudo_error_gives_a_code_for_the_interface(raw, code):
    with pytest.raises(InvalidPseudoError) as error:
        clean_pseudo(raw)
    assert error.value.code == code
