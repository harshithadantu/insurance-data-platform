import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.logger import get_logger
import great_expectations as ge
import pandas as pd
logger=get_logger()

def db_claims_validation():
    file="data\\standardized\\db_claims.parquet"

    #Check if file exists
    if not os.path.exists(file):
        logger.info(f"File not exists at path :{file}")
    logger.info("File exists.Start validation")

    #load data 
    df=pd.read_parquet(file)
    logger.info("db_claims loaded successfully")

    
    #Dataset structure inspection
    logger.info(f"db_claims structure :{df.info()}")
    logger.info(f"db_claims rows:{df.shape[0]}")
    logger.info(f"db_claims column:{df.shape[1]}")
    logger.info(f"db_claims columns:{list(df.columns)}")

    #convert to great expectations data frame
    df_ge=ge.from_pandas(df)

    #schema validation
    df_ge.expect_table_columns_to_match_ordered_list([
        "policy_id",
        "customer_id",
        "claim_amount",
        "status"
    ])

    #null value check
    df_ge.expect_column_values_to_not_be_null("policy_id")
    df_ge.expect_column_values_to_not_be_null("customer_id")

    #Range checks
    df_ge.expect_column_values_to_be_between("claim_amount",min_value=0)

    #Categorical checks
    df_ge.expect_column_values_to_be_in_set("status",["Approved","Rejected","Pending"])

    #row count checks
    if df.shape[0]==0:
        logger.error("No records found in db_claims data")

    #invalid rows
    invalid_rows=df[(df["claim_amount"]<0) | (~df["status"].isin(["Approved","Rejected","Pending"]))]

    logger.info(f"Number of invalid rows in db_claims data :{invalid_rows.shape[0]}")

    #valid rows
    valid_rows=df.drop(invalid_rows.index)
    logger.info(f"Number of valid rows in db_claims data :{valid_rows.shape[0]}")

    #store valid rows in a new file
    valid_rows.to_json("data/processed/valid_db_claims.json",orient='records')
    logger.info("Valid db_claims data stored successfully")

    invalid_rows.to_json("data/bad_records/invalid_db_claims.json",orient='records')
    logger.info("Invalid db_claims data stored successfully")

if __name__=="__main__":
    db_claims_validation()
