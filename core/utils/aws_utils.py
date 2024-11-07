from typing import Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from core.config import config
from core.exceptions import BadRequestException

AWS_ACCESS_KEY = config.AWS_ACCESS_KEY
AWS_SECRET_KEY = config.AWS_SECRET_KEY
BUCKET_NAME = config.AWS_S3_BUCKET_NAME
REGION_NAME = config.AWS_REGION


def upload_image_to_s3(
    file_data: bytes, s3_key: str, content_type: str
) -> Optional[str]:
    """
    Upload an image to an AWS S3 bucket.

    :param file_data: The image file data as bytes.
    :param s3_key: The key (path) to store the file in the bucket.
    :param content_type: The MIME type of the file (e.g., 'image/jpeg').
    :return: The public URL of the uploaded image if successful, None otherwise.
    """
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=REGION_NAME,
        )
        # Upload the file to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_data,
            ContentType=content_type,
            ACL="public-read",
        )
        # Construct the public URL
        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{s3_key}"
        return url
    except NoCredentialsError:
        raise BadRequestException("AWS credentials not available.")
    except ClientError as e:
        raise BadRequestException(f"Error uploading image: {e}")
    except Exception as e:
        raise BadRequestException(f"Unexpected error: {e}")
