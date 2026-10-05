"""Load headered UNSW-NB15 partitions without changing their contents."""
from pathlib import Path
from typing import Literal

import pandas as pd

from src.utils import RAW_DATA_DIR


def load_dataset(
    split: Literal["training", "testing"] = "training",
    data_dir: str | Path = RAW_DATA_DIR,
) -> pd.DataFrame:
    """Read one official CSV partition, preserving raw rows and column values.

    This loader deliberately does not clean, concatenate, or preprocess data.
    Use only the training partition for exploratory decisions.
    """
    if split not in {"training", "testing"}:
        raise ValueError("split must be 'training' or 'testing'.")
    csv_path = Path(data_dir) / f"UNSW_NB15_{split}-set.csv"
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}. Download the headered partition "
            "and place it in data/raw/. See data/README.md."
        )
    try:
        dataframe = pd.read_csv(csv_path)
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
        raise ValueError(f"Cannot read CSV {csv_path}: {error}") from error
    if dataframe.empty:
        raise ValueError(f"Dataset contains no records: {csv_path}")
    if "label" not in dataframe.columns:
        raise ValueError(
            f"Missing 'label' column in {csv_path}. Use the headered training/testing "
            "partition, not the original UNSW-NB15_1.csv through _4.csv files."
        )
    if dataframe["label"].isna().any() or not dataframe["label"].isin([0, 1]).all():
        raise ValueError(f"Expected 'label' values 0 (normal) or 1 (attack): {csv_path}")
    return dataframe
