# ---------- Base image ----------
FROM python:3.12-slim AS base
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv globally (instead of pip)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files (pyproject.toml, uv.lock if available)
COPY pyproject.toml uv.lock* README.md ./

# Install dependencies in a cached layer
RUN uv sync --frozen --no-dev

# Copy app source
COPY . /app


EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.fridge_app_backend.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
