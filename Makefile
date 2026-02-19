# Makefile for Mini MLOps Capstone
# This Makefile avoids the TAB-only requirement by using a custom recipe prefix.
# Any command line under a target must start with the '>' character.

.RECIPEPREFIX := >
.SHELLFLAGS := -eu -o pipefail -c

# Basic targets
.PHONY: setup up down ci deploy build-image

# Tag images with model version info
IMAGE_NAME ?= mlops-api
MODEL_REPO_DIR := model_repo
MODEL_JOBLIB := $(MODEL_REPO_DIR)/model.joblib
MODEL_VERSION_FILE := $(MODEL_REPO_DIR)/VERSION
MODEL_TAG := $(shell [ -f $(MODEL_VERSION_FILE) ] && cat $(MODEL_VERSION_FILE) || echo "latest")
FULL_IMAGE := $(IMAGE_NAME):$(MODEL_TAG)

setup:
	python -m venv .venv
	@. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
	@echo "✅ venv + deps installed."
	@echo "Next: run ./env-check.sh."

up:
	docker compose up -d

down:
	docker compose down

# Build image that bakes the promoted model in. Fails early if no promoted model exists.
build-image:
	if [ ! -f "$(MODEL_JOBLIB)" ]; then echo "ERROR: promoted model not found at $(MODEL_JOBLIB). Run promotion first."; exit 1; fi
	docker build --build-arg MODEL_TAG=$(MODEL_TAG) -t $(FULL_IMAGE) -f api/Dockerfile .

# Continuous-integration smoke target:
# - ensure the image is built with the promoted model
# - bring up the api service and run simple smoke test (health only)
ci: build-image
	docker compose up -d api
	sleep 2
	curl -fs http://localhost:8080/health > /dev/null

# Deploy target (used by deploy_local.sh / git hook)
deploy: ci
	docker compose up -d
