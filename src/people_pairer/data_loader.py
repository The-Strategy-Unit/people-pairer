from people_pairer.utils import setup_logger
import pandas as pd
import os

logger = setup_logger(__name__, level="INFO")


def load_csv(filename: str) -> pd.DataFrame:
    """Loads CSV file

    Args:
        filename (str): CSV file to load

    Returns:
        pd.DataFrame: Contents of loaded CSV file
    """
    try:
        with open(filename) as f:
            return pd.read_csv(f, encoding="utf-8")
    except Exception:
        logger.exception("Failed to load CSV: %s", filename)
        raise


def load_participants() -> pd.DataFrame:
    participants = load_csv(os.path.join("data", "participants.csv"))
    return participants[participants["active"]]
