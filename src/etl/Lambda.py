import boto3
from botocore.exceptions import ClientError
import botocore.vendored.requests.packages.urllib3 as urllib3
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

def lambda_handler(event, context):
    """
    This Lambda function uploads the latest GDELT 2.0 Events file to S3.
    New GDELT files are posted every 15 minutes here: http://data.gdeltproject.org/gdeltv2/lastupdate.txt.
    Use EventBridge to schedule Lambda at your desired frequency.
    """
    
    # Find latest Events file URL
    newFile = urlopen("http://data.gdeltproject.org/gdeltv2/lastupdate.txt").readline().decode('UTF-8')
    fileURL = newFile.split(' ')[-1]
    fileName = fileURL.split('/')[-1].replace('.zip','').strip()
    
    # Download and extract - since file is incremental it will be under 500MB Lambda limit
    fileContent = urlopen(fileURL).read()
    zipfile = ZipFile(BytesIO(fileContent))
    zipfile.extractall('/tmp/')
    
    # Upload the file
    s3_client = boto3.client('s3')
    bucket = 'gdelt-12232022' #or your S3 bucket name
    
    try:
        response = s3_client.upload_file('/tmp/'+fileName, bucket, 'gdelt/'+fileName)
    except ClientError as e:
            return {
        'statusCode': 400,
        'body': e
        }
    return {
        'statusCode': 200,
        'body':  bucket+'/gdelt/'+fileName+' was loaded successfully.'
    }
