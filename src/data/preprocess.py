from src.utils.config_loader import load_config
import pandas as pd
from sklearn.model_selection import train_test_split
import os


def main():
    config = load_config("configs/data_config.yaml")

   # Load data (Hardcoded to match the DVC pipeline dependency)
    df = pd.read_csv("data/raw/validated.csv")

    # 🔥 CRITICAL FIX 1: Clean column names
    df.columns = df.columns.str.strip()

    # 🔥 CRITICAL FIX 2: Ensure target column exists
    if "Class" not in df.columns:
        raise ValueError(f"'Class' column not found. Available columns: {df.columns.tolist()}")

    # Split features and target
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=config["split"]["test_size"],
        random_state=config["split"]["random_state"],
        stratify=y if config["split"]["stratify"] else None
    )

    # Combine back for saving
    train = X_train.copy()
    train["Class"] = y_train

    test = X_test.copy()
    test["Class"] = y_test

    # 🔥 Ensure output directory exists
    os.makedirs(os.path.dirname(config["data"]["train_path"]), exist_ok=True)

    # Save files
    train.to_csv(config["data"]["train_path"], index=False)
    test.to_csv(config["data"]["test_path"], index=False)

    print(f"✅ Preprocessing complete. Train shape: {train.shape}, Test shape: {test.shape}")


if __name__ == "__main__":
    main()