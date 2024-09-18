import os
import boto3
from integrations.base_storage import BaseStorage

class S3Client(BaseStorage):
    def __init__(self, aws_access_key_id, aws_secret_access_key, region, bucket):
        """Initialize the S3 client using environment variables."""
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region,
        )
        self.bucket = bucket

    def download_model(self, s3_key, local_file_path):
        """Download a model from S3."""
        try:
            print(f"Downloading {s3_key} from S3 bucket {self.bucket}...")
            self.s3.download_file(self.bucket, s3_key, local_file_path)
            print(f"Model saved locally at {local_file_path}")
        except Exception as e:
            print(f"Error downloading model from S3: {e}")
