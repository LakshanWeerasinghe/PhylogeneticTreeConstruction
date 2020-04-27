import logging
import boto3
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
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        region_name='us-east-2'
    )


def upload_file(file_name, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = get_s3_client()
    try:
        response = s3_client.upload_file(
            file_name, AWS_STORAGE_BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


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


def download_files_from_bucket(object_name, location):
    """
    Download dna file from the S3 bucket

    :param object_name : string
    :param location : string

    """
    s3_client = get_s3_client()
    s3_client.download_file(AWS_STORAGE_BUCKET_NAME, object_name, location)
