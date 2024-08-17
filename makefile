PYTHON_SOURCE = .
EXCLUDE_DIRS = build dist .git .venv
PYTHON_FILES := $(shell find $(PYTHON_SOURCE) $(foreach d,$(EXCLUDE_DIRS),-path ./$(d) -prune -o) -name '*.py' -print)
PYTHON_RUNTIME = python311

.PHONY: all bandit check check-format deploy-prod deploy-dev format install-deps install-dev-deps mypy pylint test upgrade-syntax

all: check

bandit:
	@echo "Running bandit"
	@poetry run bandit -r $(PYTHON_FILES)

check: check-format mypy pylint

check-format:
	@echo "Running black"
	@poetry run black --check $(PYTHON_SOURCE)
	@echo "Running isort"
	@poetry run isort --check-only $(PYTHON_FILES)

format:
	@echo "Running black"
	@poetry run black $(PYTHON_SOURCE)
	@echo "Running isort"
	@poetry run isort $(PYTHON_FILES)

install-deps:
	@echo "Installing dependencies"
	@poetry install --no-root

install-dev-deps:
	@echo "Installing dev dependencies"
	@poetry install

mypy:
	@echo "Running mypy"
	@poetry run mypy $(PYTHON_FILES)

upgrade-syntax:
	@echo "Upgrading syntax with pyupgrade"
	@poetry run pyupgrade --py311-plus $(PYTHON_FILES)

pylint:
	@echo "Running pylint"
	@poetry run pylint $(PYTHON_FILES)

test:
	@echo "Running tests"
	@poetry run pytest -W error $(PYTHON_FILES)