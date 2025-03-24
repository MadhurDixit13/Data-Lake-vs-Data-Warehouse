-- Vaccination Progress
SELECT location, MAX(people_fully_vaccinated_per_hundred) AS fully_vaccinated
FROM covid_cleaned
GROUP BY location
ORDER BY fully_vaccinated DESC
LIMIT 10;
