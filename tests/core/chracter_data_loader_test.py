import json
import unittest
from unittest.mock import mock_open, patch

from myth_hash.core.character_data_loader import CharacterDataLoader


class TestCharacterDataLoader(unittest.TestCase):

    def setUp(self):
        # Sample data to mock file content
        self.character_nouns_data = json.dumps(
            {
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
        )
        self.attributes_data = json.dumps(
            {
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
                        "de": {
                            "masculine": "weiser",
                            "feminine": "weise",
                            "neutral": "weises",
                        },
                    }
                },
            }
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_load_data_success(self, mock_file):
        # Reset the singleton instance
        CharacterDataLoader._instance = None  # pylint: disable=protected-access

        # Mocking file reads
        mock_file.side_effect = [
            mock_open(read_data=self.character_nouns_data).return_value,
            mock_open(read_data=self.attributes_data).return_value,
            mock_open(read_data=self.attributes_data).return_value,
        ]

        loader = CharacterDataLoader()

        # Check if the data was loaded correctly
        character_data = loader.character_data
        self.assertEqual(len(character_data.character_nouns), 2)
        self.assertEqual(len(character_data.physical_attributes), 2)
        self.assertEqual(len(character_data.personality_attributes), 2)

    @patch("builtins.open", new_callable=mock_open)
    def test_file_not_found_error(self, mock_file):
        # Simulate file not found error
        mock_file.side_effect = FileNotFoundError

        # Reset the singleton instance to test error handling
        CharacterDataLoader._instance = None  # pylint: disable=protected-access

        with self.assertRaises(RuntimeError) as context:
            CharacterDataLoader()
        self.assertIn("Error loading", str(context.exception))

    @patch("builtins.open", new_callable=mock_open)
    def test_json_decode_error(self, mock_file):
        # Simulate JSON decode error
        mock_file.side_effect = json.JSONDecodeError("Expecting value", "", 0)

        # Reset the singleton instance to test error handling
        CharacterDataLoader._instance = None  # pylint: disable=protected-access

        with self.assertRaises(RuntimeError) as context:
            CharacterDataLoader()
        self.assertIn("Error loading", str(context.exception))

    def test_singleton_instance(self):
        # Ensure the class is a singleton
        instance1 = CharacterDataLoader()
        instance2 = CharacterDataLoader()

        self.assertIs(instance1, instance2)


if __name__ == "__main__":
    unittest.main()
