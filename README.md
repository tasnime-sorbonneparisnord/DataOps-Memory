# DataOps Memory

## 1. Project Overview

DataOps Memory is an educational memory game developed in Python. Its objective is to help players learn about IT incidents and their corresponding solutions through an interactive matching game.

Players must match each Incident Card with its corresponding Solution Card before the countdown reaches zero.

The game also includes special cards that affect the remaining time:
- Coffee Card: adds 10 seconds.
- Critical Card: removes 10 seconds.

The project is based on Object-Oriented Programming (OOP) principles and is developed collaboratively using Git and GitHub.

## 2. Game Levels

| Level | Pairs | Special Cards | Total Cards | Grid | Time |
|---|---:|---:|---:|---|---:|
| Easy | 4 | 0 | 8 | 2 × 4 | 60 seconds |
| Medium | 8 | 2 | 18 | 3 × 6 | 90 seconds |
| Hard | 12 | 4 | 28 | 4 × 7 | 120 seconds |

## 3. Project Development – Three Main Stages

The project is divided into three main development stages:

### Stage 1 – Data Models Development (Tasnime)

This stage focuses on designing and implementing the core data models using Object-Oriented Programming.

Tasks completed:

- **Card Models:** Created the abstract `Card` class, `CardState` enumeration, `PairCard`, `IncidentCard` and `SolutionCard`.
- **Card Behaviors:** Implemented card states and operations such as reveal, hide and mark as matched.
- **Special Cards:** Developed `CardEffect`, `SpecialCard`, `CoffeeCard` and `CriticalCard`.
- **Incident Pair:** Implemented the `IncidentPair` class to validate and manage incident-solution pairs.
- **Board Management:** Developed the `Board` class to manage dimensions, capacity, card insertion, shuffling and completion.
- **Unit Testing:** Created tests with Pytest to validate the models and their behavior.

**Status:** Completed. All 16 unit tests pass successfully.

### Stage 2 – Game Logic and Data (Khoubeib)

This stage implements the rules of the game, independently of Pygame.

Tasks completed:

- **`MemoryGame`:** card selection, incident/solution matching, special cards, attempts, victory, defeat and restart.
- **`CountdownTimer`:** countdown driven from outside (`update(delta)`), never below zero, bonus and penalty.
- **`LevelConfig` / `LEVELS`:** level parameters in one configuration (no hard-coded values).
- **`GameResult`:** result of a game and the single score comparison rule.
- **`IncidentLibrary`:** loads and validates `data/incidents.json` (24 pairs, 4 themes) and draws random pairs.
- **`ScoreRepository`:** best score per level in `data/best_scores.json` (missing or corrupted file = no record, no crash).
- **`console_demo.py`:** text version of the game to play the logic without the graphical interface.
- **Unit tests:** rules, timer, levels, scores, content file and a full game with a fixed seed.

**Status:** Completed. Interface for the UI described in `docs/logique_metier.md`.

### Stage 3 – Graphical User Interface (Vanilla)

This stage builds the Pygame interface on top of the game logic, without changing the rules (`game/`, `models/`).

Tasks completed:

- **Application (`App`):** window, game loop, navigation between screens, fade-to-black transitions and brightness. Incidents, scores, player profile and settings are injected from `main.py` (dependency injection).
- **Screens (one class each, polymorphism through `Screen`):** splash screen, player name, animated home menu, level selection and level intros, intro cinematic, game, end screen (victory / defeat), rules, best scores, settings and credits. Menu pages share a `MenuPage` base class (title, background, Back button).
- **Game screen:** card grid (`GridLayout`), card drawing by type (`CardRenderer`), time / attempts / record panels, mission progress, special cards, explanation after each pair and animations when a pair is found (`MatchEffect`).
- **Settings:** music and sound-effect volume, brightness and language (French / English), saved locally (`GameSettings`).
- **Player name:** entered at start-up, shown in the menu, the game and the end screen, saved locally (`PlayerProfile`).
- **Translation:** every interface text lives in `ui/i18n.py` (one key per text); English incidents are in `data/incidents_en.json`.
- **Sound:** background music and sound effects (`SoundManager`); the game keeps running silently if no audio device is available.
- **Unit tests:** grid, texts, card styles, level descriptions, animations, slider, translation, player profile and settings (tests run without opening a window).

