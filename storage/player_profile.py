import json
import string
from pathlib import Path

MAX_PSEUDO_LENGTH = 16
ALLOWED_PSEUDO_CHARACTERS = set(string.ascii_letters + string.digits + " -_.'"
                                "àâäçéèêëîïôöùûüÿÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ")


class InvalidPseudoError(ValueError):
    """Raised when a pseudo is empty, too long or contains forbidden characters.

    `code` ("empty", "too_long" or "characters") lets the interface show the
    message in the player's language.
    """

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def clean_pseudo(raw: str) -> str:
    """Returns the pseudo without extra spaces, or raises InvalidPseudoError."""
    pseudo = " ".join(raw.split())
    if not pseudo:
        raise InvalidPseudoError("empty", "Le pseudo ne peut pas être vide.")
    if len(pseudo) > MAX_PSEUDO_LENGTH:
        raise InvalidPseudoError("too_long", f"{MAX_PSEUDO_LENGTH} caractères maximum.")
    if not set(pseudo) <= ALLOWED_PSEUDO_CHARACTERS:
        raise InvalidPseudoError("characters", "Lettres, chiffres, espaces, - et _ seulement.")
    return pseudo


class PlayerProfile:
    """Remembers the player's pseudo in a small local JSON file.

    A missing or corrupted file is never fatal: the pseudo is simply empty.
    """

    def __init__(self, path):
        self._path = Path(path)
        self._pseudo = self._load()

    @property
    def pseudo(self) -> str:
        return self._pseudo

    def set_pseudo(self, raw: str) -> str:
        """Validates, stores and saves the pseudo. Returns the cleaned pseudo."""
        self._pseudo = clean_pseudo(raw)
        self._save()
        return self._pseudo

    def _load(self) -> str:
        try:
            with self._path.open(encoding="utf-8") as file:
                return clean_pseudo(json.load(file).get("pseudo", ""))
        except (OSError, ValueError, AttributeError):
            return ""

    def _save(self):
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("w", encoding="utf-8") as file:
                json.dump({"pseudo": self._pseudo}, file, ensure_ascii=False, indent=2)
        except OSError:
            pass  # saving is a comfort: the game goes on without it
