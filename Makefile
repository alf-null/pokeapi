SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON = python3.8
PROJECT = pokeapi
isort = isort $(PROJECT) tests setup.py
black = black -S -l 79 --target-version py38 $(PROJECT) tests setup.py


all: test

venv:
	$(PYTHON) -m venv --prompt $(PROJECT) venv
	pip install -qU pip

install:
	pip install -qU -r requirements.txt

install-test: install
	pip install -qU -r requirements-test.txt

test: clean lint

format:
	$(isort)
	$(black)

lint:
	flake8 $(PROJECT) tests setup.py
	$(isort) --check-only
	$(black) --check

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf *.egg-info

.PHONY: all install-test test format lint clean