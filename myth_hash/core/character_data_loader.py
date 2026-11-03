"""Data loader for character attributes and nouns."""

import json
import threading
from dataclasses import dataclass
from importlib import resources
from typing import Any, ClassVar

from .words import CharacterNoun, NominativAdjective

CHARACTER_NOUNS_FILE = "character_nouns.json"
PHYSICAL_ATTRIBUTES_FILE = "physical_attributes.json"
PERSONALITY_ATTRIBUTES_FILE = "personality_attributes.json"


@dataclass
class CharacterData:
    """Container for character data including nouns and attributes."""

    character_nouns: list[CharacterNoun]
    physical_attributes: list[NominativAdjective]
    personality_attributes: list[NominativAdjective]


def _read_json(file_name: str) -> dict[str, Any]:
    """Read a JSON file shipped in the ``myth_hash/data`` package directory."""
    data_file = resources.files("myth_hash") / "data" / file_name
    try:
        content: dict[str, Any] = json.loads(data_file.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error loading {file_name}: {e}") from e
    return content


def _load_attributes(file_name: str) -> list[NominativAdjective]:
    return [
        NominativAdjective(word_id, data["words"])
        for word_id, data in _read_json(file_name).items()
    ]


def _load_character_nouns() -> list[CharacterNoun]:
    return [
        CharacterNoun(char_id, data["data"])
        for char_id, data in _read_json(CHARACTER_NOUNS_FILE).items()
    ]


class CharacterDataLoader:
    """Thread-safe singleton loader for character data from JSON files."""

    _instance: ClassVar["CharacterDataLoader | None"] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _character_data: CharacterData

    def __new__(cls) -> "CharacterDataLoader":
        """Return the shared loader instance, loading the data on first use."""
        with cls._lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                instance._character_data = CharacterData(
                    character_nouns=_load_character_nouns(),
                    physical_attributes=_load_attributes(PHYSICAL_ATTRIBUTES_FILE),
                    personality_attributes=_load_attributes(
                        PERSONALITY_ATTRIBUTES_FILE
                    ),
                )
                cls._instance = instance
            return cls._instance

    @property
    def character_data(self) -> CharacterData:
        """Get the loaded character data."""
        return self._character_data
