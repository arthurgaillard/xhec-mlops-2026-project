# This module contains the functions to make predictions and evaluate the model.
import numpy as np
import scipy.sparse
from prefect import task
from sklearn.base import RegressorMixin
from sklearn.metrics import root_mean_squared_error


@task
def predict_rings(
    input_data: scipy.sparse.csr_matrix, model: RegressorMixin
) -> np.ndarray:
    """Predict the number of rings of the abalones."""
    return model.predict(input_data)


@task
def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute the RMSE of the predictions."""
    return root_mean_squared_error(y_true, y_pred)
