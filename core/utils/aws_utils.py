import boto3
from botocore.exceptions import ClientError
from typing import Optional
from icecream import ic


class S3Service:
    def __init__(self, bucket_name: str, s3_key: str, region_name: str):
        self.s3_client = boto3.client("s3", region_name=region_name)
        self.bucket_name = bucket_name
        self.s3_key = s3_key

    async def upload_file(self, file):
        try:
            self.s3_client.upload_file(file, self.bucket_name, self.s3_key)
            return True
        except ClientError as e:
            return False

    async def get_file_url(self, s3_key: str, expiration: int = 3600) -> Optional[str]:
        """Generate a pre-signed URL for the file if it is an image"""
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            content_type = response.get("ContentType")
            if "image" in content_type:
                url = self.s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket_name, "Key": s3_key},
                    ExpiresIn=expiration,
                )
                return url
            else:
                ic("File is not an image, cannot generate URL.")
                return None
        except ClientError as e:
            ic(f"Error generating URL: {e}")
            return None
