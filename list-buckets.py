import boto3
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY=os.getenv('ACCESS_KEY_ID')
SECRET_KEY=os.getenv('ACCESS_SECRET')
REGION=os.getenv('REGION')
client = boto3.client ( 's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)

response=client.list_buckets()
buckets=response['Buckets']
bucketsList=[]

for e in buckets:
    bucketRegion=client.get_bucket_location( Bucket=e['Name'])['LocationConstraint']
    bucketsList.append( ( e['Name'],bucketRegion) )

print(bucketsList)