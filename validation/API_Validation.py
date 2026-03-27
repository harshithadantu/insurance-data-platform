import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.logger import get_logger
import great_expectations as ge
import pandas as pd
import re

logger = get_logger()


def api_users_validation():

    file = "data\\raw\\api_data.json"

    # -----------------------------
    # Check if file exists
    # -----------------------------
    if not os.path.exists(file):
        logger.error(f"File not exists at path: {file}")
        return

    logger.info("File exists. Start validation")

    # -----------------------------
    # Load data
    # -----------------------------
    df = pd.read_json(file)
    logger.info("API data loaded successfully")

    # -----------------------------
    # Dataset structure inspection
    # -----------------------------
    logger.info(f"API data rows: {df.shape[0]}")
    logger.info(f"API data columns: {df.shape[1]}")
    logger.info(f"API columns: {list(df.columns)}")

    # -----------------------------
    # Convert to Great Expectations
    # -----------------------------
    df_ge = ge.from_pandas(df)

    # -----------------------------
    # Schema validation
    # -----------------------------
    df_ge.expect_table_columns_to_match_ordered_list([
        "id",
        "name",
        "username",
        "email"
    ])

    # -----------------------------
    # Null checks
    # -----------------------------
    df_ge.expect_column_values_to_not_be_null("id")
    df_ge.expect_column_values_to_not_be_null("name")
    df_ge.expect_column_values_to_not_be_null("email")

    # -----------------------------
    # Email validation function
    # -----------------------------
    def is_valid_email(email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(pattern, str(email)))

    # -----------------------------
    # Add error reason column
    # -----------------------------
    df["error_reason"] = ""

    df.loc[df["id"].isnull(), "error_reason"] = "Missing id"
    df.loc[df["name"].isnull(), "error_reason"] = "Missing name"
    df.loc[df["email"].isnull(), "error_reason"] = "Missing email"
    df.loc[~df["email"].apply(is_valid_email), "error_reason"] = "Invalid email"

    # -----------------------------
    # Invalid rows
    # -----------------------------
    invalid_rows = df[df["error_reason"] != ""]
    logger.warning(f"Number of invalid rows: {invalid_rows.shape[0]}")

    # -----------------------------
    # Valid rows
    # -----------------------------
    valid_rows = df[df["error_reason"] == ""].copy()

    logger.info(f"Number of valid rows: {valid_rows.shape[0]}")

    # -----------------------------
    # Keep only required columns
    # -----------------------------
    valid_rows = valid_rows[["id", "name", "email"]]

    # -----------------------------
    # Save valid data
    # -----------------------------
    valid_rows.to_parquet(
        "data/processed/users_clean.parquet",
        index=False
    )
    logger.info("Valid API users stored successfully")

    # -----------------------------
    # Save invalid data
    # -----------------------------
    if not invalid_rows.empty:
        invalid_rows.to_json(
            "data/bad_records/users_rejected.json",
            orient='records'
        )
        logger.warning("Invalid API users stored successfully")

    logger.info("API validation completed")


if __name__ == "__main__":
    api_users_validation()