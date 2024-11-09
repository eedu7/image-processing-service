# Start from the official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR .

# Install system dependencies for OpenCV and other dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install poetry && poetry install --no-root --only main

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Run Alembic migrations and then Uvicorn server
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn core:app --host 0.0.0.0 --port 8000 --reload"]
