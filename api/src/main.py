# api/src/main.py
from fastapi import FastAPI, Response, status, HTTPException
from src.schema import PredictRequest, PredictResponse
import joblib
import os

# baked-in path inside the image
MODEL_PATH = "/app/model/model.joblib"
VERSION_PATH = "/app/model/VERSION"

app = FastAPI(title="MLOps Service")

# Load model once at startup (fail fast if missing)
model = None
model_version = None
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH} inside image")
    model = joblib.load(MODEL_PATH)
    if os.path.exists(VERSION_PATH):
        try:
            with open(VERSION_PATH, "r") as f:
                model_version = f.read().strip()
        except Exception:
            model_version = None
    print("Model loaded successfully. version:", model_version)
except Exception as e:
    # Print a clear error for logs and leave model = None
    print("ERROR loading model at startup:", e)
    model = None
    model_version = None

def _check_model_loaded():
    """
    Raises a 503 error if the model isn't loaded. Otherwise, return.
    """
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded in image")

@app.get("/health")
def health():
    """
    Health returns 200 only if model is loaded into the image.
    Otherwise returns 503 so orchestrators / students see model missing.
    """
    _check_model_loaded()
    return {"status": "ok", "model_version": model_version}

@app.head("/health")
def health_head():
    _check_model_loaded()
    return Response(status_code=status.HTTP_200_OK)


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    _check_model_loaded()
    text = (req.subject or "") + " " + (req.message or "")
    label = model.predict([text])[0]
    score = None
    if hasattr(model, "predict_proba"):
        score = float(model.predict_proba([text])[0].max())
    return PredictResponse(label=str(label), score=score, model_version=model_version)
