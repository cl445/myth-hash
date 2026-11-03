"""Command-line interface for Myth Hash."""

import argparse
import json
import logging
import sys

from myth_hash import hash_name
from myth_hash.core.hash_util import SUPPORTED_LANGUAGES

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logging(log_level: str) -> None:
    """Configure logging with the specified log level (one of ``LOG_LEVELS``)."""
    logging.basicConfig()
    logging.getLogger().setLevel(log_level)


def hash_name_cli(input_string: str, language: str, output_format: str) -> None:
    """Generate and output a fantasy name in the specified format."""
    physical_attr, personality_attr, character = hash_name(input_string, language)

    if output_format == "text":
        print(f"{physical_attr}-{personality_attr}-{character.replace(' ', '')}")
    elif output_format == "json":
        output = {
            "physical_attribute": physical_attr,
            "personality_attribute": personality_attr,
            "character": character,
        }
        print(json.dumps(output, ensure_ascii=False))


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments (defaults to ``sys.argv[1:]``)."""
    parser = argparse.ArgumentParser(
        description="Generates a fantasy name consisting of two character attributes and a mythical creature from a hash value of an input string.",
    )
    parser.add_argument(
        "input_string",
        type=str,
        help="Input string to hash and generate a fantasy name.",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="en",
        choices=sorted(SUPPORTED_LANGUAGES),
        help="Specify the output language. Supported languages: English (en) and German (de). Default is English.",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="text",
        choices=["text", "json"],
        help="Specify the output format. Choose between plain text (text) and JSON (json). Default is text.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=LOG_LEVELS,
        help="Set the logging level. Default is INFO.",
    )

    return parser.parse_args(argv)


def validate_input_string(input_string: str) -> None:
    """Validate that the input string is not empty."""
    if not input_string.strip():
        raise ValueError("Input string cannot be empty.")


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the CLI."""
    args = parse_arguments(argv)

    setup_logging(args.log_level)

    try:
        validate_input_string(args.input_string)
        hash_name_cli(args.input_string, args.language, args.format)
    except ValueError as ve:
        logging.error("Input validation error: %s", ve)
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        logging.error("Failed to generate fantasy name: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
