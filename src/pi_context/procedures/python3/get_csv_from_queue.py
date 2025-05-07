from typing import Optional, List

# Use strings instead of literals for None in CSV name as the LLM will be passing strings
def get_csv_from_queue(exclude_csvs: Optional[List[str]] = None, remove_csv: Optional[str] = "None") -> str:
    exclude_csvs = exclude_csvs or []

    if remove_csv is not "None":
        # Clear CSV from queue
        try:
            globals()['waiting_csvs'].remove(remove_csv)
        except ValueError:
            pass

    # Return first file that is not excluded.
    for filename in globals()['waiting_csvs']:
        if filename not in exclude_csvs:
            return filename
    return "None"


get_csv_from_queue({{ exclude_csvs }}, "{{remove_csv}}")
