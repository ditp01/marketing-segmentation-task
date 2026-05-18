from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd

DEFAULT_DATA_PATH = Path("data/raw/marketing_campaign.csv")


def detect_delimiter(file_path: Path) -> str:
    """Infer the CSV delimiter using a small file sample."""
    sample = file_path.read_text(encoding="utf-8", errors="ignore")[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
        return dialect.delimiter
    except csv.Error:
        # Fall back to semicolon if present; otherwise use comma.
        return ";" if ";" in sample else ","


def load_marketing_data(data_path: Path | str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load the marketing dataset from disk without mutating source data."""
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    delimiter = detect_delimiter(path)
    dataframe = pd.read_csv(path, sep=delimiter)
    return dataframe
