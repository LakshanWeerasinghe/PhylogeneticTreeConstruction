import logging
import boto3
from boto3 import client
from botocore.exceptions import ClientError
from botocore.client import Config

from app.settings import AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_STORAGE_BUCKET_NAME


def get_s3_client():

    """
    Create the boto3 client todo aws s3 operations

    :return: boto3 client connection

    """

    return boto3.client(
                        's3',
                        aws_access_key_id= AWS_ACCESS_KEY_ID,
                        aws_secret_access_key= AWS_SECRET_ACCESS_KEY,
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-2'
                        )
    

def create_preassinged_url(directory_name, object_name, expiration=3600):

    """
    Generate a presigned URL S3 PUT request to upload a file

    :param directory_name : string
    :param object_name: string
    :return: url to put the file
    :return: None if error.

    """

    # Generate a presigned S3 POST URL
    s3_client = get_s3_client()
    try:

        object_key = str(directory_name) + '/' + str(object_name)

        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': AWS_STORAGE_BUCKET_NAME,
                                                            'Key': object_key},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None
        
    # The response contains the presigned URL and required fields
    return response



def download_files_from_bucket(bucket_name, object_name, file_name): 
    #object_name - file name in the bucket, file_name - path to download and the file name to save
    
    s3_client = get_s3_client()
    try:
        s3_client.download_file(bucket_name,object_name,file_name)   #Download to root directory
    except ClientError as e:
        if e.response['Error']['Code']=='404':
            print ("Object not found")
        else:
            raise

def list_all_file_names_from_bucket (bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    exists = True
    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False

        for item in bucket.objects.all():
            print(item.file_name)
