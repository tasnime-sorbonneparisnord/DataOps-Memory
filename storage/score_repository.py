
import json
from pathlib import Path

from game.enums import Difficulty
from game.game_result import GameResult


class ScoreRepository:
    """Reads and saves the best score of each level in a local JSON file.

    A missing or corrupted file is never fatal: the game simply starts
    without any record.
    """

    def __init__(self, path):
        self._path = Path(path)
        self._best = self._load()

    def get_best(self, difficulty: Difficulty):
        """Returns the best GameResult of a level, or None."""
        return self._best.get(difficulty)

    def submit(self, result: GameResult) -> bool:
        """Saves the result if it beats the record. Returns True if it does."""
        if not result.is_better_than(self.get_best(result.difficulty)):
            return False

        self._best[result.difficulty] = result
        self._save()
        return True

    def _load(self) -> dict:
        try:
            with self._path.open(encoding="utf-8") as file:
                data = json.load(file)
            return {
                Difficulty(name): _result_from_dict(Difficulty(name), values)
                for name, values in data.items()
            }
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            return {}

    def _save(self):
        data = {
            difficulty.value: {
                "time_left": result.time_left,
                "attempts": result.attempts,
            }
            for difficulty, result in self._best.items()
        }
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


def _result_from_dict(difficulty: Difficulty, values: dict) -> GameResult:
    time_left = values["time_left"]
    attempts = values["attempts"]

    if not isinstance(time_left, int) or not isinstance(attempts, int):
        raise TypeError("Scores must be integers.")

    return GameResult(difficulty, time_left, attempts, won=True)
