# Base image
FROM python:3.11-slim

WORKDIR /app

# Dependencies copy + install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source code copy
COPY producer.py .
COPY consumer.py .
COPY fraud_detector.py .

# Default command (override kar sakte hain)
CMD ["python3", "consumer.py"]