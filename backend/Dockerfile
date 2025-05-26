# ─── Base Image ───────────────────────────────────────────────────────────────
FROM python:3.12-slim

# ─── Working Directory ────────────────────────────────────────────────────────
WORKDIR /app

# ─── System Dependencies ──────────────────────────────────────────────────────
# (for ReportLab, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
         libfreetype6-dev \
         libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# ─── Python Dependencies ──────────────────────────────────────────────────────
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ─── Application & Model ──────────────────────────────────────────────────────
# Copy your code *and* the vendored model under backend/models/
COPY . .

# Copy the MNIST ONNX model from /app/models to /models for runtime
RUN mkdir -p /models \
    && cp /app/models/mnist-8.onnx /models/mnist.onnx

# ─── Startup & Healthcheck ────────────────────────────────────────────────────
# Use Railway’s $PORT (default to 8000 if unset)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]

HEALTHCHECK CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Drop to non-root for security
USER 1001
