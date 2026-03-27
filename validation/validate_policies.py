import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.logger import get_logger
import great_expectations as ge
import pandas as pd

logger = get_logger()


def validate_policies():
    file_path = "data/standardized/policies.parquet"

    # 1. Check if file exists
    if not os.path.exists(file_path):
        logger.error(f"File not found at path: {file_path}")
        raise FileNotFoundError(f"File not found at path: {file_path}")

    logger.info("file exists. Starting validation process.")

    # 2. Load the data
    df = pd.read_parquet(file_path)
    logger.info("Policies data loaded successfully")

    # 3. Standardize again for safe validation
    df["status"] = df["status"].astype(str).str.strip().str.lower()

    # 4. Dataset structure inspection
    logger.info(f"Rows:{df.shape[0]}")
    logger.info(f"columns:{df.shape[1]}")
    logger.info(f"Column names:{list(df.columns)}")
    logger.info(f"Data types:\n{df.dtypes}")

    # Optional debug
    logger.info(f"Unique status values: {df['status'].unique()}")

    # 5. Convert to Great Expectations dataframe
    df_ge = ge.from_pandas(df)

    # 6. Schema validation
    df_ge.expect_table_columns_to_match_ordered_list([
        "policy_id",
        "customer_id",
        "policy_type",
        "premium_amount",
        "policy_start_date",
        "status"
    ])

    # 7. Null value checks
    df_ge.expect_column_values_to_not_be_null("policy_id")
    df_ge.expect_column_values_to_not_be_null("customer_id")
    df_ge.expect_column_values_to_not_be_null("premium_amount")
    df_ge.expect_column_values_to_not_be_null("policy_start_date")
    df_ge.expect_column_values_to_not_be_null("status")

    # 8. Range checks
    df_ge.expect_column_values_to_be_between("premium_amount", min_value=0)

    # 9. Categorical checks
    valid_status_values = ["active", "expired", "cancelled"]
    df_ge.expect_column_values_to_be_in_set("status", valid_status_values)

    # 10. Row count check
    if df.shape[0] == 0:
        logger.error("No records found in policies data.")
        raise ValueError("No records found in policies data.")

    # 11. Invalid rows
    invalid_rows = df[
        (df["policy_id"].isnull()) |
        (df["customer_id"].isnull()) |
        (df["premium_amount"].isnull()) |
        (df["premium_amount"] < 0) |
        (df["policy_start_date"].isnull()) |
        (df["status"].isnull()) |
        (~df["status"].isin(valid_status_values))
    ]
    logger.info(f"Number of invalid records found: {invalid_rows.shape[0]}")

    # 12. Valid rows
    valid_rows = df.drop(invalid_rows.index)
    logger.info(f"Number of valid records found: {valid_rows.shape[0]}")

    # 13. Create output folders
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/bad_records", exist_ok=True)

    # 14. Store clean data for transformation
    valid_rows.to_parquet("data/processed/policies_clean.parquet", engine="pyarrow")
    logger.info("Cleaned policies data stored successfully.")

    # 15. Store invalid rows for review
    invalid_rows.to_parquet("data/bad_records/policies_invalid.parquet", engine="pyarrow")
    logger.info("Invalid policies data stored successfully.")

    logger.info("Policies data validation completed.")


if __name__ == "__main__":
    validate_policies()