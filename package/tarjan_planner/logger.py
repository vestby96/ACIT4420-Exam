import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='package/tarjan_planner/tarjan_planner.log',
    filemode='a'
)

# Define the decorator
def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # Execute the wrapped function
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.info(f"Method {func.__name__} executed in {elapsed_time:.2f} seconds.")
        return result
    return wrapper