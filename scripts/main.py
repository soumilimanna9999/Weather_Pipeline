


import requests
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

EXCEL_FILE = next(
    (ROOT / "Training_Bootcamp_Assignment_Resources").rglob("*.xlsx"),
    None,
)
OUTPUT_FILE = DATA_DIR / "weather_data.csv"

# Capital cities to match against the demographic dataset.
CAPITAL_CITIES = {
    "Tokyo", "Delhi", "Beijing", "Cairo", "Dhaka",
    "Buenos Aires", "Kinshasa", "Manila", "Moscow",
    "Bogota", "Paris", "Bangkok", "Seoul", "London",
    "Tehran", "Luanda", "Kuala Lumpur", "Baghdad",
    "Riyadh", "Santiago", "Madrid", "Berlin", "Rome",
    "Canberra", "Ottawa", "Brasilia", "Brasília", "Lima",
    "Jakarta", "Hanoi", "Ankara", "Nairobi", "Abuja",
    "Accra", "Kampala", "Harare", "Pretoria", "Wellington",
    "Kathmandu", "Islamabad", "Kabul", "Amman", "Beirut",
    "Doha", "Muscat", "Singapore", "Vientiane", "Phnom Penh",
    "Ulaanbaatar", "Tashkent", "Astana", "Baku", "Yerevan",
    "Tbilisi", "Vienna", "Lisbon", "Athens", "Warsaw",
    "Prague", "Budapest", "Stockholm", "Oslo", "Helsinki",
    "Copenhagen", "Amsterdam", "Brussels", "Bern", "Bucharest",
    "Sofia", "Belgrade", "Zagreb", "Reykjavik", "Dublin",
    "Luxembourg", "Montevideo", "Asuncion", "La Paz", "Quito",
    "Caracas", "Havana", "Kingston", "Panama City", "San Jose",
    "Guatemala City", "Tegucigalpa", "Managua", "San Salvador",
    "Santo Domingo", "Port-au-Prince", "Suva", "Apia",
    "Port Moresby", "Dili", "Naypyidaw", "Thimphu", "Male",
    "Sana'a", "Damascus", "Kuwait City", "Manama", "Jerusalem",
    "Juba", "Khartoum", "Tripoli", "Tunis", "Algiers", "Rabat",
    "Nouakchott", "Bamako", "Niamey", "Ouagadougou", "Lome",
    "Porto-Novo", "Yamoussoukro", "Monrovia", "Freetown",
    "Conakry", "Banjul", "Bissau", "Brazzaville", "Libreville",
    "Malabo", "N'Djamena", "Bangui", "Asmara", "Djibouti",
    "Mogadishu", "Antananarivo", "Lilongwe", "Lusaka",
    "Gaborone", "Windhoek", "Maputo", "Mbabane", "Maseru",
    "New Delhi", "Seoul", "Mexico City", "Addis Ababa",
    "Dar es Salaam", "Washington, D.C.", "Washington"
}


def fetch_weather(city, country, latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,relative_humidity_2m,wind_speed_10m"
        ),
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    current = response.json()["current"]

    return {
        "City": city,
        "Country": country,
        "Temperature_C": current["temperature_2m"],
        "Humidity_Percent": current["relative_humidity_2m"],
        "Wind_Speed_kmh": current["wind_speed_10m"],
        "Fetched_At": datetime.now(timezone.utc).isoformat(),
    }


def main():
    if EXCEL_FILE is None:
        raise FileNotFoundError(
            "Demographic Excel file not found in "
            "Training_Bootcamp_Assignment_Resources."
        )

    print(f"Reading dataset: {EXCEL_FILE}")
    demographics = pd.read_excel(EXCEL_FILE)

    required = [
        "City", "Country", "Population", "Latitude", "Longitude"
    ]
    missing_columns = [
        column for column in required
        if column not in demographics.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Missing expected Excel columns: {missing_columns}"
        )

    demographics["City"] = demographics["City"].astype("string").str.strip()
    demographics["Country"] = (
        demographics["Country"].astype("string").str.strip()
    )

    demographics = demographics.dropna(
        subset=["City", "Country", "Latitude", "Longitude"]
    ).drop_duplicates(subset=["City", "Country"])

    capitals = demographics[
        demographics["City"].isin(CAPITAL_CITIES)
    ].copy()

    # Some dataset spellings may differ from the capital list.
    # Keep the matching results visible rather than silently claiming 50.
    print(f"Capital cities found in dataset: {len(capitals)}")
    print("Matched capitals:")
    print(capitals[["City", "Country"]].to_string(index=False))

    if len(capitals) < 50:
        print(
            "WARNING: Fewer than 50 capitals matched. "
            "We need to resolve city names or add missing capitals "
            "before claiming the 50-capital requirement is complete."
        )

    records = []

    for _, row in capitals.iterrows():
        try:
            record = fetch_weather(
                row["City"],
                row["Country"],
                float(row["Latitude"]),
                float(row["Longitude"]),
            )
            records.append(record)
            print(f"Fetched: {row['City']}, {row['Country']}")
        except (requests.RequestException, KeyError, TypeError, ValueError) as error:
            print(f"Weather fetch failed for {row['City']}: {error}")

    if not records:
        raise RuntimeError(
            "No weather records were fetched. Check the capital matches "
            "and internet connection."
        )

    weather_df = pd.DataFrame(records)

    merged_df = weather_df.merge(
        demographics[["City", "Country", "Population"]],
        on=["City", "Country"],
        how="left",
        validate="one_to_one",
    )

    # Clean population and weather data.
    merged_df["Population"] = pd.to_numeric(
        merged_df["Population"], errors="coerce"
    ).fillna(0).astype("int64")

    merged_df["Temperature_C"] = pd.to_numeric(
        merged_df["Temperature_C"], errors="coerce"
    ).astype("float64")

    merged_df["Temperature_F"] = (
        merged_df["Temperature_C"] * 9 / 5 + 32
    ).round(2)

    merged_df["Temperature_Category"] = pd.cut(
        merged_df["Temperature_C"],
        bins=[float("-inf"), 10, 25, float("inf")],
        labels=["Cold", "Mild", "Hot"],
        right=False,
    ).astype("string")

    merged_df = merged_df.dropna(subset=["Temperature_C"])

    merged_df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved {len(merged_df)} records to: {OUTPUT_FILE}")
    print("\nColumn data types:")
    print(merged_df.dtypes)
    print("\nPreview:")
    print(merged_df.head().to_string(index=False))


if __name__ == "__main__":
    main()


