from typing import Iterable, Set, FrozenSet
from people_pairer.utils import setup_logger
import pandas as pd

logger = setup_logger(__name__, level="INFO")


def extract_forbidden_pairs(
    past_pairing_dfs: Iterable[pd.DataFrame | None],
) -> Set[FrozenSet[str]]:
    """Parses past pairings so we can ensure they are not repeated

    Args:
        past_pairing_dfs (Iterable[pd.DataFrame | None]): List of past pairing dataframes. Can be empty if no past pairings

    Returns:
        Set[FrozenSet[str]]: Set containing past pairs to be avoided
    """
    forbidden = set()
    if len(past_pairing_dfs) > 0:
        for df in past_pairing_dfs:
            for _, row in df.iterrows():
                forbidden.add(frozenset([row["email_1"], row["email_2"]]))
    return forbidden


def generate_pairs_avoiding_history(
    participants: pd.DataFrame,
    past_pairing_dfs: Iterable[pd.DataFrame | None],
    max_attempts: int = 5000,
) -> pd.DataFrame:
    """Generates pairs, ensuring that pairs have not been seen before and that pairs do not belong to the same team.

    Args:
        participants (pd.DataFrame): DataFrame with participants to pair, with columns name, email and team
        past_pairing_dfs (Iterable[pd.DataFrame  |  None]): List of dataframes with past pairings
        max_attempts (int, optional): Number of attempts to generate pairings meeting all conditions. Defaults to 2000.

    Raises:
        ValueError: Number of participants to pair must be even
        ValueError: Because participants cannot be in the same team, no teams can be larger than 50% of participant total
        RuntimeError: Unable to generate pairings meeting conditions in the given number of max attempts

    Returns:
        pd.DataFrame: New pairings meeting all conditions
    """
    logger.info(f"🧮 Starting pair generation with {max_attempts} max attempts...")
    if len(participants) % 2 != 0:
        raise ValueError("Number of participants must be even")

    # Early impossibility check
    if participants["team"].value_counts().max() > len(participants) // 2:
        raise ValueError("Impossible to pair: one team is too large")

    forbidden_pairs = extract_forbidden_pairs(past_pairing_dfs)

    for _ in range(max_attempts):
        shuffled = participants.sample(frac=1).reset_index(drop=True)

        pairs = []
        valid = True

        for i in range(0, len(shuffled), 2):
            p1 = shuffled.iloc[i]
            p2 = shuffled.iloc[i + 1]

            # same team?
            if p1["team"] == p2["team"]:
                valid = False
                break

            # seen before?
            if frozenset([p1["email"], p2["email"]]) in forbidden_pairs:
                valid = False
                break

            pairs.append(
                {
                    "name_1": p1["name"],
                    "email_1": p1["email"],
                    "team_1": p1["team"],
                    "name_2": p2["name"],
                    "email_2": p2["email"],
                    "team_2": p2["team"],
                }
            )

        if valid:
            logger.info(f"🥳 Pairing successful after {_} attempts")
            return pd.DataFrame(pairs)

    raise RuntimeError(
        f"Could not generate valid pairs without same-team or previous matches in {max_attempts} iterations"
    )
