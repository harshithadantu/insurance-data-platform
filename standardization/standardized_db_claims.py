import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logger import get_logger
logger=get_logger()

def standardize_db_claims():
    #load data
    df_db_claims=pd.read_json("data/raw/db_claims.json")
    logger.info("claims data loaded successfully")

    #standardize column names
    df_db_claims.columns=df_db_claims.columns.str.lower().str.strip()

    #standardize numeric columns
    df_db_claims["claim_amount"]=pd.to_numeric(df_db_claims["claim_amount"],errors='coerce')

    #store standardized data
    df_db_claims.to_parquet("data/standardized/db_claims.parquet",engine='pyarrow')
    logger.info("standardized data stored successfully")

if __name__=="__main__":
    standardize_db_claims()
    