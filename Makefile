# Makefile for Mini MLOps Capstone
# Commands under targets must start with '>'

.RECIPEPREFIX := >
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: setup up down ci deploy build-image

IMAGE_NAME ?= mlops-api
MODEL_REPO_DIR := model_repo
MODEL_JOBLIB := $(MODEL_REPO_DIR)/model.joblib
MODEL_VERSION_FILE := $(MODEL_REPO_DIR)/VERSION
MODEL_TAG := $(shell [ -f $(MODEL_VERSION_FILE) ] && cat $(MODEL_VERSION_FILE) || echo "latest")
FULL_IMAGE := $(IMAGE_NAME):$(MODEL_TAG)

setup:
> python -m venv .venv
> . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
> echo "✅ venv + deps installed."
> echo "Next: run ./env-check.sh."

up:
> docker compose up -d

down:
> docker compose down

build-image:
> if [ ! -f "$(MODEL_JOBLIB)" ]; then echo "ERROR: promoted model not found at $(MODEL_JOBLIB). Run promotion first."; exit 1; fi
> docker build --build-arg MODEL_TAG=$(MODEL_TAG) -t $(FULL_IMAGE) -f api/Dockerfile .

ci: build-image
> docker compose up -d api
> sleep 2
> curl -fs http://localhost:8080/health > /dev/null

deploy: ci
> docker compose up -d
