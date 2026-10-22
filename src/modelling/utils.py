# This module contains the functions to save and load python objects (model, encoder) with pickle.
import pickle
from pathlib import Path
from typing import Any

from prefect import task


@task
def pickle_object(obj: Any, file_path: str) -> None:
    """Save a python object to a file using pickle"""
    path = Path(file_path)
    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as file:
        pickle.dump(obj, file)


def load_pickle(file_path: str) -> Any:
    """Load a python object from a pickle file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No such file: '{file_path}'")
    with open(path, "rb") as file:
        return pickle.load(file)