**Status:** Completed.

## 4. Technologies Used

- Python 3.10+
- Object-Oriented Programming (OOP)
- Pygame
- Pytest
- Git, GitHub and GitHub Actions (tests run on every pull request)

## 5. Project Structure

```text
DataOps-Memory/
│
├── models/
│   ├── __init__.py
│   ├── card.py
│   ├── effect.py
│   ├── card_effect.py
│   ├── incident_pair.py
│   └── board.py
│
├── game/
│   ├── enums.py            Difficulty, GameState, SelectionOutcome
│   ├── levels.py           LevelConfig + LEVELS
│   ├── countdown_timer.py
│   ├── game_result.py
│   ├── board_builder.py
│   └── memory_game.py
│
├── storage/
│   ├── incident_library.py
│   ├── score_repository.py
│   ├── player_profile.py   player name (data/player.json)
│   └── game_settings.py    volumes, brightness, language (data/settings.json)
│
├── ui/
│   ├── app.py              window, game loop, navigation between screens
│   ├── settings.py         window size, paths, colours (no magic numbers)
│   ├── i18n.py             French and English texts
│   ├── drawing.py, gold_style.py, hud.py
│   ├── button.py, section_button.py, slider.py
│   ├── grid_layout.py, card_renderer.py, icons.py
│   ├── floating_sprite.py, effects.py, transition.py, sound.py
│   └── screens/            one class per screen (base.py, page.py, ...)
│
├── assets/
│   ├── icons/              card and menu icons (Lucide, ISC licence)
│   ├── images/             logo, characters, backgrounds
│   ├── cinematic/          intro video frames and sound
│   ├── sounds/             music and sound effects
│   └── fonts/              Luckiest Guy (Apache 2.0 licence)
│
├── data/
│   ├── incidents.json      24 incident/solution pairs (French)
│   └── incidents_en.json   the same pairs in English
│
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_memory_game.py
│   ├── test_game_logic_parts.py
│   ├── test_ui.py
│   ├── test_player_profile.py
│   └── test_game_settings.py
│
├── console_demo.py
├── requirements.txt
├── main.py
├── README.md
└── .gitignore
```

## 6. Installation and Execution

### Clone the Repository

```bash
git clone https://github.com/tasnime-sorbonneparisnord/DataOps-Memory.git
cd DataOps-Memory
```

### Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run Unit Tests

```bash
python -m pytest -v
```

### Play the Game (Pygame)

```bash
python main.py
```

### Play the Console Version (without Pygame)

```bash
python console_demo.py
```

## 7. How to Play

1. Click to leave the splash screen, then type your name and press **Enter**.
2. In the menu, choose **Play**, pick a level and read the character's bubble, then click **Let's go!** (*C'est parti !*).
3. Click two cards: an **incident** and its **solution** make a pair, and an explanation of the fix is shown.
4. **Coffee** cards give +10 seconds, **Critical** cards remove 10 seconds.
5. Fix every incident before the timer reaches zero. The record is the most time left, then the fewest attempts.

**Keyboard:** `Esc` goes back to the menu · on the end screen, `R` plays again and `N` opens the level selection.

**Settings:** music and sound-effect volume, brightness and language (French / English) are saved in `data/settings.json`. The player name, scores and settings are local files ignored by Git.

## 8. Assets and Credits

| Asset | Source | Licence |
|---|---|---|
| Icons | [Lucide](https://lucide.dev), converted to PNG (see `assets/icons/SOURCES.md`) | ISC |
| Font | Luckiest Guy (Google Fonts) | Apache 2.0 (`assets/fonts/LICENSE-luckiest-guy.txt`) |
| Characters, backgrounds, logo and intro video | Generated with Gemini for this project, then cut out and integrated by the team | — |
| Music and sound effects | Generated by code (NumPy synthesis) for this project (see `assets/sounds/SOURCES.md`) | — |

## 9. Project Objectives

- Apply Object-Oriented Programming concepts.
- Develop modular and reusable Python components.
- Understand software testing and validation.
- Practice collaborative development using Git and GitHub.
- Build an interactive educational game based on DataOps and IT incident management.

---

**DataOps Memory – Learn, Match and Solve.**
