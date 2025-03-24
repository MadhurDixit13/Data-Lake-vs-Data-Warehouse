-- Daily Trends for a Country

SELECT date, new_cases
FROM covid_cleaned
WHERE location = 'India'
ORDER BY date;
