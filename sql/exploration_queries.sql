
-- 1. Check total records and unique cities
SELECT
  COUNT(*) AS total_records,
  COUNT(DISTINCT City) AS unique_cities,
  COUNT(DISTINCT Country) AS unique_countries
FROM `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`;


-- 2. Check missing values in important columns
SELECT
  COUNTIF(City IS NULL) AS missing_city,
  COUNTIF(Country IS NULL) AS missing_country,
  COUNTIF(Population IS NULL) AS missing_population,
  COUNTIF(Temperature_C IS NULL) AS missing_temperature,
  COUNTIF(Temperature_Category IS NULL) AS missing_category
FROM `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`;


-- 3. Preview the weather and demographic data
SELECT
  City,
  Country,
  Population,
  Temperature_C,
  Temperature_F,
  Temperature_Category,
  Humidity_Percent,
  Wind_Speed_kmh
FROM `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`
ORDER BY Country, City;


-- 4. Top 10 hottest cities
SELECT
  City,
  Country,
  Population,
  Temperature_C,
  Temperature_F,
  Temperature_Category
FROM `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`
ORDER BY Temperature_C DESC
LIMIT 10;


-- 5. Temperature category distribution
SELECT
  Temperature_Category,
  COUNT(*) AS city_count,
  ROUND(AVG(Temperature_C), 2) AS avg_temperature_c
FROM `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`
GROUP BY Temperature_Category
ORDER BY avg_temperature_c DESC;


-- 6. Cities with population above 10 million
SELECT
  City,
  Country,
  Population,
  Temperature_C
FROM `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`
WHERE Population > 10000000
ORDER BY Population DESC;


-- 7. Top 5 hottest countries among records with population above 10 million
-- This averages temperatures for qualifying city records.
SELECT
  Country,
  ROUND(AVG(Temperature_C), 2) AS Avg_Temperature_C,
  COUNT(DISTINCT City) AS Cities_Analyzed,
  MAX(Population) AS Largest_City_Population
FROM `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`
WHERE Population > 10000000
GROUP BY Country
ORDER BY Avg_Temperature_C DESC
LIMIT 5;


-- 8. Verify the saved logical view
SELECT *
FROM `valid-gizmo-512421-t7.global_weather_data.vw_hottest_large_countries`
ORDER BY Avg_Temperature_C DESC;
