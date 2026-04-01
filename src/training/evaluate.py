import pandas as pd
import joblib
from sklearn.metrics import classification_report
import json
import os


def main():
    model = joblib.load("models/model.joblib")

    X_test = pd.read_csv("data/processed/X_test.csv")
    y_test = pd.read_csv("data/processed/y_test.csv").squeeze()

    preds = model.predict(X_test)

    report = classification_report(y_test, preds, output_dict=True)

    # 🔥 create reports folder
    os.makedirs("reports", exist_ok=True)

    # 🔥 save file (THIS WAS MISSING)
    with open("reports/metrics.json", "w") as f:
        json.dump(report, f, indent=4)

    print("✅ Evaluation complete & metrics saved")


if __name__ == "__main__":
    main()