# This module contains the functions to train the model.

import numpy as np
import scipy.sparse
from sklearn.base import RegressorMixin
from sklearn.ensemble import RandomForestRegressor

RANDOM_STATE = 42


def train_model(
    x_train: scipy.sparse.csr_matrix,
    y_train: np.ndarray,
    model: RegressorMixin | None = None,
) -> RegressorMixin:
    """Train a regression model (a random forest by default)."""
    if model is None:
        model = RandomForestRegressor(
            n_estimators=200, min_samples_leaf=5, random_state=RANDOM_STATE
        )
    model.fit(x_train, y_train)
    return model
