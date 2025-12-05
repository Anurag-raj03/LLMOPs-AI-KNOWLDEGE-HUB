import redis
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import get_logger

class RedisService:
    def __init(self):
        self.logger=get_logger("RedisService")
        redis_url=os.getenv("REDIS_URL","redis://localhost:6379")
        self.client=redis.StrictRedis.from_url(redis_url,decode_responses=True)
        self.logger.info(f"Connected to Redis at {redis_url}")

    def set(self,key:str,value:dict,ttl:int=3600):
        self.client.set(key,json.dumps(value),ex=ttl)
        self.logger.debug(f"Cached key: {key}")

    def get(self, key: str):
        val = self.client.get(key)
        if val:
            return json.loads(val)
        return None

    def publish(self, channel: str, message: dict):
        self.client.publish(channel, json.dumps(message))
        self.logger.debug(f"Published message on {channel}")

    def subscribe(self, channel: str):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel)
        self.logger.info(f"Subscribed to {channel}")
        return pubsub     