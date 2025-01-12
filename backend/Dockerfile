FROM python:3.11-alpine3.20

# Set the working directory in the container
WORKDIR /backend/

# Copy setup files
COPY pyproject.toml uv.lock ./
RUN pip install uv
RUN uv venv && uv sync

# Copy the rest of the files
COPY . .

# Set the default command to run the application
CMD ["/bin/sh", "-c", ". .venv/bin/activate && alembic upgrade head && fastapi dev src/main.py --port 8000 --host 0.0.0.0"]
