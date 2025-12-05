import os
import yaml
from dotenv import load_dotenv

load_dotenv()

def load_config(path="config.yml"):
    if not os.path.exists(path):
        return {}
    with open (path,"r") as f:
        return yaml.safe_load(f)

def get_env(key,default=None):
    return os.getenv(key,default)
    