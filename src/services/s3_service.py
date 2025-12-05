import boto3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
from utils.logger import get_logger

class S3Service:
    def __init__(self):
        self.logger=get_logger("S3Service")
        self.s3=boto3.client("s3",region_name=os.getenv("AWS_REGION","us-east-1"))
        self.bucket=os.getenv("S3_BUCKET","ai-knowledgehub-bucket")
        self.logger.info(f"Connected to s3 bucket: {self.bucket}")

    def upload_file(self,file_path:str,key:str):
        self.s3.upload_file(file_path,self.bucket,key)
        self.logger.debug(f"Upload {file_path} s3://{self.bucket}/{key}")

    def download_file(self, key: str, dest_path: str):
        self.s3.download_file(self.bucket, key, dest_path)
        self.logger.debug(f"Downloaded s3://{self.bucket}/{key} → {dest_path}")

    def list_files(self, prefix: str = ""):
        resp = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        return [obj["Key"] for obj in resp.get("Contents", [])]

    def delete_file(self, key: str):
        self.s3.delete_object(Bucket=self.bucket, Key=key)
        self.logger.debug(f"Deleted s3://{self.bucket}/{key}")        