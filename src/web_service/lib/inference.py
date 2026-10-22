# Inference: turn an API payload into model features and predict the age

from sklearn.base import RegressorMixin
from sklearn.feature_extraction import DictVectorizer

from src.web_service.lib.models import InputData, PredictionOut

# Number of years to add to the number of rings to get the age of an abalone
RINGS_TO_AGE_OFFSET = 1.5

# Maps the API field names to the column names the model was trained on
FIELD_TO_COLUMN = {
    "sex": "Sex",
    "length": "Length",
    "diameter": "Diameter",
    "height": "Height",
    "whole_weight": "Whole weight",
    "shucked_weight": "Shucked weight",
    "viscera_weight": "Viscera weight",
    "shell_weight": "Shell weight",
}


def run_inference(
    input_data: InputData, dv: DictVectorizer, model: RegressorMixin
) -> PredictionOut:
    """Encode the input with the fitted DictVectorizer and predict the age."""
    record = {
        FIELD_TO_COLUMN[field]: value
        for field, value in input_data.model_dump().items()
    }
    x = dv.transform([record])
    rings = float(model.predict(x)[0])
    return PredictionOut(
        rings=round(rings, 2), age=round(rings + RINGS_TO_AGE_OFFSET, 2)
    )
