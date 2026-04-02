import joblib
import pandas as pd
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# ✅ Use environment variable (Docker sets this)
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model.joblib")

model = None

# ------------------------------
# MODEL LOADING
# ------------------------------
print(f"🔍 Loading model from: {MODEL_PATH}")

try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")

except Exception as e:
    print(f"❌ FATAL: Model loading failed: {e}")
    raise RuntimeError(f"Model loading failed: {e}")


# ------------------------------
# READINESS ENDPOINT
# ------------------------------
@app.get("/ready")
def ready():
    if model is not None:
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Model not loaded")


# ------------------------------
# HEALTH CHECK (OPTIONAL BUT GOOD)
# ------------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# ------------------------------
# PREDICTION ENDPOINT
# ------------------------------
@app.post("/predict")
def predict(data: dict):
    try:
        if model is None:
            raise RuntimeError("Model not loaded")

        if "features" not in data:
            raise ValueError("Missing 'features' key in request body")

        features = data["features"]

        if not isinstance(features, list):
            raise ValueError("Features must be a list")

        # Convert to DataFrame (sklearn expects 2D)
        df = pd.DataFrame([features])

        prediction = model.predict(df)

        return {"prediction": int(prediction[0])}

    except Exception as e:
        print(f"⚠️ Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))