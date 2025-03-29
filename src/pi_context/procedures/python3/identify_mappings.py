import pandas as pd

from bdikit.schema_matching.one2one.contrastivelearning import ContrastiveLearningSchemaMatcher


def identify_mappings(
        primary_df: pd.DataFrame,
        secondary_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identifies a set of column mappings between two dataframes.

    Parameters:
        primary_df (pd.DataFrame): The primary dataframe.
        secondary_df (pd.DataFrame): The secondary dataframe.

    Returns:
        pd.DataFrame: A DataFrame containing the mapping results with columns "primary" and "secondary".
    """
    matcher_instance = ContrastiveLearningSchemaMatcher()

    matches = matcher_instance.map(secondary_df, primary_df)

    return pd.DataFrame(matches.items(), columns=["secondary", "primary"])

column_mappings = identify_mappings({{ primary_dataframe }}, {{ secondary_dataframe }})
column_mappings
