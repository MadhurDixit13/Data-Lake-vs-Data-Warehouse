CREATE TABLE covid_cleaned (
  location VARCHAR(100),
  date DATE,
  total_cases BIGINT,
  new_cases BIGINT,
  total_deaths BIGINT,
  new_deaths BIGINT,
  people_fully_vaccinated_per_hundred DOUBLE PRECISION,
  hospital_beds_per_thousand DOUBLE PRECISION
);
