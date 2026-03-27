import logging
import os

os.makedirs("utils", exist_ok=True)
#configure logging
logging.basicConfig(
    filename="utils/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_logger():
    return logging.getLogger()