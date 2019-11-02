all: test build
config: venv install

PY3 = python3
VENV = .venv/recogn-img
VENV_PY3 = $(VENV)/bin/python3

venv:
	echo "---- Re-installing virtualenv ----"
	rm -rf $(VENV) && mkdir -p $(VENV)
	$(PY3) -m venv $(VENV)

install:
	echo "---- Installing dependencies and app itself in editable mode ----"
	$(VENV_PY3) -m pip install --upgrade pip
	$(VENV_PY3) -m pip install -e .[dev]

test:
	echo "---- Testing ---- "
	$(VENV_PY3) -m mypy --ignore-missing-imports ./recogn_img
	$(VENV_PY3) -m pytest -v --cov=./recogn_img ./recogn_img/test

build:
	echo "---- Building package ---- "
	$(VENV_PY3) setup.py sdist bdist_wheel --python-tag py3 --dist-dir ./dist

.PHONY: all config test build
