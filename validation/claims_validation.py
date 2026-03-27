import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.logger import get_logger
import great_expectations as ge
import pandas as pd

logger=get_logger()

def validate_claims():
    file_path="data/standardized/claims.parquet"

    #1 check if file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found at path: {file_path}")

    logger.info("file exists. Starting validation process.")

    #2 Load the data
    df=pd.read_parquet(file_path)
    logger.info("Claims data loaded successfully")

    #3 Dataset  structure inspection
    logger.info(f"claims data structure: {df.info()}")
    logger.info(f"Rows:{df.shape[0]}")
    logger.info(f"Columns:{df.shape[1]}")
    logger.info(f"Column names:{list(df.columns)}")

    #4 convert to Great Expectations dataframe

    df_ge=ge.from_pandas(df)

    #5 schema validation
    df_ge.expect_table_columns_to_match_ordered_list([
        "policy_id",
        "customer_id",
        "claim_amount",
        "status"
    ])

    #6 Data type validation
    df_ge.expect_column_values_to_be_of_type("policy_id","int64")
    df_ge.expect_column_values_to_be_of_type("customer_id","int64")
    df_ge.expect_column_values_to_be_of_type("claim_amount","float64")
    df_ge.expect_column_values_to_be_of_type("status","object") 
    

    #7 null value checks
    df_ge.expect_column_values_to_not_be_null("policy_id")
    df_ge.expect_column_values_to_not_be_null("customer_id")

    #8 duplicate checks
    df_ge.expect_column_values_to_be_unique("policy_id")


    #9 range checks
    df_ge.expect_column_values_to_be_between("claim_amount",min_value=0)

    #10 categorical checks
    df_ge.expect_column_values_to_be_in_set("status",["Approved","Rejected","Pending"])

    #11 row count validation
    if df.shape[0]==0:
        logger.error("Empty dataset. No rows to validate.")
    
    #12 Outlier detection
    avg_claims=df["claim_amount"].mean()

    logger.info(f"Average claim amount:{avg_claims}")

    #13identify invalid rows
    invalid_rows=df[(df["claim_amount"]<0) | (df["policy_id"].isnull()) | (df["customer_id"].isnull())] 
    logger.info(f"Invalid rows:{invalid_rows.shape[0]}")

    #14 valid rows
    valid_rows=df.drop(invalid_rows.index)

    logger.info(f"Valid rows :{valid_rows.shape[0]}")
    logger.info(f"Invalid rows:{invalid_rows.shape[0]}")

    #15 store clean data
    valid_rows.to_parquet("data/processed/claims_clean.parquet",engine="pyarrow")
    logger.info("Cleaned claims data stored successfully.")

    #16save invalid rows for review
    invalid_rows.to_parquet("data/bad_records/claims_invalid.parquet",engine="pyarrow")
    logger.info("Invalid claims data stored successfully.")

    logger.info("Claims data validation completed.")

if __name__=="__main__":
    validate_claims()