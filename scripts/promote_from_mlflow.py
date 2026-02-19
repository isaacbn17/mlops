#!/usr/bin/env python3
"""
promote_from_mlflow.py

Usage:
  # promote best run in experiment to model_repo/model.joblib
  python tools/promote_from_mlflow.py --experiment-name spam_experiments --metric macro_f1 --maximize --model-path model --out model_repo/model.joblib

  # or promote specific run id
  python tools/promote_from_mlflow.py --run-id <run_id> --model-path model --out model_repo/model.joblib
"""

import argparse
import tempfile
import os
import shutil
import joblib
from mlflow.tracking import MlflowClient
import mlflow.sklearn

def find_best_run(client: MlflowClient, experiment_name: str, metric: str, maximize: bool=True):
    # find experiment id by name
    exps = client.search_experiments()
    exp = next((e for e in exps if e.name == experiment_name), None)
    if not exp:
        raise ValueError(f"Experiment named '{experiment_name}' not found. Available: {[e.name for e in exps]}")
    exp_id = exp.experiment_id

    runs = client.search_runs(experiment_ids=[exp_id], order_by=[f"metrics.{metric} DESC" if maximize else f"metrics.{metric} ASC"], max_results=100)
    if not runs:
        raise ValueError(f"No runs found in experiment {experiment_name}")
    return runs[0]

def promote(run_id: str, model_artifact_path: str, out_path: str, client: MlflowClient):
    # Download artifacts to temp dir (will download the model artifact tree)
    tmpdir = tempfile.mkdtemp(prefix="mlflow_promote_")
    try:
        client.download_artifacts(run_id=run_id, path=model_artifact_path, dst_path=tmpdir)
        # The downloaded artifact structure depends on how the model was logged.
        # If mlflow.sklearn.log_model(..., artifact_path="model"), the model files will be under tmpdir/model
        model_dir = os.path.join(tmpdir, model_artifact_path)
        if not os.path.exists(model_dir):
            # maybe downloaded root directly
            model_dir = tmpdir

        # load model via mlflow.sklearn.load_model using runs:/ URI so we get the model object
        # This works even if model_dir uses mlflow format
        model_ref = f"runs:/{run_id}/{model_artifact_path}"
        model = mlflow.sklearn.load_model(model_ref)

        # Ensure target dir exists
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        joblib.dump(model, out_path)
        print(f"Promoted run {run_id} -> {out_path}")
    finally:
        shutil.rmtree(tmpdir)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-id", default=None, help="Specific run id to promote")
    p.add_argument("--experiment-name", default=None, help="Experiment name to search for best run")
    p.add_argument("--metric", default="macro_f1", help="Metric to sort by when selecting best run")
    p.add_argument("--maximize", action="store_true", default=True, help="Maximize the metric when selecting best run")
    p.add_argument("--model-path", default="model", help="artifact path under the run where the model was logged")
    p.add_argument("--out", default="model_repo/model.joblib", help="output path to write the promoted joblib")
    p.add_argument("--tracking-uri", default=None, help="optional mlflow tracking uri (overrides env var)")
    args = p.parse_args()

    if args.tracking_uri:
        os.environ["MLFLOW_TRACKING_URI"] = args.tracking_uri

    client = MlflowClient()

    if args.run_id:
        run_id = args.run_id
    else:
        if not args.experiment_name:
            raise SystemExit("Either --run-id or --experiment-name must be provided")
        best = find_best_run(client, args.experiment_name, args.metric, maximize=args.maximize)
        run_id = best.info.run_id
        print(f"Selected run {run_id} (metrics: {best.data.metrics})")

    promote(run_id, args.model_path, args.out, client)

    # write provenance
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(os.path.join(os.path.dirname(args.out), "PROMOTED_RUN"), "w") as fh:
        fh.write(run_id + "\n")

if __name__ == "__main__":
    main()
