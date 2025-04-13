FROM python:3.10-slim

WORKDIR /app

COPY locust/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY locust/ /app/locust/

ENTRYPOINT ["locust", "--host", "${TARGET_HOST:-http://app:8000}", "-f", "/app/locust/locustfile.py"]