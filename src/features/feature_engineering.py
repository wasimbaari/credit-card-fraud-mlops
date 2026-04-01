from src.utils.config_loader import load_config
import pandas as pd
from imblearn.over_sampling import SMOTE


def preprocess_features(df: pd.DataFrame):
    df = df.copy()

    # 1) Datetime → numeric (epoch seconds)
    if "trans_date_trans_time" in df.columns:
        df["trans_date_trans_time"] = pd.to_datetime(
            df["trans_date_trans_time"], errors="coerce"
        ).astype("int64") // 10**9  # seconds

    # 2) Convert all object columns → category codes (fast & simple)
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("category").cat.codes

    # 3) Safety: fill any NaNs (if any after conversion)
    df = df.fillna(0)

    return df


def main():
    config = load_config("configs/data_config.yaml")

    train = pd.read_csv(config["data"]["train_path"])
    test = pd.read_csv(config["data"]["test_path"])

    # Split
    X_train = train.drop("Class", axis=1)
    y_train = train["Class"]

    X_test = test.drop("Class", axis=1)
    y_test = test["Class"]

    # 🔥 Convert to numeric BEFORE SMOTE
    X_train = preprocess_features(X_train)
    X_test = preprocess_features(X_test)

    # 🔥 Apply SMOTE only on train
    if config["smote"]["enabled"]:
        print("Applying SMOTE...")
        smote = SMOTE(random_state=config["smote"]["random_state"])
        X_train, y_train = smote.fit_resample(X_train, y_train)

    # 🔥 Save aligned X and y
    X_train.to_csv("data/processed/X_train.csv", index=False)
    pd.Series(y_train).to_csv("data/processed/y_train.csv", index=False)

    X_test.to_csv("data/processed/X_test.csv", index=False)
    pd.Series(y_test).to_csv("data/processed/y_test.csv", index=False)

    print(f"✅ Features complete. Train shape: {X_train.shape}, Test shape: {X_test.shape}")


if __name__ == "__main__":
    main()