"""Tests for words module."""

import pytest

from myth_hash.core.words import CharacterNoun, NominativAdjective


class TestNominativAdjective:
    """Tests for NominativAdjective class."""

    def test_init_valid(self):
        """Test initialization with valid data."""
        words = {
            "en": {"neutral": "big"},
            "de": {"masculine": "großer", "feminine": "große", "neutral": "großes"},
        }
        adj = NominativAdjective(1, words)
        assert adj.word_id == 1
        assert adj.words == words

    def test_validate_words_invalid_structure(self):
        """Test that invalid word structure raises ValueError."""
        with pytest.raises(ValueError, match="must be a dictionary"):
            NominativAdjective(1, {"en": "not_a_dict"})

    def test_validate_words_invalid_gender(self):
        """Test that invalid gender raises ValueError."""
        with pytest.raises(ValueError, match="Invalid gender"):
            NominativAdjective(1, {"en": {"invalid_gender": "word"}})

    def test_str(self):
        """Test string representation."""
        words = {"en": {"neutral": "big"}}
        adj = NominativAdjective(1, words)
        assert str(adj) == "big"

    def test_str_no_english(self):
        """Test string representation when English is not available."""
        words = {"de": {"neutral": "groß"}}
        adj = NominativAdjective(1, words)
        assert str(adj) == "No neutral English word available"

    def test_repr(self):
        """Test repr representation."""
        words = {"en": {"neutral": "big"}}
        adj = NominativAdjective(1, words)
        assert "Adjective: 1" in repr(adj)

    def test_word_valid(self):
        """Test getting a word with valid language and gender."""
        words = {
            "en": {"neutral": "big"},
            "de": {"masculine": "großer", "feminine": "große"},
        }
        adj = NominativAdjective(1, words)
        assert adj.word("en", "neutral") == "big"
        assert adj.word("de", "masculine") == "großer"
        assert adj.word("de", "feminine") == "große"

    def test_word_default_gender(self):
        """Test that default gender is neutral."""
        words = {"en": {"neutral": "big", "masculine": "big"}}
        adj = NominativAdjective(1, words)
        assert adj.word("en") == "big"

    def test_word_invalid_language(self):
        """Test that invalid language raises ValueError."""
        words = {"en": {"neutral": "big"}}
        adj = NominativAdjective(1, words)
        with pytest.raises(ValueError, match="No word found for the language 'fr'"):
            adj.word("fr", "neutral")

    def test_word_invalid_gender(self):
        """Test that invalid gender raises ValueError."""
        words = {"en": {"neutral": "big"}}
        adj = NominativAdjective(1, words)
        with pytest.raises(ValueError, match="No word found.*gender 'masculine'"):
            adj.word("en", "masculine")

    def test_set_word(self):
        """Test setting a word."""
        words = {"en": {"neutral": "big"}}
        adj = NominativAdjective(1, words)
        adj.set_word("en", "masculine", "bigger")
        assert adj.word("en", "masculine") == "bigger"

    def test_as_json(self):
        """Test JSON serialization."""
        words = {"en": {"neutral": "big"}}
        adj = NominativAdjective(1, words)
        json_data = adj.as_json()
        assert json_data["id"] == 1
        assert json_data["words"] == words


class TestCharacterNoun:
    """Tests for CharacterNoun class."""

    def test_init(self):
        """Test initialization."""
        data = {
            "en": {"word": "Dragon", "gender": "neutral"},
            "de": {"word": "Drache", "gender": "masculine"},
        }
        noun = CharacterNoun(1, data)
        assert noun.character_id == 1
        assert noun.data == data

    def test_str(self):
        """Test string representation."""
        data = {"en": {"word": "Dragon", "gender": "neutral"}}
        noun = CharacterNoun(1, data)
        assert str(noun) == "Dragon"

    def test_repr(self):
        """Test repr representation."""
        data = {"en": {"word": "Dragon", "gender": "neutral"}}
        noun = CharacterNoun(1, data)
        assert "CharacterNoun: 1" in repr(noun)

    def test_get_attribute_word(self):
        """Test getting word attribute."""
        data = {
            "en": {"word": "Dragon", "gender": "neutral"},
            "de": {"word": "Drache", "gender": "masculine"},
        }
        noun = CharacterNoun(1, data)
        assert noun.get_attribute("en", "word") == "Dragon"
        assert noun.get_attribute("de", "word") == "Drache"

    def test_get_attribute_gender(self):
        """Test getting gender attribute."""
        data = {
            "en": {"word": "Dragon", "gender": "neutral"},
            "de": {"word": "Drache", "gender": "masculine"},
        }
        noun = CharacterNoun(1, data)
        assert noun.get_attribute("en", "gender") == "neutral"
        assert noun.get_attribute("de", "gender") == "masculine"

    def test_get_attribute_invalid_language(self):
        """Test that invalid language raises ValueError."""
        data = {"en": {"word": "Dragon", "gender": "neutral"}}
        noun = CharacterNoun(1, data)
        with pytest.raises(ValueError, match="No word found for the language 'fr'"):
            noun.get_attribute("fr", "word")

    def test_get_attribute_invalid_attribute(self):
        """Test that invalid attribute raises ValueError."""
        data = {"en": {"word": "Dragon", "gender": "neutral"}}
        noun = CharacterNoun(1, data)
        with pytest.raises(ValueError, match="No invalid found"):
            noun.get_attribute("en", "invalid")

    def test_as_json(self):
        """Test JSON serialization."""
        data = {"en": {"word": "Dragon", "gender": "neutral"}}
        noun = CharacterNoun(1, data)
        json_data = noun.as_json()
        assert json_data["character_id"] == 1
        assert json_data["data"] == data

    def test_from_json(self):
        """Test JSON deserialization."""
        json_data = {
            "character_id": 1,
            "data": {"en": {"word": "Dragon", "gender": "neutral"}},
        }
        noun = CharacterNoun.from_json(json_data)
        assert noun.character_id == 1
        assert noun.data == json_data["data"]
