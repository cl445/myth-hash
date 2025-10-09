# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
