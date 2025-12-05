import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from retriever.hybrid_retriever import HybridRetriever
from services.redis_services import RedisService
from services.dynamodb_service import DynamoDBService
from utils.logger import get_logger
logger=get_logger("Dependencies")
retriever=HybridRetriever()
retriever.setup()
redis_cache=RedisService()
feedback_db=DynamoDBService("FeedbackTable")
