from src.utils.mlflow_utils import setup_mlflow
import pandas as pd
from xgboost import XGBClassifier
import joblib
import mlflow
import mlflow.sklearn
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def main():
    base_config = load_config("configs/base.yaml")
setup_mlflow(base_config)
    # Load data
    X_train = pd.read_csv("data/processed/X_train.csv")
    y_train = pd.read_csv("data/processed/y_train.csv").squeeze()

    X_test = pd.read_csv("data/processed/X_test.csv")
    y_test = pd.read_csv("data/processed/y_test.csv").squeeze()
    with mlflow.start_run():

        # 🔹 Log parameters
        mlflow.log_params(config["xgboost"])

        # 🔹 Train model
        model = XGBClassifier(
            n_estimators=config["xgboost"]["n_estimators"],
            max_depth=config["xgboost"]["max_depth"],
            learning_rate=config["xgboost"]["learning_rate"]
        )

        model.fit(X_train, y_train)

        # 🔹 Predictions
        preds = model.predict(X_test)

        # 🔹 Metrics
        accuracy = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds)
        recall = recall_score(y_test, preds)
        f1 = f1_score(y_test, preds)

        # 🔹 Log metrics
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        # 🔹 Save model
        joblib.dump(model, "models/model.joblib")

        # 🔹 Log model
        mlflow.sklearn.log_model(model, "model")

        print("✅ Training + Evaluation complete (single MLflow run)")
        print({
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        })


if __name__ == "__main__":
    main()