# This module contains the functions to load and preprocess the abalone data.

from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse
from sklearn.feature_extraction import DictVectorizer

TARGET = "Rings"
CATEGORICAL_COLS = ["Sex"]
NUMERICAL_COLS = [
    "Length",
    "Diameter",
    "Height",
    "Whole weight",
    "Shucked weight",
    "Viscera weight",
    "Shell weight",
]
MIN_HEIGHT = 0
MAX_HEIGHT = 0.4


def load_data(path: Path) -> pd.DataFrame:
    """Load the Abalone dataset from a CSV file."""
    return pd.read_csv(path)


def filter_outliers(
    df: pd.DataFrame, min_height: float = MIN_HEIGHT, max_height: float = MAX_HEIGHT
) -> pd.DataFrame:
    """Remove the abalones with a height of 0 or above the maximal height."""
    return df[(df["Height"] > min_height) & (df["Height"] <= max_height)].reset_index(
        drop=True
    )


def extract_x_y(
    df: pd.DataFrame,
    categorical_cols: list[str] | None = None,
    numerical_cols: list[str] | None = None,
    dv: DictVectorizer | None = None,
    with_target: bool = True,
) -> tuple[scipy.sparse.csr_matrix, np.ndarray | None, DictVectorizer]:
    """Extract X (and y) from the dataframe, fitting a DictVectorizer if none is given."""
    if categorical_cols is None:
        categorical_cols = CATEGORICAL_COLS
    if numerical_cols is None:
        numerical_cols = NUMERICAL_COLS
    dicts = df[categorical_cols + numerical_cols].to_dict(orient="records")

    if dv is None:
        dv = DictVectorizer()
        dv.fit(dicts)
    x = dv.transform(dicts)

    y = df[TARGET].values if with_target else None
    return x, y, dv
