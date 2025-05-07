from typing import Optional, List
import pandas as pd

from bdikit.schema_matching.topk.contrastivelearning import CLTopkSchemaMatcher


def top_matches(
        source: pd.DataFrame,
        target: pd.DataFrame,
        top_k: int = 10,
) -> pd.DataFrame:
    """
    Returns the top-k matches between the source and target tables.

    Args:
        source (pd.DataFrame): The source table.
        target (pd.DataFrame): The target table.
        columns (Optional[List[str]], optional): The list of columns to consider for matching. Defaults to None.
        top_k (int, optional): The number of top matches to return. Defaults to 10.

    Returns:
        pd.DataFrame: A DataFrame containing the top-k matches between the source and target tables.
    """
    selected_columns = source

    topk_matcher = CLTopkSchemaMatcher()

    top_k_matches = topk_matcher.get_recommendations(
        selected_columns, target=target, top_k=top_k
    )

    dfs = []
    for match in top_k_matches:
        matches = pd.DataFrame(match["top_k_columns"], columns=["target", "similarity"])
        matches["source"] = match["source_column"]
        matches = matches[["source", "target", "similarity"]]  # reorder columns
        dfs.append(matches.sort_values(by="similarity", ascending=False))

    return pd.concat(dfs, ignore_index=True)

top_matches = top_matches({{ source_df }}, {{ target_df }})
top_matches.to_markdown()
