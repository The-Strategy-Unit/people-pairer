from people_pairer.utils import setup_logger
from people_pairer.data_loader import load_participants, load_past_pairings

logger = setup_logger(__name__, level="INFO")


def main():
    logger.info("🍐 Loading pairing participants...")
    participants = load_participants()
    ### PSEUDOCODE BELOW
    # Load past pairs (CSV)
    logger.info("Loading past pairs...")
    past_pairing_dfs = load_past_pairings()
    # Run matching
    # Output another CSV
    logger.info("Application finished")


if __name__ == "__main__":
    main()
