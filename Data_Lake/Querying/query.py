# athena_export_cleaned.py
import boto3
import time

athena = boto3.client('athena')
s3_output = 's3://data-lake-vs-data-warehouse/clean/'

query = """
SELECT 
  location, 
  date, 
  total_cases, 
  new_cases, 
  total_deaths, 
  new_deaths, 
  people_fully_vaccinated_per_hundred, 
  hospital_beds_per_thousand
FROM owid_covid_data_csv
WHERE continent IS NOT NULL AND date IS NOT NULL
"""

response = athena.start_query_execution(
    QueryString=query,
    QueryExecutionContext={'Database': 'your_database_name'},
    ResultConfiguration={'OutputLocation': s3_output}
)

query_execution_id = response['QueryExecutionId']

# Wait for completion
while True:
    result = athena.get_query_execution(QueryExecutionId=query_execution_id)
    state = result['QueryExecution']['Status']['State']
    if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
        break
    time.sleep(2)

if state == 'SUCCEEDED':
    output_path = result['QueryExecution']['ResultConfiguration']['OutputLocation']
    print(f'Cleaned CSV written to: {output_path}')
else:
    print(f'Query failed with state: {state}')
