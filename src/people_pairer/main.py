from people_pairer.utils import setup_logger
from people_pairer.data_loader import csv_validator

logger = setup_logger(__name__, level="INFO")


def main():
    logger.info("Starting application")
    logger.info(csv_validator("data/active_participants.csv"))
    logger.info("Application finished")
    ### PSEUDOCODE BELOW
    # Load users for current iteration (CSV)
    # Load past pairs (CSV)
    # Run matching
    # Output another CSV


if __name__ == "__main__":
    main()
