import joblib


def load_model(path: str = "models/model.joblib"):
    model = joblib.load(path)
    return model