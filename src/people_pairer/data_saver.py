import pandas as pd
from people_pairer.utils import setup_logger
from people_pairer.data_loader import list_past_pairings
import os

logger = setup_logger(__name__, level="INFO")


def save_created_pairs(folder_name: str, new_pairs_df: pd.DataFrame):
    """Saves dataframe of newly created pairs to specified location

    Args:
        folder_name (str): Folder containing data
        new_pairs_df (pd.DataFrame): Newly created pairs to be saved as CSV
    """
    existing_files = list_past_pairings(folder_name)
    if len(existing_files) > 0:
        current_round = int(existing_files[-1].split("_")[-1].strip(".csv")) + 1
    else:
        current_round = 1
    filepath = os.path.join(folder_name, "pairings", f"round_{current_round}.csv")
    new_pairs_df.to_csv(filepath, encoding="utf-8-sig", index=False)
    logger.info(f"💾 New pairings saved at: {filepath}")
