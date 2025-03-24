-- Hospital Capacity Insight
SELECT location, MAX(people_fully_vaccinated_per_hundred) AS fully_vaccinated_pct
FROM owid_covid_data_csv
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY fully_vaccinated_pct DESC
LIMIT 10;
