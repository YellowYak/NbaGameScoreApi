# Base image: slim Debian-based Python, ~150MB
FROM python:3.12-slim

# Install git so pip can clone the nba-watchability git+https:// dependency
RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

# All subsequent commands run from /app inside the container
WORKDIR /app

# Copy dependency manifest first and install — keeps this layer cached
# independently of app code changes
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy app code last — changes most frequently, so belongs at the bottom
COPY api/ ./api/

# Documents that the container listens on 8000 (doesn't publish it)
EXPOSE 8000

# Start uvicorn — 0.0.0.0 makes it reachable from outside the container
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]