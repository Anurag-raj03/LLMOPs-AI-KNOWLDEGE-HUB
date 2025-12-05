import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.redis_services import RedisService
cache=RedisService()
def get_cached_response(query:str):
    return cache.get(f"query:{query}")
def set_cached_response(query:str,response:dict):
    cache.set(f"query:{query}",response,ttl=3600)
    