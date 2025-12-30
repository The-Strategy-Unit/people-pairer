from people_pairer.utils import setup_logger
from people_pairer.data_loader import load_participants, load_past_pairings
from people_pairer.pairing_logic import generate_pairs_avoiding_history

logger = setup_logger(__name__, level="INFO")


def main():
    participants = load_participants()
    past_pairing_dfs = load_past_pairings()
    pairs = generate_pairs_avoiding_history(
        participants,
        previous_pairings=past_pairing_dfs,
    )
    print(pairs)
    logger.info("Application finished")


if __name__ == "__main__":
    main()
