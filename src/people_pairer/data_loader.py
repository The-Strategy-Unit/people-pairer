import pandas as pd


def csv_validator(filename: str) -> bool:
    if filename.endswith(".csv"):
        return True
    return False


def load_csv(filename: str) -> pd.DataFrame:
    with open(filename) as f:
        return pd.read_csv(f)
