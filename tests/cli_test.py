import json
import logging
from collections.abc import Iterator

import pytest

from myth_hash.cli import (
    hash_name_cli,
    main,
    parse_arguments,
    setup_logging,
    validate_input_string,
)

EXAMPLE = "The moon whispered secrets, but only the cats understood."


@pytest.fixture(autouse=True)
def restore_root_log_level() -> Iterator[None]:
    """Undo the log level that ``main()`` sets on the root logger."""
    root = logging.getLogger()
    level = root.level
    yield
    root.setLevel(level)


# End-to-end tests through main()


def test_default_language_text_output(capsys: pytest.CaptureFixture[str]) -> None:
    main([EXAMPLE])
    out, err = capsys.readouterr()
    assert out == "exotic-thoughtful-Griffin\n"
    assert not err


def test_default_language_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    main([EXAMPLE, "-f", "json"])
    out, _ = capsys.readouterr()
    assert json.loads(out) == {
        "physical_attribute": "exotic",
        "personality_attribute": "thoughtful",
        "character": "Griffin",
    }


def test_german_language_text_output(capsys: pytest.CaptureFixture[str]) -> None:
    main([EXAMPLE, "-l", "de"])
    out, _ = capsys.readouterr()
    assert out == "exotischer-nachdenklicher-Greif\n"


def test_german_language_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    main([EXAMPLE, "-l", "de", "-f", "json"])
    out, _ = capsys.readouterr()
    assert json.loads(out)["character"] == "Greif"


def test_empty_input_string(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main([""])
    assert exc_info.value.code == 1
    assert "Input validation error" in caplog.text


def test_unexpected_error_is_logged_once(
    caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*_args: object) -> tuple[str, str, str]:
        raise RuntimeError("boom")

    monkeypatch.setattr("myth_hash.cli.hash_name", fail)
    with pytest.raises(SystemExit) as exc_info:
        main(["example_name"])
    assert exc_info.value.code == 1
    assert [r.getMessage() for r in caplog.records] == [
        "Failed to generate fantasy name: boom"
    ]


def test_invalid_log_level(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["example_name", "--log-level", "INVALID"])
    assert exc_info.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_invalid_format(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["example_name", "-f", "invalid_format"])
    assert "argument -f/--format: invalid choice" in capsys.readouterr().err


def test_invalid_language(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(["example_name", "-l", "fr"])
    assert "argument -l/--language: invalid choice" in capsys.readouterr().err


@pytest.mark.parametrize("log_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
def test_log_levels(log_level: str, capsys: pytest.CaptureFixture[str]) -> None:
    main(["example_name", "--log-level", log_level])
    assert logging.getLogger().level == logging.getLevelNamesMapping()[log_level]
    out, err = capsys.readouterr()
    assert out.count("-") == 2
    assert not err


# Unit tests for CLI functions


def test_validate_input_string_valid() -> None:
    validate_input_string("test")
    validate_input_string("  test  ")


def test_validate_input_string_empty() -> None:
    with pytest.raises(ValueError, match="Input string cannot be empty"):
        validate_input_string("")
    with pytest.raises(ValueError, match="Input string cannot be empty"):
        validate_input_string("   ")


def test_setup_logging() -> None:
    setup_logging("WARNING")
    assert logging.getLogger().level == logging.WARNING


def test_hash_name_cli_text_output(capsys: pytest.CaptureFixture[str]) -> None:
    hash_name_cli("test_string", "en", "text")
    parts = capsys.readouterr().out.strip().split("-")
    assert len(parts) == 3


def test_hash_name_cli_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    hash_name_cli("test_string", "en", "json")
    data = json.loads(capsys.readouterr().out)
    assert set(data) == {"physical_attribute", "personality_attribute", "character"}
    assert all(isinstance(value, str) for value in data.values())


def test_hash_name_cli_invalid_language() -> None:
    with pytest.raises(ValueError, match="Unsupported language"):
        hash_name_cli("test_string", "fr", "text")


def test_parse_arguments_defaults() -> None:
    args = parse_arguments(["test_input"])
    assert args.input_string == "test_input"
    assert args.language == "en"
    assert args.format == "text"
    assert args.log_level == "INFO"


def test_parse_arguments_custom() -> None:
    args = parse_arguments(
        ["test_input", "-l", "de", "-f", "json", "--log-level", "DEBUG"]
    )
    assert args.input_string == "test_input"
    assert args.language == "de"
    assert args.format == "json"
    assert args.log_level == "DEBUG"
