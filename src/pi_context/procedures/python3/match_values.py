from typing import Dict, Any

import pandas as pd
from pandas import DataFrame

from bdikit.value_matching.polyfuzz import TFIDFValueMatcher


def should_match_domains(
        primary_domain: pd.DataFrame,
        secondary_domain: pd.DataFrame,
) -> bool:
    # Check domains are not null
    if primary_domain is None or secondary_domain is None:
        return False

    # Check that there are values to match
    if len(primary_domain) == 0 or len(secondary_domain) == 0:
        return False

    return True


def match_values(
        primary_df: pd.DataFrame,
        secondary_df: pd.DataFrame,
        primary_column: str,
        secondary_column: str,
) -> DataFrame | None:
    value_matcher = TFIDFValueMatcher()

    if ("unmapped" in primary_column.lower()) or ("unmapped" in secondary_column.lower()):
        return

    # Select domains to perform value match within
    primary_domain = primary_df[primary_column].unique()
    secondary_domain = secondary_df[secondary_column].unique()

    if not should_match_domains(primary_domain, secondary_domain):
        return

    # Remove blank spaces and map to the original unique values
    primary_values_dict: Dict[str, str] = {str(x).strip(): x for x in primary_domain}
    secondary_values_dict: Dict[str, str] = {str(x).strip(): x for x in secondary_domain}

    raw_matches = value_matcher.match(list(secondary_values_dict.keys()), list(primary_values_dict.keys()))

    primary_values = []
    secondary_values = []
    similarities = []

    for secondary_value, primary_value, similarity in raw_matches:
        primary_values.append(primary_value)
        secondary_values.append(secondary_value)
        similarities.append(similarity)

    matches = pd.DataFrame({secondary_column: secondary_values, primary_column: primary_values}, index=None)

    return matches

value_matches = match_values({{ primary_dataframe }}, {{ secondary_dataframe }}, "{{ primary_column }}", "{{ secondary_column }}")
value_matches.to_markdown()
