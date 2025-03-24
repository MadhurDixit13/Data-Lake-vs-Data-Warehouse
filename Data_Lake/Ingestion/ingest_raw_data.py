# data_lake/upload_to_s3.py
import boto3

s3 = boto3.client(
    's3',
    # aws_access_key_id='YOUR_ACCESS_KEY',
    # aws_secret_access_key='YOUR_SECRET_KEY',
    # region_name='us-east-1'
)
# s3 = boto3.client('s3')


bucket = 'your-bucket-name'
s3.upload_file('../../Data/owid-covid-data.csv', bucket, 'raw/owid/owid-covid-data.csv')
