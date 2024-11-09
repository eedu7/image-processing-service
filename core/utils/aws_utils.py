from typing import Optional

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from core.config import config
from core.exceptions import BadRequestException


class AWSService:
    """
    A service class for interacting with AWS S3.

    Provides methods for uploading files, generating URLs, and managing S3 objects.
    """

    def __init__(self):
        """
        Initialize the AWSService instance and set up the S3 client.
        """
        self.AWS_ACCESS_KEY = config.AWS_ACCESS_KEY
        self.AWS_SECRET_KEY = config.AWS_SECRET_KEY
        self.BUCKET_NAME = config.AWS_S3_BUCKET_NAME
        self.REGION_NAME = config.AWS_REGION

        # Initialize the S3 client with provided credentials and region
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.AWS_ACCESS_KEY,
            aws_secret_access_key=self.AWS_SECRET_KEY,
            region_name=self.REGION_NAME,
        )

    async def get_image(self, file_name: str) -> bytes:
        try:
            response = self.s3_client.get_object(Bucket=self.BUCKET_NAME, Key=file_name)
            return response['Body'].read()

        except NoCredentialsError:
            raise BadRequestException("AWS credentials not available.")
        except ClientError as e:
            raise BadRequestException(f"Error retrieving object: {e.response['Error']['Message']}")
        except Exception as e:
            raise BadRequestException(f"Unexpected error: {str(e)}")

    async def upload_image_to_s3(
        self, file_data: bytes, file_name: str, content_type: str
    ) -> str:
        """
        Upload an image to the S3 bucket and return its URL.

        Args:
            file_data (bytes): The file data in bytes.
            file_name (str): The name of the file to be saved.
            content_type (str): The MIME type of the file.

        Returns:
            str: The public URL of the uploaded file.

        Raises:
            BadRequestException: If there are issues during the upload process.
        """
        try:
            self.s3_client.put_object(
                Bucket=self.BUCKET_NAME,
                Key=file_name,
                Body=file_data,
                ContentType=content_type,
            )
            return await self.create_image_url(file_name)

        except NoCredentialsError:
            raise BadRequestException("AWS credentials not available.")
        except ClientError as e:
            raise BadRequestException(
                f"Error uploading image: {e.response['Error']['Message']}"
            )
        except Exception as e:
            raise BadRequestException(f"Unexpected error: {str(e)}")

    async def create_image_url(self, file_name: str) -> str:
        """
        Generate the public URL for an object stored in S3.

        Args:
            file_name (str): The name of the file in the S3 bucket.

        Returns:
            str: The public URL of the file.
        """
        return f"https://{self.BUCKET_NAME}.s3.{self.REGION_NAME}.amazonaws.com/{file_name}"

    async def generate_presigned_url(
        self, file_name: str, expiration: int = 3600
    ) -> str:
        """
        Generate a presigned URL for accessing an object in S3.

        Args:
            file_name (str): The name of the file in the S3 bucket.
            expiration (int): The time in seconds for the URL to remain valid. Defaults to 3600.

        Returns:
            str: The presigned URL.

        Raises:
            BadRequestException: If there are issues generating the presigned URL.
        """
        try:
            return self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.BUCKET_NAME, "Key": file_name},
                ExpiresIn=expiration,
            )
        except NoCredentialsError:
            raise BadRequestException("AWS credentials not available.")
        except ClientError as e:
            raise BadRequestException(
                f"Error generating presigned URL: {e.response['Error']['Message']}"
            )
        except Exception as e:
            raise BadRequestException(f"Unexpected error: {str(e)}")

    async def delete_object(self, file_name: str) -> None:
        """
        Delete an object from the S3 bucket.

        Args:
            file_name (str): The name of the file to delete.

        Raises:
            BadRequestException: If there are issues deleting the object.
        """
        try:
            self.s3_client.delete_object(Bucket=self.BUCKET_NAME, Key=file_name)
        except NoCredentialsError:
            raise BadRequestException("AWS credentials not available.")
        except ClientError as e:
            raise BadRequestException(
                f"Error deleting object: {e.response['Error']['Message']}"
            )
        except Exception as e:
            raise BadRequestException(f"Unexpected error: {str(e)}")
