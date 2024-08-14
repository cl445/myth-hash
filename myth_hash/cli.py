import argparse
import json
import logging

from myth_hash import hash_name


def setup_logging(log_level: str) -> None:
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")
    logging.basicConfig(level=numeric_level)


def hash_name_cli(input_string: str, language: str, output_format: str) -> None:
    try:
        physical_attr, personality_attr, character = hash_name(input_string, language)
    except Exception as e:
        logging.error(f"Failed to generate fantasy name: {e}")
        raise

    if output_format == "text":
        print(f"{physical_attr}-{personality_attr}-{character.replace(' ', '')}")
    elif output_format == "json":
        output = {
            "physical_attribute": physical_attr,
            "personality_attribute": personality_attr,
            "character": character,
        }
        print(json.dumps(output, ensure_ascii=False))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generates a fantasy name consisting of two character attributes and a mythical creature from a hash value of an input string."
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
        choices=["en", "de"],
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
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level. Default is INFO.",
    )

    return parser.parse_args()


def validate_input_string(input_string: str) -> None:
    if not input_string.strip():
        raise ValueError("Input string cannot be empty.")


def main():
    args = parse_arguments()

    setup_logging(args.log_level)

    try:
        validate_input_string(args.input_string)
        hash_name_cli(args.input_string, args.language, args.format)
    except ValueError as ve:
        logging.error(f"Input validation error: {ve}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
