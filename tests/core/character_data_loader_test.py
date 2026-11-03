import json
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from myth_hash.core import character_data_loader
from myth_hash.core.character_data_loader import CharacterDataLoader

CHARACTER_NOUNS: dict[str, Any] = {
    "1": {
        "data": {
            "en": {"word": "Dragon", "gender": "neutral"},
            "de": {"word": "Drache", "gender": "masculine"},
        }
    },
    "2": {
        "data": {
            "en": {"word": "Griffin", "gender": "neutral"},
            "de": {"word": "Greif", "gender": "masculine"},
        }
    },
}

ATTRIBUTES: dict[str, Any] = {
    "1": {
        "words": {
            "en": {"neutral": "mighty"},
            "de": {
                "masculine": "mächtiger",
                "feminine": "mächtige",
                "neutral": "mächtiges",
            },
        }
    },
    "2": {
        "words": {
            "en": {"neutral": "wise"},
            "de": {"masculine": "weiser", "feminine": "weise", "neutral": "weises"},
        }
    },
}


@pytest.fixture
def fresh_loader() -> Iterator[None]:
    """Drop the cached singleton for the test and restore it afterwards."""
    original = CharacterDataLoader._instance
    CharacterDataLoader._instance = None
    yield
    CharacterDataLoader._instance = original


@pytest.fixture
def data_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, fresh_loader: None
) -> Path:
    """Serve the package data files from a temporary directory."""
    directory = tmp_path / "data"
    directory.mkdir()
    (directory / "character_nouns.json").write_text(
        json.dumps(CHARACTER_NOUNS), encoding="utf-8"
    )
    for name in ("physical_attributes.json", "personality_attributes.json"):
        (directory / name).write_text(json.dumps(ATTRIBUTES), encoding="utf-8")

    def files(_package: str) -> Path:
        return tmp_path

    monkeypatch.setattr(character_data_loader.resources, "files", files)
    return directory


def test_load_data_success(data_dir: Path) -> None:
    character_data = CharacterDataLoader().character_data
    assert [str(noun) for noun in character_data.character_nouns] == [
        "Dragon",
        "Griffin",
    ]
    assert len(character_data.physical_attributes) == 2
    assert character_data.personality_attributes[1].word("de", "feminine") == "weise"


def test_file_not_found_error(data_dir: Path) -> None:
    (data_dir / "physical_attributes.json").unlink()
    with pytest.raises(RuntimeError, match=r"Error loading physical_attributes\.json"):
        CharacterDataLoader()


def test_json_decode_error(data_dir: Path) -> None:
    (data_dir / "character_nouns.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(RuntimeError, match=r"Error loading character_nouns\.json"):
        CharacterDataLoader()


def test_singleton_instance() -> None:
    assert CharacterDataLoader() is CharacterDataLoader()


def test_concurrent_first_use_loads_once(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[str] = []
    read_json = character_data_loader._read_json

    def counting_read_json(file_name: str) -> dict[str, Any]:
        calls.append(file_name)
        return read_json(file_name)

    monkeypatch.setattr(character_data_loader, "_read_json", counting_read_json)

    barrier = threading.Barrier(8)
    instances: list[CharacterDataLoader] = []

    def create() -> None:
        barrier.wait()
        instances.append(CharacterDataLoader())

    threads = [threading.Thread(target=create) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(instances) == 8
    assert all(instance is instances[0] for instance in instances)
    assert len(calls) == 3
