import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from utils.logger import get_logger

logger=get_logger()

def transform_claims():

    #1 Load clean data set 
    df=pd.read_parquet("data/processed/claims_clean.parquet",engine="pyarrow")
    logger.info("Cleaned claims data loaded successfully.")
    print(df.columns)

    #2 claim by status
    claim_by_status=df.groupby("status").size().reset_index(name="claim_count")
    logger.info("Claim by status transformation completed.")

    #3 Customer claim totals
    customer_claims=df.groupby("customer_id")["claim_amount"].sum().reset_index(name="total_claim_amount")
    logger.info("Customer claims transformation completed.")

    #4 Average claim amount
    average_claim_amount=df["claim_amount"].mean()
    logger.info("Average claim amount transformation completed.")

    #5 Identify high risk customers
    high_risk_customers=customer_claims[customer_claims["total_claim_amount"] > 10000]
    logger.info("High risk customers identified.")

    #6 save analytics datasets
    claim_by_status.to_parquet("data/curated/claim_by_status.parquet",engine="pyarrow")
    customer_claims.to_parquet("data/curated/customer_claims.parquet",engine="pyarrow")
    high_risk_customers.to_parquet("data/curated/high_risk_customers.parquet",engine="pyarrow")
    
    logger.info("Transformations completed successfully.")

if __name__=="__main__":
    transform_claims()