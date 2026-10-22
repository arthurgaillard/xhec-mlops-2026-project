<div align="center">

# MLOps Project: Abalone Age Prediction

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)]()
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&logoColor=white)](.pre-commit-config.yaml)
</div>

## 👥 Team

| Name | GitHub |
|---|---|
| Arthur Gaillard | [@arthurgaillard](https://github.com/arthurgaillard) |
| Ziqi Meng | [@TabErica](https://github.com/TabErica) |
| Anaïs Storp | [@AnaisStorp](https://github.com/AnaisStorp) |
| Charles | [@coasensi](https://github.com/coasensi) |

## 🎯 Project Overview

The age of an abalone (a type of sea snail) is traditionally determined by cutting the shell, staining it and counting the rings under a microscope, which is slow and tedious. This project predicts the age from easy-to-obtain physical measurements (sex, size and weights) instead.

It turns a notebook model into a production-ready system:

- **Training pipeline**: a [Prefect](https://www.prefect.io/) flow that downloads the data, preprocesses it, trains a random forest and saves the model and encoder
- **Scheduled retraining**: a Prefect deployment that retrains the model every day
- **Prediction API**: a [FastAPI](https://fastapi.tiangolo.com/) REST API with Pydantic input validation
- **Docker**: one container running the API and the Prefect server

The data is the [Abalone dataset](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset) from Kaggle. It is downloaded automatically by the training pipeline. The model predicts the number of rings, and the age is `rings + 1.5` years.

## 📁 Project Structure

```
├── .github/workflows/ci.yaml   # CI: installs dependencies and runs pre-commit
├── bin/run_services.sh         # Entrypoint of the Docker image
├── Dockerfile.app              # Docker image of the API + Prefect server
├── notebooks/
│   ├── eda.ipynb               # Exploratory data analysis
│   └── modelling.ipynb         # Model experiments (tracked with MLflow)
├── src/
│   ├── modelling/              # Training pipeline (Prefect)
│   │   ├── main.py             # Training flow
│   │   ├── deployment.py       # Scheduled retraining deployment
│   │   ├── preprocessing.py
│   │   ├── training.py
│   │   ├── predicting.py
│   │   └── utils.py
│   └── web_service/            # Prediction API (FastAPI)
│       ├── main.py             # API endpoints
│       ├── utils.py
│       ├── lib/
│       │   ├── models.py       # Pydantic input/output models
│       │   └── inference.py
│       └── local_objects/      # Trained model and encoder (.pkl, created by training)
├── pyproject.toml              # Project dependencies
└── uv.lock                     # Pinned versions of all dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Docker](https://docs.docker.com/get-docker/) (to run the API in a container)

No Kaggle account is needed: the dataset is public and downloaded automatically.

### 1. Set up the environment

Clone the repository:
```bash
git clone https://github.com/arthurgaillard/xhec-mlops-2026-project.git
cd xhec-mlops-2026-project
```

Install uv if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux
```

Create the virtual environment and install all dependencies (app + dev):
```bash
uv sync
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
```

Install the pre-commit hooks (ruff linting/formatting and file checks run on every commit):
```bash
uv run pre-commit install
```

### 2. Train the model (Prefect)

1. Start a local Prefect server (keeps a UI + history of flow runs):
   ```bash
   uv run prefect server start
   ```
   Leave this running, then open the UI at <http://127.0.0.1:4200>.

2. In a second terminal, point Prefect to this server and run the training flow once:
   ```bash
   uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
   uv run python src/modelling/main.py
   ```
   You'll see the run appear under **Flows** / **Flow Runs** in the UI. The flow prints the test RMSE and saves `model.pkl` and `dv.pkl` (the encoder) in `src/web_service/local_objects/`.

3. To set up the scheduled retraining deployment instead:
   ```bash
   uv run python src/modelling/deployment.py
   ```
   This registers the `abalone-retrain` deployment with a daily cron schedule (every day at 02:00) and keeps running to execute it. New runs show up automatically in the UI.

4. To trigger the deployment manually (without waiting for the schedule), in another terminal:
   ```bash
   uv run prefect deployment run 'train-model-flow/abalone-retrain'
   ```

### 3. Run the API locally

The API loads the model trained in step 2, so run the training first.

```bash
uv run uvicorn src.web_service.main:app --reload
```

The API is available at <http://localhost:8000>, and the interactive documentation at <http://localhost:8000/docs>.

### 4. Run the API with Docker

The image contains the trained model, so run the training (step 2) before building it.

Build the image:
```bash
docker build -f Dockerfile.app -t abalone-api .
```

Run the container:
```bash
docker run --rm -p 0.0.0.0:8000:8001 -p 0.0.0.0:4200:4201 abalone-api
```

Inside the container, the API runs on port 8001 and the Prefect server on port 4201. They are available on your machine at:
- API: <http://localhost:8000> (documentation at <http://localhost:8000/docs>)
- Prefect UI: <http://localhost:4200>

Stop the local Prefect server from step 2 first, otherwise port 4200 is already in use.

## 🌐 Using the API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/predict` | Predict the number of rings and the age of an abalone |

The measurements are scaled as in the Kaggle dataset: lengths (mm) and weights (grams) are divided by 200. `sex` is `M` (male), `F` (female) or `I` (infant), and all measurements must be greater than 0.

Example request:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sex": "M",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
  }'
```

Example response (status `201`):
```json
{"rings": 10.47, "age": 11.97}
```

Invalid inputs (missing field, unknown sex, negative measurement) are rejected with status `422` and a message explaining the error.

You can also send requests from the interactive documentation at <http://localhost:8000/docs> ("Try it out").

## 🛠️ Development

### Managing dependencies

Dependencies are declared in `pyproject.toml` and their exact versions are pinned in `uv.lock` (uv's equivalent of `requirements.txt`). To add a package:

```bash
uv add <package>              # app dependency
uv add --dev <package>        # development-only dependency
```

`uv add` updates both `pyproject.toml` and `uv.lock`; commit both files.

### Code quality

- Pre-commit runs ruff (linting and formatting) and file checks on every commit. To run it on all files:
  ```bash
  uv run pre-commit run --all-files
  ```
- The CI (`.github/workflows/ci.yaml`) installs the dependencies and runs the same checks on every push and pull request, with Python 3.11 and 3.12.
