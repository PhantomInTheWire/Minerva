FROM python:3.11-slim

# Set the working directory
WORKDIR /backend/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Install `uv` and setup virtual environment
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && \
    uv venv && uv sync

# Copy the rest of the project files
COPY . .

# Set the default command
CMD ["/bin/sh", "-c", ". .venv/bin/activate && alembic upgrade head && fastapi dev src/main.py --port 8000 --host 0.0.0.0"]

