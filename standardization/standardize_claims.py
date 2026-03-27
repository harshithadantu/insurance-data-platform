import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from utils.logger import get_logger
logger=get_logger()

def claims_standardization():
    #load data
    df_claims=pd.read_json("data/raw/claims.json")
    logger.info("claims data loaded successfully")

    #standardize column names
    df_claims.columns=df_claims.columns.str.lower().str.strip()

    #standardize numeric columns
    df_claims["claim_amount"]=pd.to_numeric(df_claims["claim_amount"],errors='coerce')

    #store standardized data
    df_claims.to_parquet("data/standardized/claims.parquet",engine='pyarrow')
    logger.info("standardized data stored successfully")

if __name__=="__main__":
    claims_standardization()