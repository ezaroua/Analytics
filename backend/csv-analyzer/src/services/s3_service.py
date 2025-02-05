import boto3
from typing import Dict, Any, Optional
import logging
from botocore.exceptions import ClientError

class S3Service:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name
        self.logger = logging.getLogger(__name__)

    def generate_presigned_url(self, file_key: str, expiration: int = 3600) -> Optional[str]:
        """Generate a presigned URL for file upload"""
        try:
            return self.s3.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_key,
                    'ContentType': 'text/csv',
                },
                ExpiresIn=expiration,
            )
        except ClientError as e:
            self.logger.error(f"Error generating presigned URL: {e}")
            return None

    def get_file(self, file_key: str) -> Optional[Dict[str, Any]]:
        """Get file from S3"""
        try:
            return self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
        except ClientError as e:
            self.logger.error(f"Error getting file from S3: {e}")
            return None

    def delete_file(self, file_key: str) -> bool:
        """Delete file from S3"""
        try:
            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=file_key
            )
            return True
        except ClientError as e:
            self.logger.error(f"Error deleting file from S3: {e}")
            return False

    def list_files(self, prefix: str = '') -> Optional[Dict[str, Any]]:
        """List files in S3 bucket with given prefix"""
        try:
            return self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        except ClientError as e:
            self.logger.error(f"Error listing files in S3: {e}")
            return None
