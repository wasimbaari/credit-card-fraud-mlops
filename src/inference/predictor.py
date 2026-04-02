import joblib
import pandas as pd
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# KServe mounts S3 here
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model.joblib") ✅

model = None


# ------------------------------
# MODEL LOADING
# ------------------------------
def load_model():
    global model

    print(f"🔍 Loading model from: {MODEL_PATH}")

    try:
        # Check mount directory
        if not os.path.exists("/mnt/models"):
            raise RuntimeError("❌ /mnt/models not found (storage-initializer failed)")

        # Debug: list files
        print(f"📂 /mnt/models contains: {os.listdir('/mnt/models')}")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")

    except Exception as e:
        print(f"❌ FATAL: {e}")
        raise RuntimeError(e)


# Load model at startup
load_model()


# ------------------------------
# READINESS
# ------------------------------
@app.get("/ready")
def ready():
    if model is not None:
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Model not loaded")


# ------------------------------
# HEALTH CHECK
# ------------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# ------------------------------
# PREDICTION
# ------------------------------
@app.post("/predict")
def predict(data: dict):
    try:
        if model is None:
            raise RuntimeError("Model not loaded")

        if "features" not in data:
            raise ValueError("Missing 'features' key")

        features = data["features"]

        if not isinstance(features, list):
            raise ValueError("Features must be a list")

        df = pd.DataFrame([features])
        prediction = model.predict(df)

        return {"prediction": int(prediction[0])}

    except Exception as e:
        print(f"⚠️ Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))