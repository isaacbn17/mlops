#!/usr/bin/env bash
set -euo pipefail

# usage: scripts/mlflow_promotion.sh [--run RUN_ID] [--exp EXP_NAME] [--metric METRIC]
RUN_ID=""
EXP_NAME="spam_experiments"
METRIC="macro_f1"
OUT=${OUT:-model_repo/model.joblib}
TRACKING_URI=${MLFLOW_TRACKING_URI:-http://localhost:5000}

while [[ $# -gt 0 ]]; do
  case $1 in
    --run) RUN_ID="$2"; shift 2;;
    --exp) EXP_NAME="$2"; shift 2;;
    --metric) METRIC="$2"; shift 2;;
    --out) OUT="$2"; shift 2;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

export MLFLOW_TRACKING_URI="$TRACKING_URI"

if [[ -n "$RUN_ID" ]]; then
  python scripts/promote_from_mlflow.py --run-id "$RUN_ID" --model-path model --out "$OUT"
else
  python scripts/promote_from_mlflow.py --experiment-name "$EXP_NAME" --metric "$METRIC" --maximize --model-path model --out "$OUT"
fi
