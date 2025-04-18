# === Stage 1: Build ===
FROM python:3.11-slim AS builder

WORKDIR /backend

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && \
    uv venv && uv sync

COPY . .

# === Stage 2: Runtime ===
FROM python:3.11-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /backend/ /backend/

CMD ["/bin/sh", "-c", ". .venv/bin/activate && alembic upgrade head && fastapi dev src/main.py --port 8000 --host 0.0.0.0"]

