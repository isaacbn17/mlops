# Setup Guide (One-Time)

This project requires a **one-time setup with internet access**. After completing this setup,
all labs can be run **offline** (assuming images and Python wheels are cached).

---

## Supported environment (recommended)
- **Python 3.11**
- Docker Desktop **or** Rancher Desktop
- git

We provide two dependency files:
- **requirements.txt** (pinned, supported) ✅
- **requirements-novers.txt** (experimental, unsupported) ⚠️

Instructor support is for the pinned environment only.

---

## Tool installation

### 1. Git
Most systems already have git.

Check:
  git --version

If not installed:
- macOS: https://git-scm.com/download/mac
- Windows: https://git-scm.com/download/win
- Linux: use your distro package manager

run 'git init' to establish a git repository

---

### 2. Python 3.11
Check:
  python --version

If you are using **pyenv** (recommended):
  pyenv install 3.11.9
  pyenv local 3.11.9

Direct installers:
- macOS / Windows: https://www.python.org/downloads/release/python-3119/
- Linux: use your distro package manager or pyenv

Ensure pyenv is configured in your shell setup file (.bashrc/.zshrc)
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

---

### 3. Container runtime (choose ONE)

#### Option A: Docker Desktop
- Works on macOS and Windows
- Requires a free Docker account

Download:
https://www.docker.com/products/docker-desktop/

After install:
- Launch Docker Desktop
- Wait until it reports “Docker is running”

Verify:
  docker --version
  docker compose version

---

#### Option B: Rancher Desktop (no account required)
- Works on macOS, Windows, and Linux
- No licensing/account requirements

Download:
https://rancherdesktop.io/

After install:
- Launch Rancher Desktop
- Ensure the application status is **Running**
- Container runtime should be Docker-compatible (`dockerd`)

Verify:
  docker --version
  docker compose version

---

## Install Python dependencies

### Option A (macOS/Linux): quick setup via Makefile
From the project root:
  make setup

### Option B (Windows or no make): manual setup

PowerShell:
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  python -m pip install -U pip
  python -m pip install -r requirements.txt

macOS/Linux:
  python -m venv .venv
  source .venv/bin/activate
  pip install -U pip
  pip install -r requirements.txt

---

## Verify installation (recommended)

Run:
  ./env-check.sh

This verifies:
- Python imports
- Docker daemon is running
- MLflow starts via docker compose

If this is failing, see KNOWN_ISSUES.md to help with troubleshooting.

You will also need to activate the local virtual environment by running:
	source .venv/bin/activate

