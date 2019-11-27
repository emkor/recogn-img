all: ut build dl_model e2e
docker: dl_model docker-x86-cpu-aio
config: clean venv install

PY3 = python3
VENV = .venv/recogn-img
VENV_PY3 = $(VENV)/bin/python3

CLASSES_FILE_URL = https://f001.backblazeb2.com/file/ml-model/keras_darknet_yolov3_2019_09_29_coco_classes.txt
MODEL_FILE_URL = https://f001.backblazeb2.com/file/ml-model/keras_darknet_yolov3_2019_09_30.h5.zip

clean:
	@echo "---- Cleaning cache and temporary files ----"
	@rm -rf $(VENV) build dist *.egg-info .mypy_cache .pytest_cache .coverage

venv:
	@echo "---- Re-installing virtualenv ----"
	@mkdir -p $(VENV)
	@$(PY3) -m venv $(VENV)

install:
	@echo "---- Installing dependencies and app itself in editable mode ----"
	@$(VENV_PY3) -m pip install --upgrade pip
	@$(VENV_PY3) -m pip install -e .[dev]

ut:
	@echo "---- Unit testing ---- "
	@$(VENV_PY3) -m mypy ./recogn_img
	@$(VENV_PY3) -m pytest -v --cov=./recogn_img ./recogn_img/test/unit

build:
	@echo "---- Building package ---- "
	@rm -rf ./dist/*
	@$(VENV_PY3) setup.py sdist bdist_wheel --python-tag py3 --dist-dir ./dist

dl_model:
	@echo "---- Downloading classes and model if not cached... ----"
	@if [ ! -f "coco_classes.txt" ]; then wget -O "coco_classes.txt" $(CLASSES_FILE_URL); fi
	@if [ ! -f "yolov3.h5" ]; then wget -O yolov3.h5.zip $(MODEL_FILE_URL) && unzip yolov3.h5.zip && rm yolov3.h5.zip; fi

docker-x86-cpu-aio:
	@echo "---- Building docker image... ----"
	@docker build -t "recogn-img:x86-cpu-aio" -f Dockerfile .

e2e:
	@echo "---- E2E testing (requires downloaded model!) ---- "
	@$(VENV_PY3) -m pytest -v --cov=./recogn_img --cov-append ./recogn_img/test/e2e

.PHONY: venv install ut dl_model e2e build config all
