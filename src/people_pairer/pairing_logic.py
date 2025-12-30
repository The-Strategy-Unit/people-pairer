from typing import Iterable, Set, FrozenSet
from people_pairer.utils import setup_logger
import pandas as pd

logger = setup_logger(__name__, level="INFO")


def extract_forbidden_pairs(
    past_pairing_dfs: Iterable[pd.DataFrame | None],
) -> Set[FrozenSet[str]]:
    forbidden = set()
    if len(past_pairing_dfs) > 0:
        for df in past_pairing_dfs:
            for _, row in df.iterrows():
                forbidden.add(frozenset([row["email_1"], row["email_2"]]))
    return forbidden


def generate_pairs_avoiding_history(
    participants: pd.DataFrame,
    previous_pairings: Iterable[pd.DataFrame],
    max_attempts: int = 2000,
) -> pd.DataFrame:
    logger.info(f"🍐🧮 Starting pair generation with {max_attempts} max attempts...")
    if len(participants) % 2 != 0:
        raise ValueError("Number of participants must be even")

    # Early impossibility check
    if participants["team"].value_counts().max() > len(participants) // 2:
        raise ValueError("Impossible to pair: one team is too large")

    forbidden_pairs = extract_forbidden_pairs(previous_pairings)

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
        "Could not generate valid pairs without same-team or previous matches"
    )
