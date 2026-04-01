import pandas as pd
import os

def main():
    # 1. Read the data
    # Note: 'index_col=0' handles that leading comma/unnamed index
    df = pd.read_csv("data/external/creditcard.csv", index_col=0)
    
    # 2. Standardize the Target Column Name
    # We rename 'is_fraud' to 'Class' to match your downstream scripts
    if 'is_fraud' in df.columns:
        df.rename(columns={'is_fraud': 'Class'}, inplace=True)
        print("✅ Renamed 'is_fraud' to 'Class'")

    # 3. Save the standardized 'raw' data
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/data.csv", index=False)
    print(f"✅ Ingestion complete. Shape: {df.shape}")

if __name__ == "__main__":
    main()