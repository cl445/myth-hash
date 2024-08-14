PYTHON_SOURCE = .
EXCLUDE_DIRS = experimental
PYTHON_FILES := $(shell find $(PYTHON_SOURCE) $(foreach d,$(EXCLUDE_DIRS),-path ./$(d) -prune -o) -name '*.py' -print)
PYTHON_RUNTIME = python311

.PHONY: all bandit check check-format deploy-prod deploy-dev flake format install-deps install-dev-deps mypy pylint test test-request

all: check

bandit:
	@echo "Running bandit"
	@bandit --configfile .bandit.yml -r $(PYTHON_FILES)

check: check-format mypy pylint

check-format:
	@echo "Running black"
	@black --check $(PYTHON_SOURCE)
	@echo "Running isort"
	@isort --check-only --profile black $(PYTHON_FILES)


flake:
	@echo "Running flake8"
	@flake8 --ignore=E203,W503 --max-line-length 120 $(PYTHON_FILES)

format:
	@echo "Running black"
	@black $(PYTHON_SOURCE)
	@echo "Running isort"
	@isort --profile black $(PYTHON_FILES)

install-deps:
	@echo "Installing dependencies"
	@pip install --upgrade --no-cache-dir -r requirements.txt

install-dev-deps:
	@echo "Installing dev dependencies"
	@pip install --upgrade --no-cache-dir -r requirements-dev.txt

mypy:
	@echo "Running mypy"
	@mypy --config-file .mypy.ini $(PYTHON_FILES)

upgrade-syntax:
	@echo "Upgrading syntax with pyupgrade"
	@pyupgrade --py311-plus $(PYTHON_FILES)

pylint:
	@echo "Running pylint"
	@pylint $(PYTHON_FILES)

test:
	@echo "Running tests"
	@pytest -W error PYTHON_FILES/

