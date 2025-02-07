import boto3
from typing import Dict, Any, Optional, Tuple
import logging
from botocore.exceptions import ClientError
import chardet


class S3Service:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client("s3")
        self.bucket_name = bucket_name
        self.logger = logging.getLogger(__name__)

    def get_file_content(self, file_key: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get file content from S3 and detect encoding
        Returns: Tuple[content, encoding]
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
            raw_content = response["Body"].read()

            # Detect encoding
            result = chardet.detect(raw_content)
            encoding = result["encoding"] or "utf-8"

            # Try multiple encodings if first one fails
            encodings_to_try = [encoding, "utf-8", "ISO-8859-1", "cp1252"]

            for enc in encodings_to_try:
                try:
                    content = raw_content.decode(enc)
                    self.logger.info(f"Successfully decoded file with {enc} encoding")
                    return content, enc
                except UnicodeDecodeError:
                    continue

            raise ValueError(
                f"Could not decode file with any encoding: {encodings_to_try}"
            )

        except ClientError as e:
            self.logger.error(f"Error getting file from S3: {e}")
            return None, None
        except Exception as e:
            self.logger.error(f"Error processing file content: {e}")
            return None, None

    def get_file(self, file_key: str) -> Optional[Dict[str, Any]]:
        """Get raw file object from S3"""
        try:
            return self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
        except ClientError as e:
            self.logger.error(f"Error getting file from S3: {e}")
            return None

    def generate_presigned_url(
        self, file_key: str, expiration: int = 3600
    ) -> Optional[str]:
        """Generate a presigned URL for file upload"""
        try:
            return self.s3.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": file_key,
                    "ContentType": "text/csv",
                },
                ExpiresIn=expiration,
            )
        except ClientError as e:
            self.logger.error(f"Error generating presigned URL: {e}")
            return None

    def delete_file(self, file_key: str) -> bool:
        """Delete file from S3"""
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=file_key)
            return True
        except ClientError as e:
            self.logger.error(f"Error deleting file from S3: {e}")
            return False

    def list_files(self, prefix: str = "") -> Optional[Dict[str, Any]]:
        """List files in S3 bucket with given prefix"""
        try:
            return self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        except ClientError as e:
            self.logger.error(f"Error listing files in S3: {e}")
            return None
