"""
This module has tools required for using S3,
currently only uploading image files to an AWS S3 bucket.

It initializes an S3 client using credentials loaded from environment variables
and provides a function to upload images, returning their public URL.
"""

import uuid
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="eu-north-1"
)

BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")


def upload_image(file):
    """
    Upload an image file to the configured S3 bucket and return its public URL.

    Args:
        file: A file-like object with attributes `filename`, `file`, and `content_type`.

    Returns:
        str: The public URL of the uploaded image.
    """
    file_ext = file.filename.split(".")[-1]
    key = f"cat-images/{uuid.uuid4()}.{file_ext}"
    s3.upload_fileobj(
        file.file,
        BUCKET_NAME,
        key,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file.content_type
        }
    )

    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
    return url
