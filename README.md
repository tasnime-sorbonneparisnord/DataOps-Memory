# DataOps Memory

## 1. Project Overview

**DataOps Memory** is an educational memory game developed in Python using Pygame. Its purpose is to help players learn about IT incidents and their corresponding solutions through an interactive matching game.

Players must match each Incident Card with its corresponding Solution Card before the countdown reaches zero.

The game also includes special cards that affect the remaining time:

- **Coffee Card:** adds 10 seconds.
- **Critical Card:** removes 10 seconds.

The project applies Object-Oriented Programming (OOP) principles and Clean Code practices. It was developed collaboratively using Git and GitHub.

## 2. Game Levels

| Level | Pairs | Special Cards | Total Cards | Grid | Time |
|---|---:|---:|---:|---|---:|
| Easy | 4 | 0 | 8 | 2 × 4 | 60 seconds |
| Medium | 8 | 2 | 18 | 3 × 6 | 90 seconds |
| Hard | 12 | 4 | 28 | 4 × 7 | 120 seconds |

## 3. Main Features

- Three difficulty levels with different board sizes and countdown durations.
- Incident and solution cards that must be matched.
- Special cards that add or remove time.
- A countdown timer and attempt counter.
- Explanations displayed when an incident is successfully resolved.
- Player profiles and local score storage.
- French and English interface and incident content.
- Background music and sound effects.
- Animated menus, transitions and game screens.
- A console version to test the game logic without the graphical interface.

## 4. Architecture and Object-Oriented Design

The project is organized into separate modules, each with a clearly defined responsibility.

### 4.1 Data Models (`models/`)

This package contains the main objects representing the game:

- **`Card`**: abstract base class defining common card behavior and states.
- **`CardState`**: enumeration representing the different states of a card.
- **`PairCard`**: abstract class shared by incident and solution cards.
- **`IncidentCard` / `SolutionCard`**: represent the two cards forming a pair.
- **`CardEffect`**: immutable data class describing a time effect.
- **`SpecialCard`**: base class for special cards.
- **`CoffeeCard` / `CriticalCard`**: implement the two special time effects.
- **`Board`**: manages board dimensions, card insertion, shuffling and completion.
- **`IncidentPair`**: represents and validates an incident-solution pair.

### 4.2 Game Logic (`game/`)

This package contains the game rules independently of the graphical interface:

- **`MemoryGame`**: manages card selection, matching, special effects, attempts, victory, defeat and restart.
- **`CountdownTimer`**: manages the countdown, time bonuses and penalties.
- **`LevelConfig` / `LEVELS`**: centralize the configuration of the difficulty levels.
- **`GameResult`**: represents the result of a completed game.
- **`board_builder.py`**: creates and prepares the game board.
- **`enums.py`**: groups the enumerations used by the game.

### 4.3 Data Storage (`storage/`)

This package handles persistent data separately from the game rules:

- **`IncidentLibrary`**: loads, validates and provides incident data from JSON files.
- **`ScoreRepository`**: manages the best scores for each level.
- **`PlayerProfile`**: stores the player's name.
- **`GameSettings`**: manages volume, brightness and language preferences.

### 4.4 Graphical Interface (`ui/`)

This package contains the Pygame presentation layer:

- **`App`**: manages the application window, main loop and screen navigation.
- **`Screen`**: base class shared by the different screens.
- **Screen classes**: implement the splash screen, menus, level selection, cinematic, game, results, rules, scores, settings and credits.
- **`GridLayout`**: calculates the card grid layout.
- **`CardRenderer`**: handles card appearance and drawing.
- **`SoundManager`**: manages music and sound effects.
- **`i18n.py`**: centralizes interface translations.
- **Drawing and animation modules**: handle visual effects, transitions, sprites and interface elements.

The graphical interface uses the game logic without duplicating its rules.

## 5. Clean Code Practices

The project aims to produce code that is readable, maintainable, reusable and easy to extend.

The main practices include:

