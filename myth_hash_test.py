import unittest
from pathlib import Path

from myth_hash import load_attributes, load_character_nouns, \
    hash_name


class TestMythHashGenerator(unittest.TestCase):

    def test_load_attributes(self):
        physical_attributes_path = Path(__file__).parent / 'physical_attributes.json'
        physical_attributes = load_attributes(physical_attributes_path)
        self.assertIsInstance(physical_attributes, list)
        self.assertGreater(len(physical_attributes), 0)

    def test_load_characters(self):
        characters = load_character_nouns()
        self.assertIsInstance(characters, list)
        self.assertGreater(len(characters), 0)

    def test_hash_name(self):
        characters = load_character_nouns()
        physical_attributes = load_attributes(Path(__file__).parent / 'physical_attributes.json')
        personality_attributes = load_attributes(Path(__file__).parent / 'personality_attributes.json')

        result = hash_name("teststring", physical_attributes, personality_attributes, characters, "en")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)


def calculate_expected_collisions(n1: int, n2: int, n3: int, total_tests: int) -> float:
    total_combinations = n1 * n2 * n3
    expected_collisions = (total_tests ** 2) / (2 * total_combinations)
    return round(expected_collisions)


class TestNameUniqueness(unittest.TestCase):

    def test_name_uniqueness(self):
        character_nouns = load_character_nouns()
        physical_attributes = load_attributes(Path(__file__).parent / 'physical_attributes.json')
        personality_attributes = load_attributes(Path(__file__).parent / 'personality_attributes.json')

        generated_names = set()
        duplicates = 0
        total_tests = 1000000  # Anzahl der zu generierenden Namen
        expected_collisions = calculate_expected_collisions(len(physical_attributes),
                                                            len(personality_attributes),
                                                            len(character_nouns), total_tests)

        for i in range(total_tests):
            input_string = f"teststring{i}"
            name = hash_name(input_string, physical_attributes, personality_attributes, character_nouns, "en")

            if name in generated_names:
                duplicates += 1
            else:
                generated_names.add(name)

        print(f"Total generated names: {total_tests}")
        print(f"Expected collisions: {expected_collisions}")
        print(f"Total duplicates: {duplicates}")
        print(f"Uniqueness rate: {100 * (1 - duplicates / total_tests)}%")

        self.assertLess(duplicates, 3 * expected_collisions)


if __name__ == '__main__':
    unittest.main()
