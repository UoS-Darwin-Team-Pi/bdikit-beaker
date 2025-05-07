from typing import List
import pandas as pd
import os
from setuptools import glob


def load_csvs(csv_paths: List[str]) -> List[str]:
    csv_files = []

    for csv_path in csv_paths:
        if os.path.isfile(csv_path) and csv_path.endswith(".csv"):
            file = os.path.basename(csv_path).replace(".csv", "")
            csv_files.append(file)
            globals()[file] = pd.read_csv(csv_path)
        elif os.path.isdir(csv_path):
            for csv_file in glob.glob(os.path.join(csv_path, "*.csv")):
                file = os.path.basename(csv_file).replace(".csv", "")
                csv_files.append(file)
                globals()[file] = pd.read_csv(csv_file)

    return csv_files


csv_files = load_csvs({{ csv_paths }})

globals()["waiting_csvs"] = csv_files

str(csv_files)
