"""Tests for hash_util module."""

import pytest

from myth_hash.core.hash_util import check_language, generate_indices, hash_name


class TestCheckLanguage:
    """Tests for check_language function."""

    def test_valid_languages(self):
        """Test that valid languages pass without error."""
        check_language("en")
        check_language("de")

    def test_invalid_language(self):
        """Test that invalid language raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported language 'fr'"):
            check_language("fr")

        with pytest.raises(ValueError, match="Supported languages are"):
            check_language("es")


class TestGenerateIndices:
    """Tests for generate_indices function."""

    def test_deterministic(self):
        """Test that same input produces same indices."""
        indices1 = generate_indices("test", [10, 20, 30])
        indices2 = generate_indices("test", [10, 20, 30])
        assert indices1 == indices2

    def test_different_inputs(self):
        """Test that different inputs produce different indices."""
        indices1 = generate_indices("test1", [10, 20, 30])
        indices2 = generate_indices("test2", [10, 20, 30])
        assert indices1 != indices2

    def test_within_bounds(self):
        """Test that indices are within specified bounds."""
        list_sizes = [10, 20, 30]
        indices = generate_indices("test", list_sizes)
        assert len(indices) == len(list_sizes)
        for index, size in zip(indices, list_sizes):
            assert 0 <= index < size

    def test_single_list(self):
        """Test with single list size."""
        indices = generate_indices("test", [100])
        assert len(indices) == 1
        assert 0 <= indices[0] < 100

    def test_many_lists(self):
        """Test with many list sizes."""
        list_sizes = [5, 10, 15, 20, 25, 30]
        indices = generate_indices("test", list_sizes)
        assert len(indices) == len(list_sizes)
        for index, size in zip(indices, list_sizes):
            assert 0 <= index < size


class TestHashName:
    """Tests for hash_name function."""

    def test_english_output(self):
        """Test English output."""
        physical, personality, character = hash_name("test", "en")
        assert isinstance(physical, str)
        assert isinstance(personality, str)
        assert isinstance(character, str)
        assert len(physical) > 0
        assert len(personality) > 0
        assert len(character) > 0

    def test_german_output(self):
        """Test German output."""
        physical, personality, character = hash_name("test", "de")
        assert isinstance(physical, str)
        assert isinstance(personality, str)
        assert isinstance(character, str)
        assert len(physical) > 0
        assert len(personality) > 0
        assert len(character) > 0

    def test_deterministic(self):
        """Test that same input produces same output."""
        result1 = hash_name("test", "en")
        result2 = hash_name("test", "en")
        assert result1 == result2

    def test_different_inputs(self):
        """Test that different inputs produce different outputs."""
        result1 = hash_name("test1", "en")
        result2 = hash_name("test2", "en")
        assert result1 != result2

    def test_default_language(self):
        """Test that default language is English."""
        result_explicit = hash_name("test", "en")
        result_default = hash_name("test")
        assert result_explicit == result_default

    def test_invalid_language(self):
        """Test that invalid language raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported language"):
            hash_name("test", "fr")

    def test_empty_string(self):
        """Test with empty string (should still work)."""
        result = hash_name("", "en")
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_unicode_input(self):
        """Test with Unicode characters."""
        result = hash_name("测试", "en")
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_long_input(self):
        """Test with very long input string."""
        long_string = "a" * 10000
        result = hash_name(long_string, "en")
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_special_characters(self):
        """Test with special characters."""
        result = hash_name("!@#$%^&*()", "en")
        assert isinstance(result, tuple)
        assert len(result) == 3
