#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  echo "❌ .venv not found."
  echo "   Run: make setup"
  exit 1
fi

# Activate the virtual environment for this script
source .venv/bin/activate

echo "✅ Using Python: $(which python)"
python --version

echo "=== Environment Check ==="

command -v git >/dev/null 2>&1 || fail "git not found"
command -v python >/dev/null 2>&1 || fail "python not found"
command -v docker >/dev/null 2>&1 || fail "docker not found"
docker compose version >/dev/null 2>&1 || fail "docker compose not found"

echo "✅ CLI tools present"
python --version
git --version
docker --version

echo ""
echo "=== Python Package Check ==="
python - <<'PY'
import sys
required = ["mlflow","fastapi","sklearn","pandas","numpy","joblib"]
missing = []
for r in required:
    try:
        __import__(r)
    except Exception:
        missing.append(r)
if missing:
    print("Missing Python packages:", missing)
    raise SystemExit(1)
print("✅ Core Python packages import correctly")
PY

echo ""
echo "=== Docker Daemon Check ==="
docker info >/dev/null 2>&1 || fail "Docker daemon not reachable. Start Docker Desktop or Rancher Desktop."
echo "✅ Docker daemon reachable"


echo ""
echo "=== MLflow Compose Smoke Test ==="

if ! docker compose up -d mlflow >/dev/null 2>&1; then
  echo "❌ Failed to start mlflow via docker compose"
  echo "   Try: docker compose up -d mlflow"
  exit 1
fi

sleep 5

if ! curl -sf http://localhost:5000 >/dev/null 2>&1; then
  echo "❌ MLflow not reachable at http://localhost:5000"
  echo "   Common causes: port 5000 already in use, container failed to start"
  echo "   Debug: docker compose ps && docker compose logs mlflow"
  exit 1
fi

echo "✅ MLflow reachable at http://localhost:5000"
docker compose down

echo ""
echo "🎉 Environment looks good!"
