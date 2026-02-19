# Makefile for Mini MLOps Capstone
# Commands under targets must start with '>'

.RECIPEPREFIX := >
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: ci deploy setup up down

setup:
> python -m venv .venv
> @. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
> @echo "✅ venv + deps installed."
> @echo "Next: run ./env-check.sh."

up:
> docker compose up -d

down:
> docker compose down

ci:
> docker compose build hello
> docker compose up -d hello
> sleep 2
> curl -fs http://localhost:8080 > /dev/null
> curl -fs http://localhost:8080/health > /dev/null
> curl -fs http://localhost:8080/hello > /dev/null

deploy: ci
> docker compose up -d --build hello
