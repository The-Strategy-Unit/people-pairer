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
        return pd.read_csv(filename, encoding="utf-8-sig")
    except Exception:
        logger.exception("Failed to load CSV: %s", filename)
        raise


def load_participants(folder_name: str) -> pd.DataFrame:
    """Loads participants.csv file and filters to active participants only

    Args:
        folder_name (str): Folder containing participants.csv file

    Returns:
        pd.DataFrame: Pandas Dataframe of participants for pairing
    """
    logger.info("🍐 Loading pairing participants...")
    participants = load_csv(os.path.join(folder_name, "participants.csv"))
    return participants[participants["active"]]


def list_past_pairings(folder_name: str) -> list[str]:
    """Looks for past pairings in pairings subfolder. Past pairings should be in CSV format and following
    the naming convention round_1, round_2, round_3.

    Args:
        folder_name (str): Folder in which pairings subfolder is located

    Returns:
        list[str]: List of past pairing CSV files, if any. Returns empty list if no past pairings.
    """
    try:
        past_pairings = sorted(
            [
                os.path.join(folder_name, "pairings", file)
                for file in os.listdir(os.path.join(folder_name, "pairings"))
                if file.startswith("round_")
            ],
            key=lambda p: int(p.split("_")[-1].strip(".csv")),
        )
        logger.info(f"{len(past_pairings)} past pairings found")
        return past_pairings
    except Exception:
        logger.exception(f"Failed to find folder: {folder_name}")
        raise


def load_past_pairings(
    folder_name: str, past_pairings_to_consider: int = 3
) -> list[pd.DataFrame | None]:
    """Loads past pairings as dataframes, so that we can check that new pairings are not repeats

    Args:
        folder_name (str): Folder in which data is stored
        past_pairings_to_consider (int, optional): Number of past pairings to load. Defaults to 3.

    Returns:
        list[pd.DataFrame | None]: List of past pairing dataframes
    """
    logger.info("Loading past pairs...")
    past_pairings = list_past_pairings(folder_name)
    recent_pairings = past_pairings[-past_pairings_to_consider:]
    recent_pairing_dfs = []
    if len(recent_pairings) > 0:
        recent_pairing_dfs = [pd.read_csv(round_file) for round_file in recent_pairings]
    logger.info(f"🚫 Using last {len(recent_pairings)} as forbidden pairings")
    return recent_pairing_dfs
