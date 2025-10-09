import shutil
from pathlib import Path

import nox

nox.options.sessions = ["check", "test"]
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True
nox.options.default_venv_backend = "venv"
# Allow nox to find Python versions via pyenv
nox.options.error_on_missing_interpreters = False

PYTHON_SOURCE = Path(__file__).parent
EXCLUDE_DIRS = {"build", "dist", ".git", ".venv", ".nox", "__pycache__"}
PYTHON_FILES = [
    str(file)
    for file in PYTHON_SOURCE.rglob("*.py")
    if not any(exclude in file.parts for exclude in EXCLUDE_DIRS)
]
MYPY_FILES = [
    str(file)
    for file in (PYTHON_SOURCE / "myth_hash").rglob("*.py")
    if not any(exclude in file.parts for exclude in EXCLUDE_DIRS)
]


def install_with_poetry(session):
    """Helper function to install dependencies with Poetry."""
    # Install poetry into the nox virtualenv
    session.run("python", "-m", "pip", "install", "poetry", external=True)
    session.run("poetry", "install", external=True)


@nox.session(python=["3.11", "3.12", "3.13", "3.14", "3.14t"])
def test(session):
    """Run the test suite (excluding slow tests)."""
    install_with_poetry(session)

    session.log("Running tests with pytest (excluding slow tests)")
    session.run(
        "poetry",
        "run",
        "pytest",
        "-m",
        "not slow",
        "--cov=myth_hash",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "tests/",
        *session.posargs,
        external=True,
    )


@nox.session(python=["3.14"])
def test_slow(session):
    """Run only the slow tests."""
    install_with_poetry(session)

    session.log("Running slow tests with pytest")
    session.run(
        "poetry",
        "run",
        "pytest",
        "-m",
        "slow",
        "--cov=myth_hash",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "tests/",
        *session.posargs,
        external=True,
    )


@nox.session(python="3.14")
def check_format(session):
    """Check code formatting with black and isort."""
    install_with_poetry(session)
    session.run("poetry", "run", "black", "--check", str(PYTHON_SOURCE), external=True)
    session.run("poetry", "run", "isort", "--check-only", *PYTHON_FILES, external=True)


@nox.session(python="3.14")
def format_files(session):
    """Format code with black and isort."""
    install_with_poetry(session)
    session.run("poetry", "run", "black", str(PYTHON_SOURCE), external=True)
    session.run("poetry", "run", "isort", *PYTHON_FILES, external=True)


@nox.session(python="3.14")
def mypy(session):
    """Run type checking with mypy."""
    install_with_poetry(session)
    session.run("poetry", "run", "mypy", *MYPY_FILES, external=True)


@nox.session(python="3.14")
def pylint(session):
    """Run linting with pylint."""
    install_with_poetry(session)
    session.run("poetry", "run", "pylint", *PYTHON_FILES, external=True)


@nox.session(python="3.14")
def bandit(session):
    """Run security checks with bandit."""
    install_with_poetry(session)
    session.run("poetry", "run", "bandit", "-r", "myth_hash/", external=True)


@nox.session(python="3.14")
def upgrade_syntax(session):
    """Upgrade syntax with pyupgrade."""
    install_with_poetry(session)
    session.run(
        "poetry", "run", "pyupgrade", "--py311-plus", *PYTHON_FILES, external=True
    )


@nox.session(python="3.14")
def check(session):
    """Run all checks (format, types, linting, security)."""
    session.notify("check_format")
    session.notify("mypy")
    session.notify("pylint")
    session.notify("bandit")


@nox.session
def clean(session):
    """Clean up temporary files and directories."""
    session.log("Cleaning up temporary files and directories")

    folders_to_clean = [
        "build",
        "dist",
        ".nox",
        ".pytest_cache",
        "htmlcov",
        "__pycache__",
        ".mypy_cache",
        ".coverage",
        "coverage.xml",
    ]

    folders_to_clean.extend(str(folder) for folder in PYTHON_SOURCE.glob("*.egg-info"))

    for folder_name in folders_to_clean:
        folder_path = PYTHON_SOURCE / folder_name
        if folder_path.exists():
            session.log(f"Removing {folder_path}")
            shutil.rmtree(folder_path, ignore_errors=True)

    for pattern in ["*.pyc", "*.pyo", "*.pyd", "*.so", "*~"]:
        for path in PYTHON_SOURCE.rglob(pattern):
            session.log(f"Removing {path}")
            try:
                path.unlink()
            except (PermissionError, FileNotFoundError) as e:
                session.log(f"Error removing {path}: {e}")
