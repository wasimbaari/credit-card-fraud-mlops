import joblib
import pandas as pd
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# ✅ MUST BE ABSOLUTE: KServe mounts S3 data here
MODEL_PATH = os.getenv("MODEL_PATH", "/mnt/models/model.joblib")

model = None

def load_model():
    global model
    print(f"🔍 Attempting to load model from: {MODEL_PATH}")
    try:
        if not os.path.exists(MODEL_PATH):
            parent_dir = os.path.dirname(MODEL_PATH)
            if os.path.exists(parent_dir):
                print(f"📂 Contents of {parent_dir}: {os.listdir(parent_dir)}")
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully into memory")
    except Exception as e:
        print(f"❌ FATAL: Model loading failed: {str(e)}")
        raise RuntimeError(f"Model loading failed: {e}")

load_model()

@app.get("/ready")
@app.get("/healthz")
def ready():
    if model is not None: return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Model not loaded")

@app.post("/predict")
def predict(data: dict):
    try:
        features = data["features"]
        df = pd.DataFrame([features])
        prediction = model.predict(df)
        return {"prediction": int(prediction[0]), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))