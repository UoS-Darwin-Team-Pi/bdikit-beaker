from typing import Dict
import pandas as pd

def perform_join(
        primary_df: pd.DataFrame,
        secondary_df: pd.DataFrame,
        column_mappings: Dict,
) -> pd.DataFrame:
    cols = []
    secondary = secondary_df.copy()

    for mapping in column_mappings:
        # Map secondary values to corresponding primary ones
        if mapping.get("matches"):
            for match in mapping["matches"]:
                secondary[mapping["secondary"]].replace(match["secondary"], match["primary"], inplace=True)

        # Add mapped columns to join list
        if ("unmapped" not in mapping["primary"].lower()) and ("unmapped" not in mapping["secondary"].lower()):
            cols.append(mapping["primary"])

            # Rename secondary DF columns to have same name as primary
            secondary.rename(columns={mapping["secondary"]: mapping["primary"]}, inplace=True)

    joined_df = pd.merge(
        primary_df,
        secondary,
        how="outer",
        on=cols,
    )

    joined_df.to_csv("harmonized.csv", index=False)

    return joined_df

joined_df = perform_join({{ primary_dataframe }}, {{ secondary_dataframe }}, {{ column_mappings }})
joined_df.to_markdown()
