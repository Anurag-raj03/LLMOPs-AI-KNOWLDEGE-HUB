import boto3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger

class DynamoDBService:
    def __init__(self,table_name:str):
        self.logger=get_logger(f"DynamoDBService[{table_name}]")
        self.table_name=table_name
        self.resource=boto3.resource("dynamodb",region_name=os.getenv("AWS_REGION","us-east-1"))

        self.table=self.resource.Table(table_name)
        self.logger.info(f"Connected to DyanmoDB table: {table_name}")

    def put_item(self,item:dict):
        self.table.put_item(Item=item)
        self.logger.debug(f"Inserted item with keys: {list(item.keys())}") 

    def get_item(self,key:dict):
        response=self.table.get_item(key=key)
        return response.get("Item",None)
    
    def query_items(self, key_name: str, value):
        resp = self.table.scan(FilterExpression=f"{key_name} = :v", ExpressionAttributeValues={":v": value})
        return resp.get("Items", [])
           
    def delete_item(self, key: dict):
        self.table.delete_item(Key=key)
        self.logger.debug(f"Deleted item: {key}")       