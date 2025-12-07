FROM python:3.9.18-slim

WORKDIR /app

# Install system dependencies for scipy/numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy dependency files first for better caching
COPY pyproject.toml poetry.lock ./
COPY bayes_continuous ./bayes_continuous/

# Install dependencies (no virtualenv in container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

EXPOSE 8000

# gunicorn is production-ready here because Coolify's reverse proxy (Traefik)
# handles SSL termination, request buffering, and static file serving
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
