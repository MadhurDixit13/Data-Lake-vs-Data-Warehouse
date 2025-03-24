--  Total Cases & Deaths by Country
SELECT location, MAX(total_cases) AS total_cases, MAX(total_deaths) AS total_deaths
FROM covid_cleaned
GROUP BY location
ORDER BY total_cases ASC
LIMIT 10;
