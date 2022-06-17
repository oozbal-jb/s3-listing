import boto3
import os
import urllib.parse
from dotenv import load_dotenv

def createHrefList(files,folders):
    hrefList=[]
    hrefStr=""
    for e in folders:
        href="<li><a href=\""+e[1]+"\">"+e[0]+"</a></li>"
        hrefList.append(href)
        hrefStr=hrefStr+href
    for e in files:
        href="<li><a href=\""+e[1]+"\">"+e[0]+"</a></li>"
        hrefList.append(href)
        hrefStr=hrefStr+href
    return hrefStr

load_dotenv()

ACCESS_KEY=os.getenv('ACCESS_KEY_ID')
SECRET_KEY=os.getenv('ACCESS_SECRET')
REGION=os.getenv('REGION')
client = boto3.client ( 's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
#get value of prefix query param.
safePrefix='appBuilder.jmx%2F'
prefix=urllib.parse.unquote(safePrefix)
print(prefix)

bucket='lcap-jmeter-results'
apiId='test-api'



# Print out bucket names
# for bucket in client.list_buckets()["Buckets"]:
#     print(bucket["Name"])
#     print("http://localhost:5000/search?bucket="+bucket["Name"])


response=client.list_objects_v2(
    Bucket=bucket,
    Delimiter='/',
    Prefix=prefix
)

# print(response)

#get folders under prefix
folders=[]
try:
    commonPrefixes=response['CommonPrefixes']
    for i in commonPrefixes:
        folderName=i['Prefix'].split('/')[-2]+"/"
        urlPrefix=urllib.parse.quote(i['Prefix'], safe='')
        link="https://"+apiId+".execute-api."+REGION+".amazonaws.com/search?prefix="+urlPrefix+"&"+bucket
        folders.append( (folderName,link) )
    print("folders    ",folders)
except:
    print("There is a problem in response CommonPrefixes.")


#get files under prefix
files=[]
try:
    contents=response['Contents']
    for e in contents:
        key=e['Key'].split('/')[-1]
        link="https://"+bucket+".s3."+REGION+".amazonaws.com/"+key
        files.append( ( key , link ) )
    print("files   ",files)
except:
    print("There s a problem in response Contents.")

hrefList=createHrefList(files,folders)

htmlResponse="""<html><body>
<h2>"""+bucket+"""</h2>
<ul>
"""+hrefList+"""
</ul>
</body>
</html>
"""

print(htmlResponse)








# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Distant Reading Archive</h1>
# <p>A prototype API for distant reading of science fiction novels.</p>'''



# @app.route('/search', methods=['GET'])
# def bucket_root():
#     if 'bucket' in request.args:
#         bucketName = request.args['bucket']
#         session = boto3.Session (
#             aws_access_key_id=ACCESS_KEY,
#             aws_secret_access_key=SECRET_KEY
#         )
#         s3 = session.resource('s3')
#         bucket = s3.Bucket(bucketName)
#         objs = bucket.objects.all()
#         for obj in objs:
#             print(obj)
#         return "success"
#     else:
#         return "Error: No bucket field provided. Please provide bucket name."


# app.run()