# compare_performance_aws.py

import boto3
import psycopg2
import pandas as pd
import time
import io

# Athena settings
athena_client = boto3.client('athena')
athena_database = 'your_database_name'  
athena_output = 's3://bucket-name/athena/results/'


athena_query = """
SELECT location, AVG(new_cases) AS avg_new_cases
FROM owid_covid_data_csv
WHERE continent IS NOT NULL AND new_cases IS NOT NULL
GROUP BY location
"""

start_athena_time = time.time()

# Start Athena query
athena_response = athena_client.start_query_execution(
    QueryString=athena_query,
    QueryExecutionContext={'Database': athena_database},
    ResultConfiguration={'OutputLocation': athena_output}
)

query_execution_id = athena_response['QueryExecutionId']

# Wait for Athena query to complete
status = 'RUNNING'
while status in ['RUNNING', 'QUEUED']:
    response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
    status = response['QueryExecution']['Status']['State']
    time.sleep(1)
    
athena_time = time.time() - start_athena_time

athena_result_path = response['QueryExecution']['ResultConfiguration']['OutputLocation']
print("Athena query complete. Results at:", athena_result_path)

# Read Athena result into DataFrame
df_athena = pd.read_csv(
    athena_result_path,
    storage_options={"anon": False}  # or add access keys if needed
)

# Redshift connection
redshift_conn = psycopg2.connect(
    dbname="your_database",
    user="your_username",
    password="your_password",
    host="your-redshift-cluster.redshift.amazonaws.com",
    port=5439
)

redshift_query = """
SELECT location, AVG(new_cases) AS avg_new_cases
FROM covid_cleaned
GROUP BY location
"""

start_time = time.time()
df_redshift = pd.read_sql(redshift_query, redshift_conn)
redshift_time = time.time() - start_time
redshift_conn.close()

# Create summary
df_summary = pd.DataFrame({
    "System": ["Athena", "Redshift"],
    "Num Rows": [len(df_athena), len(df_redshift)],
    "Query Time (s)": [f"{athena_time:.2f}", f"{redshift_time:.2f}"]
})

# Upload to S3
s3 = boto3.client('s3')
bucket = 'bucket-name' 
prefix = 'comparison/'

def upload_df_to_s3(df, filename):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=f"{prefix}{filename}", Body=csv_buffer.getvalue())
    print(f"Uploaded {filename} to s3://{bucket}/{prefix}")

upload_df_to_s3(df_athena, "athena_results.csv")
upload_df_to_s3(df_redshift, "redshift_results.csv")
upload_df_to_s3(df_summary, "comparison_summary.csv")
