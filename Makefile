# Makefile for Mini MLOps Capstone
# This Makefile avoids the TAB-only requirement by using a custom recipe prefix.
# Any command line under a target must start with the '>' character.

.RECIPEPREFIX := >
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: setup up down 

setup:
	python -m venv .venv
	@. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
	@echo "✅ venv + deps installed."
	@echo "Next: run ./env-check.sh."


up:
	docker compose up -d

down:
	docker compose down

