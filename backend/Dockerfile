# Use a minimal Python runtime
FROM python:3.12-slim

# Set working dir
WORKDIR /app

# Install system deps needed by ReportLab (and clean up apt cache)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         libfreetype6-dev \
         libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code (including vendored model under backend/models/)
COPY . /app

# Copy the vendored MNIST ONNX model into /models for runtime use
RUN mkdir -p /models \
    && cp /app/backend/models/mnist-8.onnx /models/mnist.onnx

# Expose the port Railway sets (fallback to 8000 if PORT is unset)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]

# Simple healthcheck against the root endpoint
HEALTHCHECK CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Drop back to a non-root user
USER 1001
