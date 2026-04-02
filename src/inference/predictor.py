import joblib
import pandas as pd
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

# ✅ KServe standard: S3 models are mounted to /mnt/models
# We use an absolute path to avoid the relative path errors seen in logs.
MODEL_PATH = os.getenv("MODEL_PATH", "/mnt/models/model.joblib")

model = None

# ------------------------------
# MODEL LOADING (Executed at Startup)
# ------------------------------
def load_model():
    global model
    print(f"🔍 Attempting to load model from: {MODEL_PATH}")
    
    try:
        # Check if the file exists
        if not os.path.exists(MODEL_PATH):
            # PRO-TIP: List directory contents to debug "silly" path issues in logs
            parent_dir = os.path.dirname(MODEL_PATH)
            if os.path.exists(parent_dir):
                print(f"📂 Contents of {parent_dir}: {os.listdir(parent_dir)}")
            else:
                print(f"⚠️ Parent directory {parent_dir} does not exist.")
            
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully into memory")

    except Exception as e:
        print(f"❌ FATAL: Model loading failed: {str(e)}")
        # In production, we want the container to crash if the model is missing
        # so Kubernetes knows the pod is not healthy.
        raise RuntimeError(f"Model loading failed: {e}")

# Trigger loading
load_model()

# ------------------------------
# KSERVE / KUBERNETES ENDPOINTS
# ------------------------------

@app.get("/ready")
@app.get("/healthz") # Standard k8s health check path
def ready():
    """Confirms the container is up and model is in memory."""
    if model is not None:
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Model not loaded")


@app.get("/")
def health():
    """Basic root check."""
    return {"status": "ok", "model_path": MODEL_PATH}


# ------------------------------
# PREDICTION LOGIC
# ------------------------------

@app.post("/predict")
def predict(data: dict):
    """
    Expects JSON: {"features": [val1, val2, ...]}
    """
    try:
        if model is None:
            raise RuntimeError("Model is not initialized")

        if "features" not in data:
            raise ValueError("Missing 'features' key in request body")

        features = data["features"]

        if not isinstance(features, list):
            raise ValueError("Features must be a list of numerical values")

        # Convert to DataFrame: Sklearn expects a 2D array-like input
        df = pd.DataFrame([features])

        # Perform inference
        prediction = model.predict(df)
        
        # Log success for observability
        print(f"✅ Prediction successful: {prediction[0]}")

        return {
            "prediction": int(prediction[0]),
            "status": "success"
        }

    except Exception as e:
        print(f"⚠️ Prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))