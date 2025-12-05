import asyncio
import time
from tenacity import retry,stop_after_attempt,wait_exponential

@retry(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=2,min=1,max=10))
def safe_run(func,*args,**kwargs):
    return func(*args,**kwargs)

async def run_parallel(tasks):
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
def exponential_backoff(base=2, max_time=60):
    t = 1
    while t < max_time:
        yield t
        t *= base