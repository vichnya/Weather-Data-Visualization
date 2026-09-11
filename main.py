import os
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

load_dotenv()

CITY = "Saint Petersburg"
LATITUDE = 59.57
LONGITUDE = 30.19

dates = []
temps = []


def get_weather(api_key):
    """Получает прогноз погоды на 5 дней с шагом 3 часа."""
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "appid": api_key,
        "units": "metric",
        "lang": "ru",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def add_data(data):
    """Извлекает даты и температуры из ответа API."""
    for item in data["list"]:
        date = datetime.fromtimestamp(item["dt"])
        dates.append(date)
        temps.append(item["main"]["temp"])


def visualize_data():
    """Строит графики температуры и средних температур по дням."""
    daily_temps = defaultdict(list)

    for date, temp in zip(dates, temps):
        daily_temps[date.date()].append(temp)

    daily_dates = list(daily_temps.keys())
    daily_average = [
        sum(values) / len(values)
        for values in daily_temps.values()
    ]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    axes[0].scatter(dates, temps)
    axes[0].set_title(f"Прогноз температуры: {CITY}")
    axes[0].set_xlabel("Дата и время")
    axes[0].set_ylabel("Температура, °C")
    axes[0].grid(True)

    axes[1].plot(daily_dates, daily_average, marker="o")
    axes[1].set_title("Средняя прогнозируемая температура по дням")
    axes[1].set_xlabel("Дата")
    axes[1].set_ylabel("Средняя температура, °C")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise ValueError(
            "Не найден OPENWEATHER_API_KEY. "
            "Добавьте API-ключ в файл .env."
        )

    weather_data = get_weather(api_key)
    add_data(weather_data)
    visualize_data()


if __name__ == "__main__":
    main()
