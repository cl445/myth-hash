import json
import subprocess
from pathlib import Path

import pytest

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
