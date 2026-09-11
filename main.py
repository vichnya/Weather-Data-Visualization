import json
import os
from datetime import datetime, timedelta
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


CITY = "Saint Petersburg, RU"
LATITUDE = 59.57
LONGITUDE = 30.19

dates = []
temps = []
dates_for_dat = []


def get_weather(api_key=None, dt=None):
    """Получение погодных данных через OpenWeatherMap API."""

    if not api_key:
        raise ValueError("Не указан API-ключ OpenWeatherMap.")

    if dt is None:
        dt = int(datetime.now().timestamp())

    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

    params = {
        "lat": LATITUDE,
        "lon": LONGITUDE,
        "dt": dt,
        "appid": api_key,
        "lang": "ru",
        "units": "metric",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    weather_data = response.json()

    result = {
        "city": CITY,
        "temps": [
            {
                "dt": str(measure["dt"]),
                "temp": str(measure["temp"]),
            }
            for measure in weather_data["hourly"]
        ],
    }

    return json.dumps(result)


def add_data(json_data):
    """Добавление полученных данных в общий набор."""

    data = pd.read_json(json_data)

    dates.extend(
        item["dt"]
        for item in data["temps"]
    )

    dates_for_dat.extend(
        item["dt"]
        for item in data["temps"][:1]
    )

    temps.extend(
        float(item["temp"])
        for item in data["temps"]
    )


def visualize_data():
    """Визуализация почасовой и средней температуры."""

    dat = [
        datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d")
        for timestamp in dates_for_dat
    ]

    plt.figure(figsize=(14, 5))

    # Почасовая температура
    plt.subplot(1, 2, 1)
    plt.plot(dates, temps)
    plt.xticks(
        np.arange(12, 132, 24),
        dat,
    )
    plt.yticks(np.arange(-15, 16, 2))
    plt.title(CITY)
    plt.xlabel("Дата")
    plt.ylabel("Температура, °C")

    # Средняя температура за каждый день
    temps_mean = []

    for i in range(5):
        day_temperatures = temps[i * 24:(i + 1) * 24]
        temps_mean.append(round(mean(day_temperatures), 4))

    plt.subplot(1, 2, 2)
    plt.plot(dat, temps_mean, marker="o")
    plt.xticks(np.arange(5), dat)
    plt.yticks(np.arange(-20, 1, 2))
    plt.title("Средняя температура по дням")
    plt.xlabel("Дата")
    plt.ylabel("Средняя температура, °C")

    plt.tight_layout()
    plt.show()


def get_time(day):
    """Получение Unix-времени для указанного количества дней назад."""

    current_datetime = datetime.now() - timedelta(days=day)
    return int(current_datetime.timestamp())


def main():
    api_key = os.getenv("OPENWEATHER_API_KEY")

    for day in range(5):
        weather_data = get_weather(
            api_key,
            get_time(day),
        )
        add_data(weather_data)

    visualize_data()


if __name__ == "__main__":
    main()
