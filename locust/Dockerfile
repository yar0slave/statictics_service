FROM python:3.10-slim

WORKDIR /app

# Install Locust
COPY locust/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Locust configuration
COPY locust/ /app/locust/

# Command to run Locust
ENTRYPOINT ["locust", "--host", "${TARGET_HOST:-http://app:8000}", "-f", "/app/locust/locustfile.py"]