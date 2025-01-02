FROM python:3.12.8-alpine3.20

# Set the working directory in the container
WORKDIR /app/

# Copy setup files
COPY pyproject.toml requirements.txt uv.lock ./
RUN pip install uv
RUN uv venv && source .venv/bin/activate
RUN uv pip install -r requirements.txt

# Copy the rest of the files
COPY . .

# Set the default command to run the application
CMD ["/bin/sh", "-c", ". .venv/bin/activate && fastapi run main.py --port 8000 --host 0.0.0.0"]
