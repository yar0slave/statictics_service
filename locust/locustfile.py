import json
import random
import uuid
from datetime import datetime, timedelta
from locust import HttpUser, task, between


class DeviceStatsUser(HttpUser):
    wait_time = between(1, 5)  # wait between 1 and 5 seconds between tasks

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_prefix = "/api/v1"
        self.device_ids = []
        self.user_id = None

    def on_start(self):
        # Create a test user
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        user_data = {
            "username": username,
            "email": f"{username}@example.com"
        }

        # Создаем пользователя
        with self.client.post(f"{self.api_prefix}/users/", json=user_data, catch_response=True) as response:
            if response.status_code == 201:
                self.user_id = response.json().get("id")
                print(f"Created user with ID: {self.user_id}")

                # Регистрируем устройства
                self.register_devices()

                # Отправляем начальную статистику для каждого устройства
                self.send_initial_stats()
            else:
                print(f"Failed to create user: {response.text}")

    def register_devices(self):
        # Создаем несколько устройств для пользователя
        for i in range(3):  # Создаем 3 устройства
            # Генерируем уникальный строковый device_id
            device_string_id = f"dev_{uuid.uuid4().hex[:10]}"

            device_data = {
                "device_id": device_string_id,  # Строковый ID, который будет использоваться в URL
                "name": f"device_{i}_{uuid.uuid4().hex[:6]}",
                "user_id": self.user_id
            }

            # Адаптируйте URL в соответствии с вашим API
            with self.client.post(f"{self.api_prefix}/devices/", json=device_data, catch_response=True) as response:
                if response.status_code == 201:
                    # Сохраняем строковый device_id вместо числового id из ответа
                    self.device_ids.append(device_string_id)
                    print(f"Created device with ID: {device_string_id}")
                else:
                    print(f"Failed to create device: {response.status_code} - {response.text}")

    def send_initial_stats(self):
        # Отправка начальной статистики для каждого устройства
        for device_id in self.device_ids:
            # Отправляем несколько записей статистики с разными временными метками
            for _ in range(5):  # Отправляем 5 записей на устройство
                stats_data = {
                    "x": random.uniform(-100, 100),
                    "y": random.uniform(-100, 100),
                    "z": random.uniform(-100, 100)
                }

                with self.client.post(
                        f"{self.api_prefix}/stats/devices/{device_id}",
                        json=stats_data,
                        catch_response=True
                ) as response:
                    if response.status_code == 201 or response.status_code == 200:
                        print(f"Initial stats sent for device {device_id}")
                    else:
                        print(f"Failed to send initial stats for device {device_id}: {response.text}")

    @task(10)
    def send_device_stats(self):
        """Send statistics for a random device."""
        if not self.device_ids:
            print("No device IDs available")
            return

        device_id = random.choice(self.device_ids)
        stats_data = {
            "x": random.uniform(-100, 100),
            "y": random.uniform(-100, 100),
            "z": random.uniform(-100, 100)
        }

        with self.client.post(
                f"{self.api_prefix}/stats/devices/{device_id}",
                json=stats_data,
                catch_response=True
        ) as response:
            print(f"Send stats response: {response.status_code}, {response.text}")

    @task(3)
    def get_device_stats(self):
        """Get statistics for a random device."""
        if not self.device_ids:
            return

        device_id = random.choice(self.device_ids)
        self.client.get(f"{self.api_prefix}/stats/devices/{device_id}")

    @task(2)
    def analyze_device_stats(self):
        """Analyze statistics for a random device."""
        if not self.device_ids:
            return

        device_id = random.choice(self.device_ids)
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)

        time_range = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }

        self.client.post(
            f"{self.api_prefix}/stats/devices/{device_id}/analyze",
            json=time_range
        )

    @task(1)
    def analyze_user_stats(self):
        """Analyze statistics for all user devices."""
        if not self.user_id:
            return

        # Текущее время
        now = datetime.utcnow()

        # Расширяем диапазон: 1 день назад и 1 день вперед
        start_time = now - timedelta(days=1)
        end_time = now + timedelta(days=1)

        time_range = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }

        with self.client.post(
                f"{self.api_prefix}/stats/users/{self.user_id}/analyze",
                json=time_range,
                catch_response=True
        ) as response:
            print(f"Analyze user stats response: {response.status_code}, {response.text}")