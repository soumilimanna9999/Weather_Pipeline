
-- Create a view showing the five hottest countries
-- among city records where population exceeds 10 million.

CREATE OR REPLACE VIEW
  `valid-gizmo-512421-t7.global_weather_data.vw_hottest_large_countries` AS

SELECT
  Country,
  ROUND(AVG(Temperature_C), 2) AS Avg_Temperature_C,
  COUNT(DISTINCT City) AS Cities_Analyzed,
  MAX(Population) AS Largest_City_Population
FROM
  `valid-gizmo-512421-t7.global_weather_data.current_weather_stats`
WHERE
  Population > 10000000
GROUP BY
  Country
ORDER BY
  Avg_Temperature_C DESC
LIMIT 5;
