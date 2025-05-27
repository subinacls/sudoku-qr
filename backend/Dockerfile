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
# Copy all your code and the vendored model at backend/models/mnist-8.onnx
COPY . .

# Put the vendored ONNX into /models for runtime
RUN mkdir -p /models \
    && cp /app/models/mnist-8.onnx /models/mnist.onnx

# ─── Startup & Healthcheck ────────────────────────────────────────────────────
# Use shell form so $PORT (set by Railway) is expanded at container start time
# Fallback to 8000 only if PORT isn’t set.
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"

# Healthcheck via shell form as well
HEALTHCHECK --interval=30s CMD sh -c "curl -fs http://localhost:${PORT:-8000}/ || exit 1"

# Drop to non-root user
USER 1001
