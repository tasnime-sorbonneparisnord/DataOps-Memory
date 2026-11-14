
import json
import random
from dataclasses import dataclass
from pathlib import Path

from models.card import IncidentCard, SolutionCard
from models.incident_pair import IncidentPair


REQUIRED_FIELDS = (
    "pair_id",
    "theme",
    "incident",
    "solution",
    "explanation",
)


class IncidentLibraryError(Exception):
    """Raised when the incident file is missing, malformed or too small."""


@dataclass(frozen=True)
class IncidentEntry:
    """One incident/solution pair as written in the content file."""

    pair_id: str
    theme: str
    incident_label: str
    solution_label: str
    explanation: str
    incident_icon: str = ""
    solution_icon: str = ""

    def to_pair(self) -> IncidentPair:
        """Creates two fresh cards (hidden) for a new game."""
        incident = IncidentCard(
            f"{self.pair_id}-I", self.pair_id,
            self.incident_label, self.explanation, self.incident_icon,
        )
        solution = SolutionCard(
            f"{self.pair_id}-S", self.pair_id,
            self.solution_label, self.explanation, self.solution_icon,
        )
        return IncidentPair(incident, solution)


class IncidentLibrary:
    """Stock of incident/solution pairs in which each game draws its pairs."""

    def __init__(self, entries: list):
        pair_ids = [entry.pair_id for entry in entries]

        if len(pair_ids) != len(set(pair_ids)):
            raise IncidentLibraryError("Each pair_id must be unique.")

        self._entries = tuple(entries)

    @classmethod
    def from_json(cls, path) -> "IncidentLibrary":
        """Loads and validates the content file (UTF-8 JSON)."""
        raw_pairs = _read_json_list(Path(path))
        entries = [_entry_from_dict(raw, position)
                   for position, raw in enumerate(raw_pairs)]
        return cls(entries)

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def themes(self) -> set:
        return {entry.theme for entry in self._entries}

    def draw(self, count: int, rng: random.Random = None) -> list:
        """Returns `count` different pairs chosen at random, as new cards."""
        if count <= 0:
            raise ValueError("The number of pairs must be positive.")

        if count > len(self._entries):
            raise IncidentLibraryError(
                f"Not enough incidents: {count} requested, "
                f"{len(self._entries)} available."
            )

        chosen = (rng or random).sample(self._entries, count)
        return [entry.to_pair() for entry in chosen]


def _read_json_list(path: Path) -> list:
    try:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise IncidentLibraryError(f"Incident file not found: {path}") from None
    except json.JSONDecodeError as error:
        raise IncidentLibraryError(f"Invalid JSON in {path}: {error}") from None

    if not isinstance(data, list) or not data:
        raise IncidentLibraryError("The incident file must be a non-empty list.")

    return data


def _entry_from_dict(raw: dict, position: int) -> IncidentEntry:
    if not isinstance(raw, dict):
        raise IncidentLibraryError(f"Pair #{position} is not an object.")

    missing = [field for field in REQUIRED_FIELDS if not raw.get(field)]
    if missing:
        raise IncidentLibraryError(
            f"Pair #{position} is missing: {', '.join(missing)}"
        )

    return IncidentEntry(
        pair_id=raw["pair_id"],
        theme=raw["theme"],
        incident_label=raw["incident"],
        solution_label=raw["solution"],
        explanation=raw["explanation"],
        incident_icon=raw.get("incident_icon", ""),
        solution_icon=raw.get("solution_icon", ""),
    )
