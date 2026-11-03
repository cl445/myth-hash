import logging

import pytest

from myth_hash import hash_name
from myth_hash.core import CharacterDataLoader


def test_hash_name() -> None:
    result = hash_name("teststring", "en")
    assert isinstance(result, tuple)
    assert len(result) == 3


def estimate_expected_collisions(n1: int, n2: int, n3: int, total_tests: int) -> float:
    total_combinations = n1 * n2 * n3
    return round((total_tests**2) / (2 * total_combinations))


@pytest.mark.slow
def test_name_uniqueness() -> None:
    character_data = CharacterDataLoader().character_data
    total_tests = 1_000_000
    expected_collisions = estimate_expected_collisions(
        len(character_data.physical_attributes),
        len(character_data.personality_attributes),
        len(character_data.character_nouns),
        total_tests,
    )
    threshold_factor = 3

    generated_names: set[tuple[str, str, str]] = set()
    duplicates = 0
    for i in range(total_tests):
        name = hash_name(f"teststring{i}", "en")
        if name in generated_names:
            duplicates += 1
        else:
            generated_names.add(name)

        if i % 100_000 == 0 and i > 0:
            logging.info("Progress: %d/%d", i, total_tests)

    logging.info("Total generated names: %d", total_tests)
    logging.info("Expected collisions: %s", expected_collisions)
    logging.info("Total duplicates: %d", duplicates)
    logging.info("Uniqueness rate: %s%%", 100 * (1 - duplicates / total_tests))

    assert duplicates < round(threshold_factor * expected_collisions)
