# Use a slim official Python image
FROM python:3.10-slim

# Install uv directly from the official binary distribution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Prevent Python from writing .pyc files and enable stdout/stderr flushing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps and Python deps using uv
COPY requirements.txt .
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libc-dev \
 # --system: installs into the system Python environment
 # --no-cache: keeps the image size small
 && uv pip install --system --no-cache -r requirements.txt \
 && apt-get remove -y gcc libc-dev \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

# Copy app code and model file(s)
COPY . .

# Train the Model
RUN python3 model/train.py

# Expose the port your app runs on
EXPOSE 6000

# Start the app with gunicorn (4 workers, bind to 0.0.0.0:6000)
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:6000", "app:app"]