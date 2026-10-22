FROM python:3.12-slim

# Install uv to install the dependencies from uv.lock
COPY --from=ghcr.io/astral-sh/uv:0.11.12 /uv /bin/uv

WORKDIR /app

# Install the app dependencies first so this layer is cached between code changes
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the code and the trained model (src/web_service/local_objects/*.pkl)
COPY src ./src
COPY bin ./bin

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PREFECT_UI_API_URL="http://localhost:4200/api"

# API on 8001 and Prefect UI on 4201, mapped to 8000 and 4200 on the host
EXPOSE 8001 4201

CMD ["bash", "bin/run_services.sh"]
