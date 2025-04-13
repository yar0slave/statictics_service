#!/bin/bash

# Создание директорий
mkdir -p app/models app/schemas app/routers app/services
mkdir -p tests
mkdir -p locust

# Создание файлов в app
touch app/__init__.py
touch app/main.py  # FastAPI application entry point
touch app/config.py  # Configuration settings

# Создание файлов в app/models
touch app/models/__init__.py
touch app/models/database.py  # Database connection and base model
touch app/models/device.py  # Device model
touch app/models/stats.py  # Stats model
touch app/models/user.py  # User model

# Создание файлов в app/schemas
touch app/schemas/__init__.py
touch app/schemas/device.py  # Device Pydantic schemas
touch app/schemas/stats.py  # Stats Pydantic schemas
touch app/schemas/user.py  # User Pydantic schemas

# Создание файлов в app/routers
touch app/routers/__init__.py
touch app/routers/devices.py  # Device endpoints
touch app/routers/stats.py  # Stats endpoints
touch app/routers/users.py  # User endpoints

# Создание файлов в app/services
touch app/services/__init__.py
touch app/services/device_service.py  # Device business logic
touch app/services/stats_service.py  # Stats business logic
touch app/services/user_service.py  # User business logic

# Создание файлов в tests
touch tests/__init__.py
touch tests/conftest.py  # Test configuration
touch tests/test_devices.py  # Device tests
touch tests/test_stats.py  # Stats tests
touch tests/test_users.py  # User tests

# Создание файлов в locust
touch locust/locustfile.py  # Load testing configuration
touch locust/requirements.txt  # Locust dependencies

# Создание файлов в корневой директории
touch docker-compose.yml  # Docker Compose configuration
touch Dockerfile  # App Dockerfile
touch requirements.txt  # Python dependencies
touch README.md  # Project documentation

echo "Структура проекта создана успешно!"