import boto3
import uuid
import os
from dotenv import load_dotenv
from .logger import logger

load_dotenv()

s3 = boto3.client("s3", aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                  region_name="eu-north-1")

BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")


def upload_image(file):
    logger.info(file.file)
    file_ext = file.filename.split(".")[-1]
    key = f"cat-images/{uuid.uuid4()}.{file_ext}"
    s3.upload_fileobj(file.file, BUCKET_NAME, key)

    return key
