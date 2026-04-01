import pandas as pd

def main():
    df = pd.read_csv("data/raw/data.csv")

    # basic validation
    assert not df.isnull().sum().any(), "Missing values found"

    df.to_csv("data/raw/validated.csv", index=False)

if __name__ == "__main__":
    main()