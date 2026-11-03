"""Nox sessions for testing, linting and type checking."""

import shutil
from pathlib import Path

import nox

nox.options.sessions = ["check", "test"]
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True
nox.options.default_venv_backend = "uv"

PROJECT_ROOT = Path(__file__).parent
PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14", "3.15", "3.14t", "3.15t"]
DEFAULT_PYTHON = "3.14"


def sync_dependencies(session: nox.Session) -> None:
    """Install the project and its dev dependencies from uv.lock into the session venv."""
    session.run_install(
        "uv",
        "sync",
        "--locked",
        "--group=dev",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


def run_pytest(session: nox.Session, marker: str) -> None:
    """Run pytest with coverage for the tests matching the given marker expression."""
    sync_dependencies(session)
    session.run(
        "pytest",
        "-m",
        marker,
        "--cov=myth_hash",
        "--cov-report=term-missing",
        "tests/",
        *session.posargs,
    )


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run the test suite (excluding slow tests)."""
    run_pytest(session, "not slow")


@nox.session(python=DEFAULT_PYTHON)
def test_slow(session: nox.Session) -> None:
    """Run only the slow tests."""
    run_pytest(session, "slow")


@nox.session(python=DEFAULT_PYTHON)
def lint(session: nox.Session) -> None:
    """Check formatting and lint rules with ruff."""
    sync_dependencies(session)
    session.run("ruff", "format", "--check", ".")
    session.run("ruff", "check", ".")


@nox.session(python=DEFAULT_PYTHON)
def format_files(session: nox.Session) -> None:
    """Format code and apply safe lint fixes with ruff."""
    sync_dependencies(session)
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")


@nox.session(python=DEFAULT_PYTHON)
def typecheck(session: nox.Session) -> None:
    """Run strict type checking with pyrefly."""
    sync_dependencies(session)
    session.run("pyrefly", "check")


@nox.session(python=DEFAULT_PYTHON)
def bandit(session: nox.Session) -> None:
    """Run security checks with bandit."""
    sync_dependencies(session)
    session.run("bandit", "-c", "pyproject.toml", "-r", "myth_hash/")


@nox.session(python=False)
def check(session: nox.Session) -> None:
    """Run all checks (lint, types, security)."""
    session.notify("lint")
    session.notify("typecheck")
    session.notify("bandit")


@nox.session(python=False)
def clean(session: nox.Session) -> None:
    """Clean up temporary files and directories."""
    session.log("Cleaning up temporary files and directories")

    paths_to_clean = [
        "build",
        "dist",
        ".nox",
        ".pytest_cache",
        ".ruff_cache",
        "htmlcov",
        ".coverage",
        "coverage.xml",
    ]

    for name in paths_to_clean:
        path = PROJECT_ROOT / name
        if path.is_dir():
            session.log(f"Removing {path}")
            shutil.rmtree(path, ignore_errors=True)
        elif path.exists():
            session.log(f"Removing {path}")
            path.unlink()

    for cache_dir in PROJECT_ROOT.rglob("__pycache__"):
        if ".venv" not in cache_dir.parts:
            shutil.rmtree(cache_dir, ignore_errors=True)
