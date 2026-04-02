import joblib
import pandas as pd
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# 🛡️ FORCE ABSOLUTE PATH
# KServe mounts S3 storage to /mnt/models
MODEL_BASE_PATH = "/mnt/models"
MODEL_FILE = "model.joblib"
MODEL_PATH = os.path.join(MODEL_BASE_PATH, MODEL_FILE)

model = None

# --- DEBUGGING: SCAN DIRECTORY ---
print(f"🔍 Checking for model at: {MODEL_PATH}")
try:
    if os.path.exists(MODEL_BASE_PATH):
        # This will list everything KServe downloaded from S3
        content = os.listdir(MODEL_BASE_PATH)
        print(f"📂 Directory {MODEL_BASE_PATH} contains: {content}")
    else:
        print(f"❌ {MODEL_BASE_PATH} does not exist yet. Check storage-initializer logs.")
except Exception as e:
    print(f"⚠️ Could not scan directory: {e}")
# ---------------------------------

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"✅ SUCCESS: Model loaded successfully from {MODEL_PATH}")
    else:
        # Check if it's nested (S3 sometimes downloads into a subfolder)
        nested_path = os.path.join(MODEL_BASE_PATH, "model", MODEL_FILE)
        if os.path.exists(nested_path):
            model = joblib.load(nested_path)
            print(f"✅ SUCCESS: Model loaded from nested path {nested_path}")
        else:
            print(f"❌ FATAL: model.joblib not found in {MODEL_BASE_PATH}")
            # Raising an error here forces the pod to Error/Restart 
            # so you can see this message in the logs.
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

except Exception as e:
    print(f"❌ FATAL: Error during model loading: {str(e)}")
    # We raise a RuntimeError so the pod enters CrashLoopBackOff 
    # instead of staying 'Running' but being broken inside.
    raise RuntimeError(e)

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
        
        # Scikit-learn expects a 2D array/DataFrame
        df = pd.DataFrame([features])
        prediction = model.predict(df)
        
        return {"prediction": int(prediction[0])}
    
    except Exception as e:
        print(f"⚠️ Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))