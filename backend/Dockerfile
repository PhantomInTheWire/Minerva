FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /backend/

# Copy setup files
COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv venv && uv sync
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0
# Copy the rest of the files
COPY . .

# Set the default command to run the application
CMD ["/bin/sh", "-c", ". .venv/bin/activate && alembic upgrade head && fastapi dev src/main.py --port 8000 --host 0.0.0.0"]
