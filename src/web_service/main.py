# Code with FastAPI (app = FastAPI(...))

from pathlib import Path

from fastapi import FastAPI

from src.web_service.lib.inference import run_inference
from src.web_service.lib.models import InputData, PredictionOut
from src.web_service.utils import load_object

LOCAL_OBJECTS_DIR = Path(__file__).resolve().parent / "local_objects"
MODEL_PATH = LOCAL_OBJECTS_DIR / "model.pkl"
DV_PATH = LOCAL_OBJECTS_DIR / "dv.pkl"

app = FastAPI(
    title="Abalone Age Prediction API",
    description="Predict the age of an abalone from its physical measurements.",
)

dv = load_object(DV_PATH)
model = load_object(MODEL_PATH)


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(payload: InputData) -> PredictionOut:
    """Predict the number of rings and the age of an abalone."""
    return run_inference(payload, dv, model)
