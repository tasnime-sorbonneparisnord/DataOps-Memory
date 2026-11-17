"""Tests de l'interface qui ne demandent pas d'ouvrir de fenêtre."""

import pygame
import pytest

from models.card import IncidentCard, SolutionCard
from models.card_effect import CoffeeCard, CriticalCard
from ui.card_renderer import card_style
from ui.drawing import wrap_text
from ui.grid_layout import GridLayout
from ui.screens.game_screen import format_time

AREA = pygame.Rect(40, 140, 860, 620)


@pytest.fixture(scope="module")
def font():
    pygame.font.init()
    yield pygame.font.Font(None, 24)
    pygame.font.quit()


# --- GridLayout ---------------------------------------------------------------

@pytest.mark.parametrize("rows, columns", [(2, 4), (3, 6), (4, 7)])
def test_grid_has_one_rect_per_card_inside_the_area(rows, columns):
    layout = GridLayout(AREA, rows, columns)

    assert len(layout.rects) == rows * columns
    assert all(AREA.contains(rect) for rect in layout.rects)


def test_grid_cards_do_not_overlap():
    rects = GridLayout(AREA, 4, 7).rects

    assert not any(a.colliderect(b) for i, a in enumerate(rects) for b in rects[i + 1:])


def test_click_in_a_card_returns_its_index():
    layout = GridLayout(AREA, 3, 6)

    assert layout.index_at(layout.rect_of(0).center) == 0
    assert layout.index_at(layout.rect_of(7).center) == 7
    assert layout.index_at(layout.rect_of(17).center) == 17


def test_click_outside_the_cards_returns_none():
    layout = GridLayout(AREA, 2, 4)

    assert layout.index_at((0, 0)) is None
    assert layout.index_at((AREA.right + 50, AREA.centery)) is None


