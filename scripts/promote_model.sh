#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/promote_model.sh nb
#   ./scripts/promote_model.sh logreg

MODEL_NAME="${1:-}"

if [[ -z "$MODEL_NAME" ]]; then
  echo "Usage: $0 <model_name>"
  echo "Example: $0 nb"
  exit 1
fi

MODEL_BUILD_DIR="training/models"
MODEL_REPO_DIR="model_repo"

SOURCE_PATH="${MODEL_BUILD_DIR}/model-${MODEL_NAME}.joblib"
TARGET_PATH="${MODEL_REPO_DIR}/model.joblib"
TEMP_PATH="${MODEL_REPO_DIR}/model.joblib.tmp"

# Check source exists
if [[ ! -f "$SOURCE_PATH" ]]; then
  echo "❌ Model artifact not found: $SOURCE_PATH"
  exit 1
fi

# Ensure model_repo exists
mkdir -p "$MODEL_REPO_DIR"

echo "Promoting model: $MODEL_NAME"
echo "From: $SOURCE_PATH"
echo "To:   $TARGET_PATH"

# Atomic copy (copy → move) to avoid application loading a partially copied model
cp "$SOURCE_PATH" "$TEMP_PATH"
mv "$TEMP_PATH" "$TARGET_PATH"

echo "✅ Promotion complete."
echo "You may now run CI/CD to reload the model."
