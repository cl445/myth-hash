import shutil
from pathlib import Path

import nox

nox.options.sessions = ["check", "test"]
nox.options.reuse_existing_virtualenvs = True
nox.options.stop_on_first_error = True

PYTHON_SOURCE = Path(__file__).parent
EXCLUDE_DIRS = {"build", "dist", ".git", ".venv", ".nox", "__pycache__"}
PYTHON_FILES = [
    str(file)
    for file in PYTHON_SOURCE.rglob("*.py")
    if not any(exclude in file.parts for exclude in EXCLUDE_DIRS)
]


@nox.session(python="python3.11")
def install_deps(session):
    session.log("Installing project dependencies")
    session.run("poetry", "install", "--no-root", external=True)


@nox.session(python="python3.11")
def install_dev_deps(session):
    session.log("Installing development dependencies")
    session.run("poetry", "install", "--with", "dev", external=True)


@nox.session(python="python3.11")
def check_format(session):
    session.log("Checking code formatting with black and isort")
    session.run("poetry", "run", "black", "--check", str(PYTHON_SOURCE), external=True)
    session.run("poetry", "run", "isort", "--check-only", *PYTHON_FILES, external=True)


@nox.session(python="python3.11")
def format_files(session):
    session.log("Formatting code with black and isort")
    session.run(
        "poetry", "run", "pyupgrade", "--py311-plus", *PYTHON_FILES, external=True
    )
    session.run("poetry", "run", "black", str(PYTHON_SOURCE), external=True)
    session.run("poetry", "run", "isort", *PYTHON_FILES, external=True)


@nox.session(python="python3.11")
def bandit(session):
    session.log("Running security checks with bandit")
    tests_dir = PYTHON_SOURCE / "tests"
    session.run(
        "poetry",
        "run",
        "bandit",
        "-r",
        *PYTHON_FILES,
        "--exclude",
        str(tests_dir),
        external=True,
    )


@nox.session(python="python3.11")
def mypy(session):
    session.log("Running type checks with mypy")
    session.run("poetry", "run", "mypy", *PYTHON_FILES, external=True)


@nox.session(python="python3.11")
def pylint(session):
    session.log("Running linting with pylint")
    session.run("poetry", "run", "pylint", *PYTHON_FILES, external=True)


@nox.session(python="python3.11")
def upgrade_syntax(session):
    session.log("Upgrading syntax with pyupgrade")
    session.run(
        "poetry", "run", "pyupgrade", "--py311-plus", *PYTHON_FILES, external=True
    )


@nox.session(python=["3.11", "3.12", "3.13"])
def test(session):
    session.log("Running tests with pytest")
    session.install("poetry")
    session.run("poetry", "env", "use", session.python, external=True)
    session.run("poetry", "install", external=True)
    tests_dir = PYTHON_SOURCE / "tests"
    session.run("poetry", "run", "pytest", "-W", "error", str(tests_dir), external=True)


@nox.session(python="python3.11")
def check(session):
    session.notify("check_format")
    session.notify("mypy")
    session.notify("pylint")
    session.notify("bandit")


@nox.session
def clean(session):
    session.log("Cleaning up temporary files and directories")

    folders_to_clean = [
        "build",
        "dist",
        ".nox",
        ".pytest_cache",
        "htmlcov",
        "__pycache__",
    ]

    folders_to_clean.extend(str(folder) for folder in PYTHON_SOURCE.glob("*.egg-info"))

    for folder_name in folders_to_clean:
        folder_path = PYTHON_SOURCE / folder_name
        if folder_path.exists():
            session.log(f"Removing {folder_path}")
            shutil.rmtree(folder_path, ignore_errors=True)

    for path in PYTHON_SOURCE.rglob("*.pyc"):
        session.log(f"Removing {path}")
        try:
            path.unlink()
        except PermissionError:
            session.log(f"Permission denied: {path}")

    for path in PYTHON_SOURCE.rglob("*.pyo"):
        session.log(f"Removing {path}")
        try:
            path.unlink()
        except PermissionError:
            session.log(f"Permission denied: {path}")
