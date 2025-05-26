
FROM python:3.12-slim

WORKDIR /app

# System dependencies for ReportLab and model download
RUN apt-get update \
    && apt-get install -y --no-install-recommends libfreetype6-dev libjpeg-dev wget \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Download MNIST ONNX model at build time
RUN mkdir -p /models && wget -q -O /models/mnist.onnx https://huggingface.co/onnx/models/resolve/main/vision/mnist-8.onnx

COPY . /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


HEALTHCHECK CMD curl -f http://localhost:8000/ || exit 1

USER 1001
