import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pandas as pd
from utils.logger import get_logger

logger = get_logger()

def transform_api():

    df = pd.read_json("data/raw/api_data.json")

    # select useful columns
    df = df[["id", "name", "email"]]

    # rename columns (standardization)
    df = df.rename(columns={
        "id": "user_id"
    })

    # remove duplicates
    df = df.drop_duplicates()

    # save processed
    df.to_parquet(
        "data/processed/users_clean.parquet",
        index=False
    )

    logger.info("API data transformed and saved")


if __name__ == "__main__":
    transform_api()