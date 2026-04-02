import joblib
import pandas as pd
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Model path matches the KServe volume mount
MODEL_PATH = os.getenv("MODEL_PATH", "/mnt/models/model.joblib")
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded successfully from {MODEL_PATH}")
    else:
        print(f"❌ Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")

@app.get("/ready")
def ready():
    if model is not None:
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Model not loaded")

@app.post("/predict")
def predict(data: dict):
    try:
        if "features" not in data:
            raise ValueError("Missing 'features' key in request body")
        
        features = data["features"]
        # Scikit-learn expects a DataFrame or 2D array
        df = pd.DataFrame([features])
        prediction = model.predict(df)
        
        return {"prediction": int(prediction[0])}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))