import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def get_logger(name: str):
    """
    Returns specific Logger for each file.
    """
    return logging.getLogger(name)

def fetch_with_retry(fn, max_retries=3, delay_seconds=5, logger=None):
    """
    Executes a function with an automatic retry mechanism.
    
    Designed for transient failures in I/O operations, API calls, and database connections.    
    """
    if logger is None:
        logger = get_logger(__name__)

    for attempt in range(1,max_retries + 1):
        try:
            return fn()
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                logger.error("All retry ateempts failed.")
                raise
            time.sleep(delay_seconds)