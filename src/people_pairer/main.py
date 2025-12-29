from people_pairer.utils import setup_logger
from people_pairer.data_loader import load_participants

logger = setup_logger(__name__, level="INFO")


def main():
    logger.info("🍐 Loading pairing participants...")

    ### PSEUDOCODE BELOW
    # Load past pairs (CSV)
    # Run matching
    # Output another CSV
    logger.info("Application finished")


if __name__ == "__main__":
    main()
