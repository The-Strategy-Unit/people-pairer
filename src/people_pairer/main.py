import argparse
from people_pairer.utils import setup_logger
from people_pairer.data_loader import load_participants, load_past_pairings
from people_pairer.pairing_logic import generate_pairs_avoiding_history
from people_pairer.data_saver import save_created_pairs

logger = setup_logger(__name__, level="INFO")


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_filepath",
        help="Path to the folder containing the participants.csv and pairings subfolder. Defaults to data",
        type=str,
        default="data",
    )
    return parser.parse_args()


def main(folder_name: str = "data"):
    """Full people pairing pipeline. Loads participants, checks for past pairings, creates new pairings, and saves new pairings

    Args:
        folder_name (str, optional): Folder containing participants and past pairings as CSV files in pairings subfolder. Defaults to "data".
    """
    participants = load_participants(folder_name)
    past_pairing_dfs = load_past_pairings(folder_name)
    new_pairs_df = generate_pairs_avoiding_history(
        participants,
        past_pairing_dfs,
    )
    save_created_pairs(folder_name, new_pairs_df)
    logger.info("Application finished")


if __name__ == "__main__":
    args = parse_args()
    main(args.data_filepath)
