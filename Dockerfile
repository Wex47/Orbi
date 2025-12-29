FROM python:3.11-slim

# Python hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal system deps
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Copy dependency manifests first (cache-friendly)
COPY pyproject.toml uv.lock ./

# Install dependencies into uv-managed virtualenv (.venv)
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Create log directory
RUN mkdir -p /app/logs

# Run Orbi using the virtualenv Python
ENTRYPOINT ["/app/.venv/bin/python", "-m", "app.main"]
