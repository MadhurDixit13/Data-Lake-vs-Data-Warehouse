-- Total Cases & Deaths by Country
SELECT location, MAX(hospital_beds_per_thousand) AS beds_per_thousand
FROM owid_covid_data_csv
WHERE hospital_beds_per_thousand IS NOT NULL
GROUP BY location
ORDER BY beds_per_thousand DESC
LIMIT 10;