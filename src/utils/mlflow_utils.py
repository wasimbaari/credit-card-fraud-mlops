import mlflow
import os


def setup_mlflow(config):
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

    if not tracking_uri:
        raise ValueError("MLFLOW_TRACKING_URI not set")

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(config["mlflow"]["experiment_name"])