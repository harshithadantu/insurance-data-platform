import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import requests
import pandas as pd
from utils.logger import get_logger

logger = get_logger()

API_URL = "https://jsonplaceholder.typicode.com/users"

def ingest_api():
    response = requests.get(API_URL)
    
    if response.status_code != 200:
        logger.error("API request failed")
        return
    
    data = response.json()

    df = pd.DataFrame(data)

    df.to_json(
        "data/raw/api_data.json",
        orient="records"
    )

    logger.info("API data ingested")

if __name__ == "__main__":
    ingest_api()