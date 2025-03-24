-- Daily New Cases Trend (e.g., United States)
SELECT date, new_cases
FROM owid_covid_data_csv
WHERE location = 'United States'
  AND new_cases IS NOT NULL
ORDER BY date;
