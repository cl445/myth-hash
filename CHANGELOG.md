# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-11-03

### Added
- Python 3.15 support, including the free-threaded 3.15t build
- Dependabot configuration for GitHub Actions and `uv.lock` (monthly, grouped)
- `main()` and `parse_arguments()` accept an optional argument list

### Changed
- Migrated packaging from Poetry to uv: PEP 621 `[project]` metadata, `uv_build` backend, `uv.lock` and PEP 735 dependency groups
- Nox sessions now use the uv backend and install from `uv.lock`
- Replaced black, isort, pylint and pyupgrade with ruff (formatter and linter, including pydocstyle and flake8-annotations rules)
- Replaced mypy with pyrefly in strict mode; type checking now also covers the tests and the noxfile
- Updated GitHub Actions (checkout v7, setup-uv v10.3.3, action-gh-release v3)
- Release workflow checks that the tag matches the project version and runs the full check suite before publishing
- Added the free-threading trove classifier
- `CharacterDataLoader` initialisation is now guarded by a lock, so concurrent first use (e.g. on free-threaded Python) loads the data exactly once
- Package data is read via `importlib.resources`; the `*_FILE` constants now hold file names instead of absolute paths and `BASE_PATH` was removed
- The CLI takes its language choices from `SUPPORTED_LANGUAGES`
- Test suite converted from unittest to plain pytest; CLI tests call `main()` in-process instead of spawning a subprocess (coverage 91% → 99%)
- README: rewrote the collision section (no longer tied to version 0.1.0, explains the name space and when not to use Myth Hash as an identifier)
- CI runs all Python versions on Linux and only the oldest and newest on macOS and Windows

### Fixed
- Type annotations of `NominativAdjective.word_id` and `CharacterNoun.character_id` said `int`, but the IDs come from JSON keys and are `str`
- The CLI logged a failure twice when name generation raised an exception
- The "unsupported language" error listed the languages in random order
- Removed an unreachable invalid-log-level branch from `setup_logging`
- CLI tests failed on Windows because they started `python3` instead of the current interpreter and read the output with the console code page
- Release notes linked the full changelog against a hard-coded `v0.1.0`
- Renamed the misspelled test module `chracter_data_loader_test.py`

### Removed
- Codecov upload and badge: the repository was never activated on Codecov, so no report was ever received. Coverage is still printed in the CI log.

## [0.2.1] - 2025-10-09

### Added
- Automated release workflow with GitHub Actions
- PyPI trusted publishing support
- CHANGELOG.md for tracking changes
- Enhanced .gitignore with IDE, OS, and tool-specific entries

### Changed
- Improved .gitignore to include VS Code, macOS, Windows, Linux files
- Added Nox and Ruff cache directories to .gitignore

## [0.2.0] - 2025-10-09

### Added
- Comprehensive test suite with 67 tests (47 new tests)
- CLI unit tests achieving 74% coverage
- Complete test coverage for `words.py` (100%)
- Complete test coverage for `hash_util.py` (100%)
- Module, class, and function docstrings throughout codebase
- `py.typed` marker for type hint support
- Python 3.12, 3.13, and 3.14 support (including free-threaded 3.14t)
- Multi-OS testing in CI (Ubuntu, macOS, Windows)
- Automated release workflow

### Changed
- Increased test coverage from 62% to 91%
- Consolidated GitHub workflows (removed redundant `nox.yml`)
- Renamed workflow to "CI" for clarity
- Configured Nox to use `venv` backend
- Set Python 3.14 as development version
- Updated README badges (CI, coverage, black, mypy)
- Improved error messages with lazy logging
- Optimized CI with dependency caching

### Fixed
- Pylint issues: achieved 10.00/10 score
- All pylint checks enabled (only `line-too-long` disabled)
- Trailing whitespace in docstrings
- Broad exception handling with targeted disables

### Removed
- `myth_hash/core/__init__.py` (simplified imports)
- Redundant `nox.yml` workflow

## [0.1.0] - Initial Release

### Added
- Core functionality for generating fantasy character names
- Support for English and German languages
- CLI interface with text and JSON output
- Character data loader with singleton pattern
- Hash-based name generation
- Basic test suite
- GitHub Actions workflow with Nox
