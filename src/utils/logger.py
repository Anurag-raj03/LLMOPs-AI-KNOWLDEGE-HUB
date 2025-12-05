import logging 
import os 
def get_logger(name:str):
    logger=logging.getLogger(name)
    handler=logging.StreamHandler()
    formatter=logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s")
    handler.setFormatter(formatter)
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(os.getenv("LOG_LEVEL","INFO"))
    return logger   