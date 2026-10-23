# WeatherScope: Global Weather & Demographics Pipeline

## Project Overview

WeatherScope is an end-to-end data pipeline that collects current weather observations, combines them with global demographic data, and makes the resulting dataset available for analysis in Google BigQuery and Looker Studio.

The project uses Python, Pandas, the Open-Meteo API, Google BigQuery, SQL, and Looker Studio.

## Objectives

- Fetch current weather data for capital cities.
- Merge weather observations with population and geographic data.
- Clean and validate the dataset.
- Convert temperature from Celsius to Fahrenheit.
- Classify temperatures into Cold, Mild, and Hot categories.
- Load the processed dataset into BigQuery.
- Analyze weather and population patterns using SQL.
- Build an interactive Looker Studio dashboard.

## Tech Stack

- Python
- Pandas
- Requests
- Open-Meteo API
- Google BigQuery
- SQL
- Looker Studio
- Git and GitHub

## Project Structure

```text
Weather_Pipeline/
├── scripts/
│   └── main.py
├── sql/
│   ├── create_views.sql
│   └── exploration_queries.sql
├── data/
│   └── weather_data.csv
├── README.md
└── .gitignore
```

Note: Generated data and local configuration files may be excluded from Git using `.gitignore`.

## Data Sources

### Weather Data
Current weather observations are retrieved from the Open-Meteo API.

### Demographic Data
The demographic dataset contains city, country, population, latitude, and longitude information.

Source: [Training Bootcamp Assignment Resources](https://github.com/yashhh0001/Training_Bootcamp_Assignment_Resources.git)

## Data Pipeline

1. Read the demographic Excel dataset.
2. Select the available matching capital-city records.
3. Fetch current weather observations using latitude and longitude.
4. Merge weather and demographic data.
5. Handle missing values and validate data types.
6. Calculate Fahrenheit temperature and temperature categories.
7. Export the processed dataset to CSV.
8. Upload the data to BigQuery for SQL analysis.

## Data Coverage and Validation

- Matched city records: 28
- Unique cities: 28
- Missing values in the generated dataset: 0
- Temperature categories: Cold, Mild, and Hot

The original target was 50 capital cities. The current pipeline produced 28 matched records because of the available matching city data. This is a documented limitation of the current dataset.

## Google BigQuery

**Project ID:** `valid-gizmo-512421-t7`

**Dataset:** `global_weather_data`

**Table:** `current_weather_stats`

The processed weather dataset is stored in BigQuery for exploration and visualization.

### SQL Analysis

The `sql/exploration_queries.sql` file contains exploratory queries, including:

- Top 10 hottest cities
- Temperature and population analysis
- Top 5 hottest countries with population above 10 million

The `sql/create_views.sql` file creates the logical view:

`vw_hottest_large_countries`

This view supports the analysis of the hottest countries that meet the population threshold.

## Looker Studio Dashboard

**Dashboard Name:** WeatherScope — Global Weather & Demographics Analytics

**Dashboard Link:**(https://datastudio.google.com/reporting/092160f9-53e6-438a-bd69-0298176bbb55/page/I2xBG)

### Dashboard Features

- Global weather map with temperature categories
- City and country filters
- Cities analyzed, countries covered, average temperature, and total population KPIs
- Top 10 hottest cities
- Temperature category distribution
- Temperature versus humidity analysis
- Top 5 hottest countries with population above 10 million
- Top 5 cities by population
- Average wind speed gauge

## How to Run the Pipeline

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Place the demographic Excel file in the expected project folder.
5. Run the pipeline.
6. Review the generated CSV and upload it to BigQuery.

Example commands:

```bash
git clone https://github.com/soumilimanna9999/Weather_Pipeline.git
cd Weather_Pipeline

python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install requests pandas python-dotenv openpyxl
```

Run the pipeline:

```bash
python scripts/main.py
```

## Security

- Do not commit API secrets, passwords, `.env` files, or service-account JSON keys.
- Keep credentials outside version control.
- Use the appropriate Google Cloud permissions for BigQuery access.

## Future Improvements

- Expand coverage to all 50 target capital cities.
- Automate scheduled weather ingestion.
- Store historical weather observations for trend analysis.
- Add automated data-quality checks.
- Improve dashboard filtering and geographic coverage.

## Author

WeatherScope — Weather and Demographics Analytics Project
