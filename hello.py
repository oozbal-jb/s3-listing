import boto3
import os
from dotenv import load_dotenv
import flask
from flask import request, jsonify


load_dotenv()
ACCESS_KEY=os.getenv('ACCESS_KEY_ID')
SECRET_KEY=os.getenv('ACCESS_SECRET')
REGION=os.getenv('REGION')
client = boto3.client ( 's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
# buckets = client.list_buckets()
# print(buckets.type())

# Print out bucket names
for bucket in client.list_buckets()["Buckets"]:
    print(bucket["Name"])
    print("http://localhost:5000/search?bucket="+bucket["Name"])



response=client.list_objects_v2(
    Bucket='lcap-jmeter-results',
    Delimiter='/',
    Prefix='appBuilder.jmx/'
)
print(response)

app = flask.Flask(__name__)



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''



@app.route('/search', methods=['GET'])
def bucket_root():
    if 'bucket' in request.args:
        bucketName = request.args['bucket']
        session = boto3.Session (
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
        )
        s3 = session.resource('s3')
        bucket = s3.Bucket(bucketName)
        objs = bucket.objects.all()
        for obj in objs:
            print(obj)
        return "success"
    else:
        return "Error: No bucket field provided. Please provide bucket name."


app.run()