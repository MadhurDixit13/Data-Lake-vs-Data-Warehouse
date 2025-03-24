# load_to_redshift.py

import psycopg2
import sys

# Replace with your actual configuration
REDSHIFT_HOST = 'your-redshift-cluster.redshift.amazonaws.com'
REDSHIFT_PORT = 5439
REDSHIFT_DB = 'your_database'
REDSHIFT_USER = 'your_username'
REDSHIFT_PASSWORD = 'your_password'

S3_PATH = 's3://data-lake-vs-data-warehouse/clean/owid-covid-clean.csv'
IAM_ROLE = 'arn:aws:iam::<your-account-id>:role/<redshift-access-role>'

# SQL to load the data
COPY_SQL = f"""
COPY covid_cleaned
FROM '{S3_PATH}'
IAM_ROLE '{IAM_ROLE}'
FORMAT AS CSV
IGNOREHEADER 1;
"""

try:
    print("Connecting to Redshift...")
    conn = psycopg2.connect(
        dbname=REDSHIFT_DB,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD,
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT
    )
    cur = conn.cursor()

    print("Running COPY command...")
    cur.execute(COPY_SQL)
    conn.commit()

    print("Data successfully loaded into Redshift!")

except Exception as e:
    print("Failed to load data:")
    print(e)
    sys.exit(1)

finally:
    if 'cur' in locals(): cur.close()
    if 'conn' in locals(): conn.close()
