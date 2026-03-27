import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logger import get_logger
import pandas as pd
logger = get_logger()

def standardize_policies():

    #load data
    df_policy=pd.read_json("data/raw/policies.json")
    logger.info("policies data loaded successfully")

    #standardize column names
    df_policy.columns=df_policy.columns.str.lower().str.strip()

    #standardize date formats
    df_policy["policy_start_date"]=pd.to_datetime(df_policy["policy_start_date"],errors='coerce')

    #standardize numeric columns
    df_policy["premium_amount"]=pd.to_numeric(df_policy["premium_amount"],errors='coerce')

    #store standardized data
    df_policy.to_parquet("data/standardized/policies.parquet",engine='pyarrow')
    logger.info("standardized data stored successfully")

if __name__=="__main__":
    standardize_policies()