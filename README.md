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

This stage focuses on creating the graphical interface using Pygame.

Planned tasks:

- Design the game window and interface.
- Display the cards and game board.
- Implement mouse interactions.
- Display the countdown timer and score.
- Add game menus and difficulty selection.
- Display victory and defeat screens.
- Integrate the graphical interface with the game logic.

**Status:** To be developed.

## 4. Technologies Used

- Python
- Object-Oriented Programming (OOP)
- Pytest
- Pygame
- Git and GitHub

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
│   └── score_repository.py
│
├── data/
│   └── incidents.json
│
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_memory_game.py
│   └── test_game_logic_parts.py
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

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Run Unit Tests

```bash
python -m pytest -v
```

### Play the Console Version (without Pygame)

```bash
python console_demo.py
```

## 7. Project Objectives

- Apply Object-Oriented Programming concepts.
- Develop modular and reusable Python components.
- Understand software testing and validation.
- Practice collaborative development using Git and GitHub.
- Build an interactive educational game based on DataOps and IT incident management.

---

**DataOps Memory – Learn, Match and Solve.**
