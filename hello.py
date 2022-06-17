import boto3
import os
import urllib.parse

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
    


def lambda_handler(event, context):
    # TODO implement
    ACCESS_KEY=os.getenv('ACCESS_KEY_ID')
    SECRET_KEY=os.getenv('ACCESS_SECRET')
    client = boto3.client ( 's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
    #get value of prefix query param.
    safePrefix=event['query']['prefix']

    prefix=urllib.parse.unquote(safePrefix)
    host=event['headers']['Host']
    REGION=event['query']['region']

    bucket=event['query']['bucket']

    path=event['path']
    print(prefix)
    print(safePrefix)
    print(REGION)
    print(host)
    
    print(event)
    
    
#    REGION='us-east-2'
#    bucket='lcap-jmeter-results'
#    apiId='test-api'
    response=client.list_objects_v2(
    Bucket=bucket,
    Delimiter='/',
    Prefix=prefix
    )
    #get folders under prefix
    folders=[]
    try:
        commonPrefixes=response['CommonPrefixes']
        for i in commonPrefixes:
            folderName=i['Prefix'].split('/')[-2]+"/"
            urlPrefix=urllib.parse.quote(i['Prefix'], safe='')
            link="https://"+host+path+"?prefix="+urlPrefix+"&bucket="+bucket+"&region="+REGION+""
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
            link="https://"+bucket+".s3."+REGION+".amazonaws.com/"+e['Key']
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
    return htmlResponse