# Use the official Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app
COPY pyproject.toml /app
COPY uv.lock /app

# Install dependencies
RUN pip install uv
RUN uv venv
RUN uv sync

# Copy rest of the source files
COPY . /app

# Set the default command to run the application
CMD ["/bin/sh", "-c", ". .venv/bin/activate && fastapi dev main.py --port 8000 --host 0.0.0.0"]
