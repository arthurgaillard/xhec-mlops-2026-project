# Pydantic models for the web service

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class InputData(BaseModel):
    """Physical measurements of one abalone, scaled as in the Kaggle dataset.

    Lengths (mm) and weights (grams) are divided by 200, e.g. a length of 91 mm
    is sent as 0.455.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "sex": "M",
                    "length": 0.455,
                    "diameter": 0.365,
                    "height": 0.095,
                    "whole_weight": 0.514,
                    "shucked_weight": 0.2245,
                    "viscera_weight": 0.101,
                    "shell_weight": 0.15,
                }
            ]
        }
    )

    sex: Literal["M", "F", "I"] = Field(
        description="M (male), F (female) or I (infant)"
    )
    length: float = Field(gt=0, description="Longest shell measurement")
    diameter: float = Field(gt=0, description="Perpendicular to length")
    height: float = Field(gt=0, description="With meat in shell")
    whole_weight: float = Field(gt=0, description="Whole abalone")
    shucked_weight: float = Field(gt=0, description="Weight of meat")
    viscera_weight: float = Field(gt=0, description="Gut weight (after bleeding)")
    shell_weight: float = Field(gt=0, description="After being dried")


class PredictionOut(BaseModel):
    """Predicted number of rings and the corresponding age."""

    rings: float = Field(description="Predicted number of shell rings")
    age: float = Field(description="Predicted age in years (rings + 1.5)")
