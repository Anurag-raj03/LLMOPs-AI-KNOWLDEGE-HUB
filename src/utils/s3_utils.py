import boto3
import os
import subprocess
from src.utils.logger import get_logger

logger = get_logger("S3Utils")

def upload_json_to_s3(file_path, s3_key):
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    bucket = os.getenv("S3_BUCKET", "ai-knowledgehub-bucket")
    s3.upload_file(file_path, bucket, s3_key)
    logger.info(f"Uploaded {file_path} → s3://{bucket}/{s3_key}")

def download_from_s3(s3_key, dest_path):
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    bucket = os.getenv("S3_BUCKET", "ai-knowledgehub-bucket")
    s3.download_file(bucket, s3_key, dest_path)
    logger.info(f"Downloaded s3://{bucket}/{s3_key} → {dest_path}")

def sync_s3(local_path: str, direction: str = "upload"):
    """
    Sync a local directory with an S3 bucket using AWS CLI.
    
    Args:
        local_path: Local directory to sync (e.g. 'data/processed/')
        direction: "upload" or "download"
    """
    bucket = os.getenv("S3_BUCKET", "ai-knowledgehub-bucket")
    region = os.getenv("AWS_REGION", "us-east-1")


    cmd = None
    if direction == "upload":
        cmd = ["aws", "s3", "sync", local_path, f"s3://{bucket}/{local_path}", "--region", region]
    else:
        cmd = ["aws", "s3", "sync", f"s3://{bucket}/{local_path}", local_path, "--region", region]

    logger.info(f"Syncing {direction} → {local_path}")
    try:
        subprocess.run(cmd, check=True)
        logger.info(f"S3 sync {direction} completed for {local_path}")
    except subprocess.CalledProcessError as e:
        logger.error(f"S3 sync failed: {e}")
