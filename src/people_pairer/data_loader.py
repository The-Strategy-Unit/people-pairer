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
            return pd.read_csv(f, encoding="utf-8-sig")
    except Exception:
        logger.exception("Failed to load CSV: %s", filename)
        raise


def load_participants(folder_name: str) -> pd.DataFrame:
    logger.info("🍐 Loading pairing participants...")
    participants = load_csv(os.path.join(folder_name, "participants.csv"))
    participants.columns = participants.columns.str.replace(
        "ï»¿", "", regex=False
    ).str.strip()  # Defending against CSV files with UTF-8 Byte Order Mark (BOM)
    return participants[participants["active"]]


def list_past_pairings(folder_name: str):
    try:
        past_pairings = sorted(
            [
                os.path.join(folder_name, "pairings", file)
                for file in os.listdir(os.path.join(folder_name, "pairings"))
                if file.startswith("round_")
            ]
        )
        logger.info(f"{len(past_pairings)} past pairings found")
        return past_pairings
    except Exception:
        logger.exception(f"Failed to find folder: {folder_name}")
        raise


def load_past_pairings(folder_name: str):
    logger.info("Loading past pairs...")
    past_pairings = list_past_pairings(folder_name)
    recent_pairings = past_pairings[-3:]
    recent_pairing_dfs = []
    if len(recent_pairings) > 0:
        recent_pairing_dfs = [pd.read_csv(round_file) for round_file in recent_pairings]
    logger.info(f"🚫 Using last {len(recent_pairings)} as forbidden pairings")
    return recent_pairing_dfs
