#!/usr/bin/env python3
"""
Evaluate deployed /predict endpoint on a CSV test file (numeric binary labels 0/1).

Usage:
    python scripts/eval_endpoint_numeric.py --test-file test_small.csv --url http://localhost:8080/predict

Expectations:
- CSV has a header with a column named "label" that contains 0 or 1.
- The service returns JSON with a top-level "label" field that is numeric (or a string that can be int-cast).
"""

import argparse
import sys
import time
import requests
import pandas as pd
from sklearn.metrics import f1_score, classification_report

def parse_args():
    p = argparse.ArgumentParser(description="Evaluate /predict endpoint (numeric labels 0/1).")
    p.add_argument("--test-file", "-t", required=True, help="Path to CSV test file")
    p.add_argument("--url", "-u", default="http://localhost:8080/predict", help="Full URL of predict endpoint")
    p.add_argument("--batch-delay", type=float, default=0.0, help="Seconds to wait between requests (throttle)")
    p.add_argument("--label-col", default="label", help="Column name with ground-truth numeric label (0/1)")
    p.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds")
    return p.parse_args()

def read_test_csv(path, label_col):
    df = pd.read_csv(path)
    if label_col not in df.columns:
        raise SystemExit(f"ERROR: label column '{label_col}' not found in {path}. Columns: {df.columns.tolist()}")
    return df

def call_predict(url, payload, timeout):
    try:
        resp = requests.post(url, json=payload, timeout=timeout)
    except Exception as e:
        return {"error": f"request failed: {e}"}
    if resp.status_code != 200:
        return {"error": f"status {resp.status_code}: {resp.text}"}
    try:
        return resp.json()
    except Exception as e:
        return {"error": f"invalid json response: {e}; body: {resp.text}"}

def extract_numeric_label_from_response(resp):
    """
    Expect resp to be a dict containing a 'label' key (numeric or numeric-string).
    Returns integer 0/1 or None on failure.
    """
    if not isinstance(resp, dict):
        return None
    if "label" not in resp:
        # also allow 'prediction' as alternate key
        if "prediction" in resp:
            raw = resp["prediction"]
        else:
            return None
    else:
        raw = resp["label"]
    try:
        # TODO: map this lable to an integer
        return int(raw)
    except Exception:
        # maybe the API returns nested or different format; give up gracefully
        return None

def main():
    args = parse_args()
    df = read_test_csv(args.test_file, args.label_col)
    url = args.url.rstrip()

    y_true = []
    y_pred = []
    errors = []

    total = len(df)
    print(f"Loaded {total} rows from {args.test_file}. Sending to {url}")

    for i, row in df.iterrows():
        payload = {
            "subject": row.get("subject", "") if "subject" in row and pd.notna(row.get("subject")) else "",
            "email_to": row.get("email_to", "") if "email_to" in row and pd.notna(row.get("email_to")) else "",
            "email_from": row.get("email_from", "") if "email_from" in row and pd.notna(row.get("email_from")) else "",
            "message": row.get("message", "") if "message" in row and pd.notna(row.get("message")) else "",
        }

        res = call_predict(url, payload, timeout=args.timeout)
        if "error" in res:
            errors.append((i, res["error"]))
            y_pred.append(None)
        else:
            pred_label = extract_numeric_label_from_response(res)
            if pred_label is None:
                errors.append((i, f"bad response format: {res}"))
                y_pred.append(None)
            else:
                y_pred.append(pred_label)

        # ground truth
        try:
            true_label = int(row[args.label_col])
        except Exception:
            errors.append((i, f"invalid ground truth label: {row[args.label_col]}"))
            y_pred[-1] = None
            y_true.append(None)
            continue
        y_true.append(true_label)

        if args.batch_delay and i < total - 1:
            time.sleep(args.batch_delay)

    # Filter out rows where prediction failed (None)
    paired = [(t, p) for t, p in zip(y_true, y_pred) if (t is not None and p is not None)]
    if not paired:
        print("No successful predictions to score. Errors:")
        for e in errors[:20]:
            print(e)
        sys.exit(2)

    y_true_f, y_pred_f = zip(*paired)

    # Compute binary F1 (pos_label=1)
    f1 = f1_score(y_true_f, y_pred_f, pos_label=1)
    print(f"\nF1 (pos_label=1): {f1:.3f}\n")
    print("Classification report:")
    print(classification_report(y_true_f, y_pred_f, digits=3))

    # Summary
    total_sent = len(y_true)
    successful = sum(1 for p in y_pred if p is not None)
    failed = total_sent - successful
    print(f"\nSummary: total={total_sent} successful={successful} failed={failed}")

    if errors:
        print(f"\nErrors (showing up to 10):")
        for idx, err in errors[:10]:
            print(f"- row {idx}: {err}")

if __name__ == "__main__":
    main()
