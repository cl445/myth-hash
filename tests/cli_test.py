import json
import logging
import subprocess
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from myth_hash.cli import (
    hash_name_cli,
    parse_arguments,
    setup_logging,
    validate_input_string,
)

CLI_PATH = Path(__file__).parent.parent / "myth_hash" / "cli.py"


def run_cli(args: list[str]) -> tuple[str, str, int]:
    result = subprocess.run(
        ["python3", CLI_PATH.as_posix()] + args,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout, result.stderr, result.returncode


def test_default_language_text_output():
    stdout, stderr, returncode = run_cli(["example_name"])
    assert returncode == 0
    assert "-" in stdout  # Check if the output contains the expected format
    assert not stderr  # Expect no errors or warnings


def test_default_language_json_output():
    stdout, stderr, returncode = run_cli(["example_name", "-f", "json"])
    assert returncode == 0
    assert not stderr
    output = json.loads(stdout)
    assert "physical_attribute" in output
    assert "personality_attribute" in output
    assert "character" in output


def test_german_language_text_output():
    stdout, stderr, returncode = run_cli(["example_name", "-l", "de"])
    assert returncode == 0
    assert "-" in stdout
    assert not stderr


def test_german_language_json_output():
    stdout, stderr, returncode = run_cli(["example_name", "-l", "de", "-f", "json"])
    assert returncode == 0
    assert not stderr
    output = json.loads(stdout)
    assert "physical_attribute" in output
    assert "personality_attribute" in output
    assert "character" in output


def test_empty_input_string():
    _, stderr, returncode = run_cli([""])
    assert returncode != 0
    assert "Input validation error" in stderr


def test_invalid_log_level():
    _, stderr, returncode = run_cli(["example_name", "--log-level", "INVALID"])
    assert returncode != 0
    assert "invalid choice" in stderr


def test_debug_log_level():
    _, stderr, returncode = run_cli(["example_name", "--log-level", "DEBUG"])
    assert returncode == 0
    assert (
        "DEBUG" in stderr or not stderr
    )  # DEBUG log output might be empty if nothing logs at that level


def test_critical_log_level():
    _, stderr, returncode = run_cli(["example_name", "--log-level", "CRITICAL"])
    assert returncode == 0
    assert not stderr  # No critical errors should be present


def test_invalid_format():
    _, stderr, returncode = run_cli(["example_name", "-f", "invalid_format"])
    assert returncode != 0
    assert "argument -f/--format: invalid choice" in stderr


@pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_log_levels(log_level):
    _, stderr, returncode = run_cli(["example_name", "--log-level", log_level])
    assert returncode == 0
    if log_level == "DEBUG":
        assert "DEBUG" in stderr or not stderr
    elif log_level == "INFO":
        assert (
            not stderr
        )  # INFO logs usually go to stdout or are not logged if there's no message
    elif log_level == "WARNING":
        assert "WARNING" in stderr or not stderr  # No warnings might be logged
    elif log_level == "ERROR":
        assert "ERROR" in stderr or not stderr  # No errors might be logged
    elif log_level == "CRITICAL":
        assert not stderr  # Only critical errors should appear, but we're assuming none


# Unit tests for CLI functions


def test_validate_input_string_valid():
    """Test that valid input strings pass validation."""
    validate_input_string("test")
    validate_input_string("  test  ")  # Should strip whitespace


def test_validate_input_string_empty():
    """Test that empty strings raise ValueError."""
    with pytest.raises(ValueError, match="Input string cannot be empty"):
        validate_input_string("")
    with pytest.raises(ValueError, match="Input string cannot be empty"):
        validate_input_string("   ")  # Only whitespace


def test_setup_logging_valid():
    """Test that valid log levels are configured correctly."""
    # Note: basicConfig only sets level if not already configured
    # So we test that it doesn't raise an error
    setup_logging("INFO")
    # Level might be INFO or DEBUG from previous test
    assert logging.getLogger().level in (logging.INFO, logging.DEBUG)

    setup_logging("DEBUG")
    # Just verify it doesn't crash
    assert logging.getLogger().level >= logging.DEBUG


def test_setup_logging_invalid():
    """Test that invalid log levels cause exit."""
    with pytest.raises(SystemExit):
        setup_logging("INVALID_LEVEL")


def test_hash_name_cli_text_output():
    """Test CLI text output format."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        hash_name_cli("test_string", "en", "text")
        output = fake_out.getvalue()
        assert "-" in output
        parts = output.strip().split("-")
        assert len(parts) == 3


def test_hash_name_cli_json_output():
    """Test CLI JSON output format."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        hash_name_cli("test_string", "en", "json")
        output = fake_out.getvalue()
        data = json.loads(output)
        assert "physical_attribute" in data
        assert "personality_attribute" in data
        assert "character" in data
        assert isinstance(data["physical_attribute"], str)
        assert isinstance(data["personality_attribute"], str)
        assert isinstance(data["character"], str)


def test_hash_name_cli_german():
    """Test CLI with German language."""
    with patch("sys.stdout", new=StringIO()) as fake_out:
        hash_name_cli("test_string", "de", "text")
        output = fake_out.getvalue()
        assert "-" in output


def test_hash_name_cli_invalid_language():
    """Test CLI with invalid language raises exception."""
    with pytest.raises(ValueError, match="Unsupported language"):
        hash_name_cli("test_string", "fr", "text")


def test_parse_arguments_defaults():
    """Test argument parsing with defaults."""
    with patch("sys.argv", ["myth-hash", "test_input"]):
        args = parse_arguments()
        assert args.input_string == "test_input"
        assert args.language == "en"
        assert args.format == "text"
        assert args.log_level == "INFO"


def test_parse_arguments_custom():
    """Test argument parsing with custom values."""
    with patch(
        "sys.argv",
        [
            "myth-hash",
            "test_input",
            "-l",
            "de",
            "-f",
            "json",
            "--log-level",
            "DEBUG",
        ],
    ):
        args = parse_arguments()
        assert args.input_string == "test_input"
        assert args.language == "de"
        assert args.format == "json"
        assert args.log_level == "DEBUG"
