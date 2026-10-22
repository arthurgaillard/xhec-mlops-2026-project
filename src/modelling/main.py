# This module is the training flow: it reads the data, preprocesses it, trains a model and saves it.

import argparse
from pathlib import Path

from predicting import evaluate_model, predict_rings
from preprocessing import extract_x_y, filter_outliers, load_data
from sklearn.model_selection import train_test_split
from training import RANDOM_STATE, train_model
from utils import pickle_object

TEST_SIZE = 0.2
LOCAL_OBJECTS_DIR = (
    Path(__file__).resolve().parents[1] / "web_service" / "local_objects"
)
MODEL_PATH = LOCAL_OBJECTS_DIR / "model.pkl"
DV_PATH = LOCAL_OBJECTS_DIR / "dv.pkl"


def main(trainset_path: Path) -> None:
    """Train a model using the data at the given path and save the model (pickle)."""
    # Read data
    df = filter_outliers(load_data(trainset_path))
    train_df, test_df = train_test_split(
        df, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    # Preprocess data
    x_train, y_train, dv = extract_x_y(train_df)
    x_test, y_test, _ = extract_x_y(test_df, dv=dv)

    # (Optional) Pickle encoder if need be
    pickle_object(dv, DV_PATH)

    # Train model
    model = train_model(x_train, y_train)
    test_rmse = evaluate_model(y_test, predict_rings(x_test, model))
    print(f"Test RMSE: {test_rmse:.2f}")

    # Pickle model --> The model should be saved in pkl format the `src/web_service/local_objects` folder
    pickle_object(model, MODEL_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model using the data at the given path."
    )
    parser.add_argument("trainset_path", type=str, help="Path to the training set")
    args = parser.parse_args()
    main(Path(args.trainset_path))
