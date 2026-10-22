
import requests
import pandas as pd
from datetime import datetime, timezone

def fetch_weather(city, latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()
    current = data["current"]

    record = {
        "city": city,
        "temperature_c": current["temperature_2m"],
        "humidity_percent": current["relative_humidity_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "fetched_at": datetime.now(timezone.utc).isoformat()
    }

    return record



if __name__ == "__main__":
    cities = {
        "Delhi": (28.6139, 77.2090),
        "Mumbai": (19.0760, 72.8777),
        "Bengaluru": (12.9716, 77.5946),
        "Kolkata": (22.5726, 88.3639),
        "Chennai": (13.0827, 80.2707)
    }

    records = []

    for city, coordinates in cities.items():
        weather = fetch_weather(city, coordinates[0], coordinates[1])
        records.append(weather)

    df = pd.DataFrame(records)
    df.to_csv("data/weather_data.csv", index=False)

    print("Weather data saved successfully!")
    print(df)

