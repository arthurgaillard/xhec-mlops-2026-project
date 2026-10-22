#!/bin/bash

# Entrypoint of the Docker image (see Dockerfile.app): starts the Prefect server
# in the background and the FastAPI app in the foreground.

prefect server start --host 0.0.0.0 --port 4201 &
exec uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001
