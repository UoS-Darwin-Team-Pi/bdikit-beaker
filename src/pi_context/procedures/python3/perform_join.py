from typing import Dict
import pandas as pd

def perform_join(
        primary_df: pd.DataFrame,
        secondary_df: pd.DataFrame,
        column_mappings: Dict,
) -> pd.DataFrame:
    primary_cols = []
    secondary_cols = []

    for mapping in column_mappings:
        if ("unmapped" not in mapping["primary"].lower()) and ("unmapped" not in mapping["secondary"].lower()):
            primary_cols.append(mapping["primary"])
            secondary_cols.append(mapping["secondary"])
        if mapping.get("matches"):
            for match in mapping["matches"]:
                secondary_df[mapping["secondary"]].replace(match["secondary"], match["primary"], inplace=True)

    joined_df = pd.merge(
        primary_df,
        secondary_df,
        how="outer",
        left_on=primary_cols,
        right_on=secondary_cols,
    )

    joined_df.to_csv("harmonized.csv", index=False)

    return joined_df

joined_df = perform_join({{ primary_dataframe }}, {{ secondary_dataframe }}, {{ column_mappings }})
joined_df.to_markdown()