def test_click_in_the_gap_between_two_cards_returns_none():
    layout = GridLayout(AREA, 2, 4)
    first, second = layout.rect_of(0), layout.rect_of(1)

    gap_point = ((first.right + second.left) // 2, first.centery)
    assert layout.index_at(gap_point) is None


def test_grid_rejects_an_empty_grid():
    with pytest.raises(ValueError):
        GridLayout(AREA, 0, 4)


# --- Textes -------------------------------------------------------------------

def test_wrap_text_keeps_every_line_inside_the_width(font):
    lines = wrap_text("Purger les vieux logs du serveur de production", font, 120)

    assert len(lines) > 1
    assert all(font.size(line)[0] <= 120 for line in lines if " " in line)
    assert " ".join(lines) == "Purger les vieux logs du serveur de production"


def test_wrap_text_keeps_a_short_text_on_one_line(font):
    assert wrap_text("Café", font, 200) == ["Café"]


@pytest.mark.parametrize("seconds, expected", [(90, "01:30"), (59.2, "01:00"), (0, "00:00"), (-3, "00:00")])
def test_format_time(seconds, expected):
    assert format_time(seconds) == expected


# --- Style des cartes ---------------------------------------------------------

def test_card_style_of_pair_cards():
    incident = IncidentCard("I-1", "P1", "Disque plein", "explication")
    solution = SolutionCard("S-1", "P1", "Purger les logs", "explication")

    assert card_style(incident) == ("incident", "INCIDENT")
    assert card_style(solution) == ("solution", "SOLUTION")


def test_card_style_of_special_cards_shows_their_effect():
    assert card_style(CoffeeCard("C-1", 10)) == ("coffee", "+10 s")
    assert card_style(CriticalCard("K-1", 10)) == ("critical", "−10 s")


# --- Présentation des niveaux -------------------------------------------------

def french():
    from types import SimpleNamespace

    from ui.i18n import Translator
    return Translator(SimpleNamespace(language="fr"))


def english():
    from types import SimpleNamespace

    from ui.i18n import Translator
    return Translator(SimpleNamespace(language="en"))


def test_level_description_of_easy_level_has_no_special_card():
    from game.enums import Difficulty
    from ui.screens.level_intro_screen import level_description

    lines = level_description(Difficulty.EASY, french())

    assert lines[0] == "4 incidents à réparer"
    assert "Aucune carte spéciale" in lines


def test_level_description_of_hard_level_lists_special_cards():
    from game.enums import Difficulty
    from ui.screens.level_intro_screen import level_description

    lines = level_description(Difficulty.HARD, french())

    assert "2 cartes Café : +10 s" in lines
    assert "2 cartes Critique : -10 s" in lines


def test_level_description_follows_the_language():
    from game.enums import Difficulty
    from ui.screens.level_intro_screen import level_description

    assert level_description(Difficulty.MEDIUM, english())[2] == "1 Coffee card: +10 s"


# --- Traduction ---------------------------------------------------------------

def test_every_french_text_has_an_english_version():
    from ui.i18n import TEXTS

    assert set(TEXTS["fr"]) == set(TEXTS["en"])


def test_translator_fills_values_and_follows_the_settings():
    from types import SimpleNamespace

    from ui.i18n import Translator

    settings = SimpleNamespace(language="fr")
    t = Translator(settings)
    assert t("menu.hello", pseudo="Vanilla") == "Salut, Vanilla !"

    settings.language = "en"                    # la langue change : le texte suit
    assert t("menu.hello", pseudo="Vanilla") == "Hi, Vanilla!"


def test_english_incidents_match_the_french_ones():
    from storage.incident_library import IncidentLibrary
    from ui.settings import INCIDENTS_EN_FILE, INCIDENTS_FILE
    import json

    french_ids = [entry["pair_id"] for entry in json.load(open(INCIDENTS_FILE, encoding="utf-8"))]
    english_ids = [entry["pair_id"] for entry in json.load(open(INCIDENTS_EN_FILE, encoding="utf-8"))]
    assert french_ids == english_ids
    assert len(IncidentLibrary.from_json(INCIDENTS_EN_FILE)) == len(french_ids)


# --- Animations ---------------------------------------------------------------

def test_wave_stays_between_minus_and_plus_amplitude():
    from ui.floating_sprite import wave

    values = [wave(t / 10, 6, 2.0) for t in range(100)]

    assert max(values) <= 6 and min(values) >= -6
    assert wave(0, 6, 2.0) == 0


def test_fade_goes_to_black_calls_the_action_once_then_comes_back():
    from ui.transition import FADE_IN_DURATION, FADE_OUT_DURATION, FadeTransition

    calls = []
    fade = FadeTransition(lambda: calls.append("écran suivant"))

    fade.update(FADE_OUT_DURATION / 2)
    assert 0 < fade.darkness < 1 and calls == []

    fade.update(FADE_OUT_DURATION / 2)
    assert fade.darkness == pytest.approx(1) and calls == ["écran suivant"]

    fade.update(FADE_IN_DURATION)
    assert fade.finished and calls == ["écran suivant"]


def test_match_effect_pops_then_finishes():
    import random

    from ui.effects import MATCH_DURATION, POP_DURATION, MatchEffect

    effect = MatchEffect([0, 5], [pygame.Rect(0, 0, 100, 130)] * 2, random.Random(1))
    effect.update(POP_DURATION / 2)
    assert effect.scale > 1

    effect.update(MATCH_DURATION)
    assert effect.scale == 1 and effect.finished


# --- Curseur des paramètres ---------------------------------------------------

def test_slider_buttons_change_the_value_by_steps_and_stay_in_range():
    from ui.slider import STEP, Slider

    changes = []
    slider = Slider((0, 0, 430, 40), 95, changes.append)
    click = lambda rect: pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=rect.center)

    slider.handle_event(click(slider.plus_rect))
    assert slider.value == 100 and changes == [100]

    slider.handle_event(click(slider.plus_rect))            # déjà au maximum : rien ne change
    assert changes == [100]

    slider.handle_event(click(slider.minus_rect))
    assert slider.value == 100 - STEP
