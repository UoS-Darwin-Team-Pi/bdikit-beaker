import pandas as pd

def save_join(path: str) -> bool:
    try:
        globals()["joined_df"].to_csv(path, index=False)
        return True
    except Exception:
        return False

save_join("{{ path }}")
globals()["joined_df"].head(5).to_markdown()