- **Single Responsibility Principle (SRP):** classes and modules have distinct responsibilities. For example, `MemoryGame` handles game rules, while `App` and the screen classes handle presentation.
- **DRY (Don't Repeat Yourself):** shared behavior and configuration are centralized to avoid unnecessary duplication.
- **Encapsulation:** objects manage their own data and expose methods and properties to control access.
- **Abstraction:** abstract classes such as `Card` and `Screen` define common interfaces.
- **Inheritance and polymorphism:** specialized cards and screens reuse common behavior while providing their own implementations.
- **Separation of concerns:** models, game logic, storage and graphical presentation are organized into separate packages.
- **Constants and configuration:** difficulty settings and reusable values are centralized instead of being scattered throughout the code.

## 6. Testing and Quality

Automated tests are written with **Pytest**.

The test suite covers:

- Card models, states and board behavior.
- Game rules, matching and special effects.
- Countdown timer and difficulty levels.
- Game results and score management.
- Player profiles and settings.
- Incident data validation and loading.
- Graphical interface components and behavior.

The UI tests are designed to run without opening a game window.

To run the complete test suite:

```bash
python -m pytest -v
```

The repository also includes a GitHub Actions workflow in `.github/workflows/tests.yml` to automate quality checks.

## 7. Technologies Used

- **Python 3.10+**
- **Pygame** – graphical interface and game loop.
- **Pytest** – automated testing.
- **JSON** – incident and solution data.
- **Scala 3** – additional content quality checker.
- **Git and GitHub** – version control and collaborative development.
- **GitHub Actions** – automated testing.

## 8. Project Structure

```text
DataOps-Memory/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── assets/
│   ├── cinematic/
│   ├── fonts/
│   ├── icons/
│   ├── images/
│   └── sounds/
│
├── data/
│   ├── incidents.json
│   └── incidents_en.json
│
├── docs/
│   └── logique_metier.md
│
├── game/
│   ├── __init__.py
│   ├── board_builder.py
│   ├── countdown_timer.py
│   ├── enums.py
│   ├── game_result.py
│   ├── levels.py
│   └── memory_game.py
│
├── models/
│   ├── __init__.py
│   ├── board.py
│   ├── card.py
│   ├── effect.py
│   ├── incident_pair.py
│   └── special_card.py
│
├── scala/
│   ├── README.md
│   ├── project.scala
│   ├── src/
│   └── tests/
│
├── storage/
│   ├── __init__.py
│   ├── game_settings.py
│   ├── incident_library.py
│   ├── player_profile.py
│   └── score_repository.py
│
├── tests/
│   ├── conftest.py
│   ├── test_game_logic_parts.py
│   ├── test_game_settings.py
│   ├── test_memory_game.py
│   ├── test_models.py
│   ├── test_player_profile.py
│   └── test_ui.py
│
├── ui/
│   ├── __init__.py
│   ├── app.py
│   ├── card_renderer.py
│   ├── drawing.py
│   ├── effects.py
│   ├── floating_sprite.py
│   ├── gold_style.py
│   ├── grid_layout.py
│   ├── hud.py
│   ├── i18n.py
│   ├── icons.py
│   ├── screens/
│   ├── section_button.py
│   ├── settings.py
│   ├── slider.py
│   ├── sound.py
│   └── transition.py
│
├── console_demo.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 9. Installation and Execution

### 9.1 Clone the Repository

```bash
git clone https://github.com/tasnime-sorbonneparisnord/DataOps-Memory.git
cd DataOps-Memory
```

### 9.2 Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 9.3 Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 9.4 Run the Automated Tests

```bash
python -m pytest -v
```

### 9.5 Launch the Graphical Game

```bash
python main.py
```

### 9.6 Launch the Console Version

```bash
python console_demo.py
```

The console version allows the game logic to be explored without launching the Pygame interface.

## 10. How to Play

1. Click to leave the splash screen.
2. Enter your player name and press **Enter**.
3. Select **Play**, choose a difficulty level and start the game.
4. Click two cards to try to match an incident with its corresponding solution.
5. When a pair is found, read the explanation of the solution.
6. Use special cards strategically: Coffee adds 10 seconds, while Critical removes 10 seconds.
7. Resolve all incidents before the countdown reaches zero.

**Keyboard shortcuts:**

- `Esc`: return to the menu.
- `R`: restart the game from the end screen.
- `N`: open level selection from the end screen.

**Settings:** music volume, sound-effect volume, brightness and language (French / English) can be configured in the settings screen.

Player information, scores and settings are stored locally.

## 11. Scala Extension – Content Quality Checker

The `scala/` directory contains an independent content quality checker written in **Scala 3**.

It uses functional programming concepts, including immutable case classes, pure functions, `Option`, `Either` and collection transformations.

The checker validates the incident JSON files, including:

- JSON structure and required fields.
- Duplicate pair identifiers.
- Minimum number of incident-solution pairs.
- Card label length.
- Existence of referenced icons.
- Consistency between French and English incident data.

To run the content checker:

```bash
scala-cli run scala --main-class dataops.quality.checkIncidents
```

To run the Scala tests:

```bash
scala-cli run scala --main-class dataops.quality.runQualityTests
```

For further details, see [`scala/README.md`](scala/README.md).

## 12. Assets and Credits

| Asset | Source | Licence |
|---|---|---|
| Icons | Lucide, converted to PNG (see `assets/icons/SOURCES.md`) | ISC |
| Font | Luckiest Guy – Google Fonts | Apache 2.0 |
| Characters, backgrounds, logo and cinematic frames | Generated with Gemini for this project and integrated by the team | — |
| Music and sound effects | Generated specifically for this project (see `assets/sounds/SOURCES.md`) | — |

## 13. Project Objectives

The project aims to:

- Apply Object-Oriented Programming concepts in a practical application.
- Develop modular, reusable and maintainable software components.
- Apply Clean Code principles and separation of responsibilities.
- Understand automated testing and data validation.
- Practice collaborative software development using Git and GitHub.
- Build an interactive educational game related to DataOps and IT incident management.

---

**DataOps Memory – Learn, Match and Solve.**# DataOps Memory

## 1. Project Overview

**DataOps Memory** is an educational memory game developed in Python using Pygame. Its purpose is to help players learn about IT incidents and their corresponding solutions through an interactive matching game.

Players must match each Incident Card with its corresponding Solution Card before the countdown reaches zero.

The game also includes special cards that affect the remaining time:

- **Coffee Card:** adds 10 seconds.
- **Critical Card:** removes 10 seconds.

The project applies Object-Oriented Programming (OOP) principles and Clean Code practices. It was developed collaboratively using Git and GitHub.

## 2. Game Levels

| Level | Pairs | Special Cards | Total Cards | Grid | Time |
|---|---:|---:|---:|---|---:|
| Easy | 4 | 0 | 8 | 2 × 4 | 60 seconds |
| Medium | 8 | 2 | 18 | 3 × 6 | 90 seconds |
| Hard | 12 | 4 | 28 | 4 × 7 | 120 seconds |

## 3. Main Features

- Three difficulty levels with different board sizes and countdown durations.
- Incident and solution cards that must be matched.
- Special cards that add or remove time.
- A countdown timer and attempt counter.
- Explanations displayed when an incident is successfully resolved.
- Player profiles and local score storage.
- French and English interface and incident content.
- Background music and sound effects.
- Animated menus, transitions and game screens.
- A console version to test the game logic without the graphical interface.

## 4. Architecture and Object-Oriented Design

The project is organized into separate modules, each with a clearly defined responsibility.

### 4.1 Data Models (`models/`)

This package contains the main objects representing the game:

- **`Card`**: abstract base class defining common card behavior and states.
- **`CardState`**: enumeration representing the different states of a card.
- **`PairCard`**: abstract class shared by incident and solution cards.
- **`IncidentCard` / `SolutionCard`**: represent the two cards forming a pair.
- **`CardEffect`**: immutable data class describing a time effect.
- **`SpecialCard`**: base class for special cards.
- **`CoffeeCard` / `CriticalCard`**: implement the two special time effects.
- **`Board`**: manages board dimensions, card insertion, shuffling and completion.
- **`IncidentPair`**: represents and validates an incident-solution pair.

### 4.2 Game Logic (`game/`)

This package contains the game rules independently of the graphical interface:

- **`MemoryGame`**: manages card selection, matching, special effects, attempts, victory, defeat and restart.
- **`CountdownTimer`**: manages the countdown, time bonuses and penalties.
- **`LevelConfig` / `LEVELS`**: centralize the configuration of the difficulty levels.
- **`GameResult`**: represents the result of a completed game.
- **`board_builder.py`**: creates and prepares the game board.
- **`enums.py`**: groups the enumerations used by the game.

### 4.3 Data Storage (`storage/`)

This package handles persistent data separately from the game rules:

- **`IncidentLibrary`**: loads, validates and provides incident data from JSON files.
- **`ScoreRepository`**: manages the best scores for each level.
- **`PlayerProfile`**: stores the player's name.
- **`GameSettings`**: manages volume, brightness and language preferences.

### 4.4 Graphical Interface (`ui/`)

This package contains the Pygame presentation layer:

- **`App`**: manages the application window, main loop and screen navigation.
- **`Screen`**: base class shared by the different screens.
- **Screen classes**: implement the splash screen, menus, level selection, cinematic, game, results, rules, scores, settings and credits.
- **`GridLayout`**: calculates the card grid layout.
- **`CardRenderer`**: handles card appearance and drawing.
- **`SoundManager`**: manages music and sound effects.
- **`i18n.py`**: centralizes interface translations.
- **Drawing and animation modules**: handle visual effects, transitions, sprites and interface elements.

The graphical interface uses the game logic without duplicating its rules.

## 5. Clean Code Practices

The project aims to produce code that is readable, maintainable, reusable and easy to extend.

The main practices include:

- **Single Responsibility Principle (SRP):** classes and modules have distinct responsibilities. For example, `MemoryGame` handles game rules, while `App` and the screen classes handle presentation.
- **DRY (Don't Repeat Yourself):** shared behavior and configuration are centralized to avoid unnecessary duplication.
- **Encapsulation:** objects manage their own data and expose methods and properties to control access.
- **Abstraction:** abstract classes such as `Card` and `Screen` define common interfaces.
- **Inheritance and polymorphism:** specialized cards and screens reuse common behavior while providing their own implementations.
- **Separation of concerns:** models, game logic, storage and graphical presentation are organized into separate packages.
- **Constants and configuration:** difficulty settings and reusable values are centralized instead of being scattered throughout the code.

## 6. Testing and Quality

Automated tests are written with **Pytest**.

The test suite covers:

- Card models, states and board behavior.
- Game rules, matching and special effects.
- Countdown timer and difficulty levels.
- Game results and score management.
- Player profiles and settings.
- Incident data validation and loading.
- Graphical interface components and behavior.

The UI tests are designed to run without opening a game window.

To run the complete test suite:

```bash
python -m pytest -v
```

The repository also includes a GitHub Actions workflow in `.github/workflows/tests.yml` to automate quality checks.

## 7. Technologies Used

- **Python 3.10+**
- **Pygame** – graphical interface and game loop.
- **Pytest** – automated testing.
- **JSON** – incident and solution data.
- **Scala 3** – additional content quality checker.
- **Git and GitHub** – version control and collaborative development.
- **GitHub Actions** – automated testing.

## 8. Project Structure

```text
DataOps-Memory/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── assets/
│   ├── cinematic/
│   ├── fonts/
│   ├── icons/
│   ├── images/
│   └── sounds/
│
├── data/
│   ├── incidents.json
│   └── incidents_en.json
│
├── docs/
│   └── logique_metier.md
│
├── game/
│   ├── __init__.py
│   ├── board_builder.py
│   ├── countdown_timer.py
│   ├── enums.py
│   ├── game_result.py
│   ├── levels.py
│   └── memory_game.py
│
├── models/
│   ├── __init__.py
│   ├── board.py
│   ├── card.py
│   ├── effect.py
│   ├── incident_pair.py
│   └── special_card.py
│
├── scala/
│   ├── README.md
│   ├── project.scala
│   ├── src/
│   └── tests/
│
├── storage/
│   ├── __init__.py
│   ├── game_settings.py
│   ├── incident_library.py
│   ├── player_profile.py
│   └── score_repository.py
│
├── tests/
│   ├── conftest.py
│   ├── test_game_logic_parts.py
│   ├── test_game_settings.py
│   ├── test_memory_game.py
│   ├── test_models.py
│   ├── test_player_profile.py
│   └── test_ui.py
│
├── ui/
│   ├── __init__.py
│   ├── app.py
│   ├── card_renderer.py
│   ├── drawing.py
│   ├── effects.py
│   ├── floating_sprite.py
│   ├── gold_style.py
│   ├── grid_layout.py
│   ├── hud.py
│   ├── i18n.py
│   ├── icons.py
│   ├── screens/
│   ├── section_button.py
│   ├── settings.py
│   ├── slider.py
│   ├── sound.py
│   └── transition.py
│
├── console_demo.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 9. Installation and Execution

### 9.1 Clone the Repository

```bash
git clone https://github.com/tasnime-sorbonneparisnord/DataOps-Memory.git
cd DataOps-Memory
```

### 9.2 Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 9.3 Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 9.4 Run the Automated Tests

```bash
python -m pytest -v
```

### 9.5 Launch the Graphical Game

```bash
python main.py
```

### 9.6 Launch the Console Version

```bash
python console_demo.py
```

The console version allows the game logic to be explored without launching the Pygame interface.

## 10. How to Play

1. Click to leave the splash screen.
2. Enter your player name and press **Enter**.
3. Select **Play**, choose a difficulty level and start the game.
4. Click two cards to try to match an incident with its corresponding solution.
5. When a pair is found, read the explanation of the solution.
6. Use special cards strategically: Coffee adds 10 seconds, while Critical removes 10 seconds.
7. Resolve all incidents before the countdown reaches zero.

**Keyboard shortcuts:**

- `Esc`: return to the menu.
- `R`: restart the game from the end screen.
- `N`: open level selection from the end screen.

**Settings:** music volume, sound-effect volume, brightness and language (French / English) can be configured in the settings screen.

Player information, scores and settings are stored locally.

## 11. Scala Extension – Content Quality Checker

The `scala/` directory contains an independent content quality checker written in **Scala 3**.

It uses functional programming concepts, including immutable case classes, pure functions, `Option`, `Either` and collection transformations.

The checker validates the incident JSON files, including:

- JSON structure and required fields.
- Duplicate pair identifiers.
- Minimum number of incident-solution pairs.
- Card label length.
- Existence of referenced icons.
- Consistency between French and English incident data.

To run the content checker:

```bash
scala-cli run scala --main-class dataops.quality.checkIncidents
```

To run the Scala tests:

```bash
scala-cli run scala --main-class dataops.quality.runQualityTests
```

For further details, see [`scala/README.md`](scala/README.md).

## 12. Assets and Credits

| Resource | Source | License |
|---|---|---|
| Characters and backgrounds | Drawn in Krita for this project | Created by the team |
| Logo | Designed in Adobe Illustrator for this project | Created by the team |
| Screen mockups | Designed in Figma (design stage only, not included in the game) | Created by the team |
| Intro video | Generated with Gemini (Veo), then split into frames with ffmpeg | — |
| Icons | [Lucide](https://lucide.dev), see `assets/icons/SOURCES.md` | ISC |
| Font | Luckiest Guy, [Google Fonts](https://fonts.google.com/specimen/Luckiest+Guy) | Apache 2.0 |
| Music and sound effects | Generated with code (Python, NumPy) for this project, see `assets/sounds/SOURCES.md` | No third-party rights |

All assets are stored in `assets/` and are separate from the code: they can be replaced
without changing any Python file, as long as the file names and formats stay the same.

## 13. Project Objectives

The project aims to:

- Apply Object-Oriented Programming concepts in a practical application.
- Develop modular, reusable and maintainable software components.
- Apply Clean Code principles and separation of responsibilities.
- Understand automated testing and data validation.
- Practice collaborative software development using Git and GitHub.
- Build an interactive educational game related to DataOps and IT incident management.

---

**DataOps Memory – Learn, Match and Solve.**
