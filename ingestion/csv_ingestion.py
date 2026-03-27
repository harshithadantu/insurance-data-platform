import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import  pandas as pd
from utils.logger import get_logger

logger=get_logger()

def ingest_csv():
    df=pd.read_csv("data/source/policies.csv")
    logger.info("CSV data ingested successfully.")

    df.to_json("data/raw/policies.json",orient="records")

    logger.info("CSV converted to raw JSON successfully.")

if __name__=="__main__":
    ingest_csv()