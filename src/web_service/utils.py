# Utils file: helpers to load the pickled objects used by the web service

import pickle
from pathlib import Path
from typing import Any


def load_object(file_path: Path) -> Any:
    """Load a python object from a pickle file."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"No such file: '{file_path}'. "
            "Train the model first with `uv run python src/modelling/main.py`."
        )
    with open(file_path, "rb") as file:
        return pickle.load(file)
