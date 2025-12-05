import boto3
import json
import os
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger

class SQSService:
    def __init__(self,queue_name:str):
        self.logger=get_logger(f"SQSService[{queue_name}]")
        self.sqs=boto3.client("sqs",region_name=os.getenv("AWS_REGION","us-east-1"))
        self.queue_url=self.sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]

    def send_message(self,message:dict):
        self.sqs.send_message(QueueUrl=self.queue_url, MessageBody=json.dumps(message)) 
        self.logger.info(f"Sent message to {self.queue_url}")

    def poll_message(self,max_messages:int=1):
        resp=self.sqs.receive_message(QueueUrl=self.queue_url,MaxNumberofMessages=max_messages,WaitTimeSecond=5)
        messages=[json.loads(m["Body"]) for m in resp.get("Messages",[])]
        for m in resp.get("Message",[]):
            self.sqs.delete_message(QueueUrl=self.queue_url,ReceiptHandle=m["ReceiptHandle"])
            if messages:
                self.logger.debug(f"Retrieved {len(messages)} messages from {self.queue_url}")
            return messages          