FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl (for uv installer)
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Copy lock + pyproject first for dependency caching
COPY pyproject.toml uv.lock ./

# Install deps from lockfile (no dev deps)
RUN uv sync --frozen --no-dev

# Copy the rest of the code
COPY . .

# Ensure logs dir exists (matches logger.py's Path("logs"))
RUN mkdir -p /app/logs

# Run your CLI (pick the correct entrypoint)
# Option A: if you have app/__main__.py -> python -m app
ENTRYPOINT ["python", "-m", "app.main"]
