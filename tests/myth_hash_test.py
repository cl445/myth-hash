import logging
import unittest

from myth_hash import hash_name
from myth_hash.core import CharacterDataLoader

logging.basicConfig(level=logging.INFO)


class TestMythHashGenerator(unittest.TestCase):

    def test_hash_name(self):
        result = hash_name("teststring", "en")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)


def estimate_expected_collisions(n1: int, n2: int, n3: int, total_tests: int) -> float:
    total_combinations = n1 * n2 * n3
    return round((total_tests**2) / (2 * total_combinations))


class TestNameUniqueness(unittest.TestCase):

    def setUp(self):
        self.data_loader = CharacterDataLoader()
        self.physical_attributes = self.data_loader.character_data.physical_attributes
        self.personality_attributes = (
            self.data_loader.character_data.personality_attributes
        )
        self.character_nouns = self.data_loader.character_data.character_nouns

    def test_name_uniqueness(self):
        generated_names = set()
        duplicates = 0
        total_tests = 1_000_000
        expected_collisions = estimate_expected_collisions(
            len(self.physical_attributes),
            len(self.personality_attributes),
            len(self.character_nouns),
            total_tests,
        )
        threshold_factor = 3

        for i in range(total_tests):
            input_string = f"teststring{i}"
            name = hash_name(input_string, "en")

            if name in generated_names:
                duplicates += 1
            else:
                generated_names.add(name)

            if i % 100_000 == 0 and i > 0:
                logging.info(f"Progress: {i}/{total_tests}")

        logging.info(f"Total generated names: {total_tests}")
        logging.info(f"Expected collisions: {expected_collisions}")
        logging.info(f"Total duplicates: {duplicates}")
        logging.info(f"Uniqueness rate: {100 * (1 - duplicates / total_tests)}%")

        self.assertLess(duplicates, round(threshold_factor * expected_collisions))


if __name__ == "__main__":
    unittest.main()
