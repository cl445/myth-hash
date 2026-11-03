# Myth Hash

[![CI](https://github.com/cl445/myth-hash/actions/workflows/test.yml/badge.svg)](https://github.com/cl445/myth-hash/actions/workflows/test.yml)
[![Python Versions](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14%20%7C%203.15-blue)](https://www.python.org)
[![License](https://img.shields.io/github/license/cl445/myth-hash.svg)](https://github.com/cl445/myth-hash/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Type checked: pyrefly (strict)](https://img.shields.io/badge/types-pyrefly%20strict-blue)](https://pyrefly.org/)

`Myth Hash` is a Python package designed to create human-readable hashes that are not only functional but also cognitively engaging. A key feature of this tool is its multilingual support, enabling the generation of hashes in multiple languages. The concept behind these human-readable hashes is to enhance communication and recognition by creating hashes that form vivid, memorable mental images. The goal is to make the hash as human-compatible as possible, ensuring it effectively serves its purpose in an intuitive and user-friendly manner.

## Features

- **Character Name Generation:** Generates a unique fantasy name based on an input string.
- **Supported Languages:** Currently supports English (`en`) and German (`de`).
- **CLI Support:** Easily generate names via the command line.
- **Library Usage:** Integrate `Myth Hash` into your Python projects.
- **Customizable Data:** Modify the included JSON files to customize the generated names.


## Requirements

- **Python:** 3.11, 3.12, 3.13, 3.14, 3.15 (including free-threaded 3.14t and 3.15t)
- **Platforms:** Linux, macOS, Windows

## Installation

You can install `Myth Hash` using pip:

```bash
pip install myth-hash
```

## Usage

### Command Line Interface (CLI)

After installing the package, you can use the myth-hash command to generate fantasy names.

Basic Example:
    
```bash
myth-hash "The moon whispered secrets, but only the cats understood." 
```
Example Output:
```bash
exotic-thoughtful-Griffin
```

### Using as a Library

You can also use Myth Hash within your Python code:

Example:
```python
import myth_hash

# Generate a character name using the hash_name function
name_parts = myth_hash.hash_name(
    "The moon whispered secrets, but only the cats understood.", "en"
)
print(name_parts)  # Output: ('exotic', 'thoughtful', 'Griffin')

# Access individual parts of the name
physical_attr, personality_attr, mystical_character = name_parts
print(f"Physical Attribute: {physical_attr}")
print(f"Personality Trait: {personality_attr}")
print(f"Mystical Character: {mystical_character}")
```
## Uniqueness and Collisions

A name is built from one of 259 physical attributes, one of 239 personality attributes and one of 153 creatures, so there are 9,470,853 possible names. That is a small space compared to a cryptographic hash, and different inputs will regularly map to the same name.

The slow test (`uv run nox -s test_slow`) hashes 1,000,000 distinct inputs and counts duplicates:

| Generated names | Duplicates | Uniqueness |
|----------------:|-----------:|-----------:|
| 1,000,000       | 119,949    | 88.0%      |

By the birthday problem, the chance of at least one collision is about 5% for 1,000 inputs and above 99% for 10,000 inputs.

Use Myth Hash to make values easy to recognize and talk about, for example in logs, dashboards or UIs, but not as a unique identifier. Keep the original hash around when you need to tell values apart reliably.

These numbers apply to the bundled word lists; adding entries to the JSON files enlarges the name space and lowers the collision rate.

## Future Improvements

 - **Improved Uniqueness:** Add more attributes and characters to reduce the likelihood of name collisions.
 - **Additional Languages:** Add support for more languages with help from the community.

## Development

The project uses [uv](https://docs.astral.sh/uv/) for dependency management and [Nox](https://nox.thea.codes/) as task runner.

```bash
uv sync                          # create .venv with all dev dependencies
uv run nox -s check              # ruff (format + lint), pyrefly (strict), bandit
uv run nox -s test-3.14          # tests with coverage on a single Python version
uv run nox -s test               # tests on all supported Python versions
uv run nox -s format_files       # auto-format and apply safe lint fixes
```

## Contributing

Contributions are welcome! Please fork the repository, create a new branch for your feature or bug fix, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.