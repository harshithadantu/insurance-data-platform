import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from utils.logger import get_logger
from sqlalchemy import create_engine

logger=get_logger()

engine=create_engine("sqlite:///data/source/sample.db")

def ingest_data():

    query="SELECT * FROM claims"
    df=pd.read_sql(query,engine)
    df.to_json("data/raw/db_claims.json",orient='records')
    logger.info("Data ingested successfully")

if __name__=="__main__":
    ingest_data()