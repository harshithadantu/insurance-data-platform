import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from utils.logger import get_logger
from cdc.detect_cdc import detect_cdc

logger = get_logger()

STATE_FILE = "data/metadata/pipeline_state.json"
SNAPSHOT_FILE = "data/snapshots/policy_claims_summary_previous.parquet"


def update_pipeline_state():
    os.makedirs("data/metadata", exist_ok=True)

    state = {
        "last_run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_snapshot_file": SNAPSHOT_FILE
    }

    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

    logger.info("Pipeline metadata updated successfully")


def save_snapshot():
    os.makedirs("data/snapshots", exist_ok=True)

    df = pd.read_parquet("data/curated/policy_claims_summary.parquet")
    df.to_parquet(SNAPSHOT_FILE, index=False)
    logger.info("Latest curated snapshot saved successfully")


def load_to_warehouse():
    try:
        logger.info("Warehouse CDC upsert process started")

        cdc_df = detect_cdc()

        if cdc_df.empty:
            logger.info("No new or changed records found. Skipping warehouse load.")
            return

        cdc_df["load_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        os.makedirs("data/warehouse", exist_ok=True)

        db_path = "data/warehouse/insurance_warehouse.db"
        engine = create_engine(f"sqlite:///{db_path}")

        # Table schema must match curated dataframe columns
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS policy_claims_table (
                    policy_id TEXT,
                    customer_id TEXT,
                    policy_type TEXT,
                    premium_amount REAL,
                    policy_start_date TEXT,
                    status TEXT,
                    total_claims_amount REAL,
                    claim_count INTEGER,
                    loss_ratio REAL,
                    cdc_flag TEXT,
                    load_timestamp TEXT
                )
            """))

        logger.info("Warehouse table checked/created successfully")

        key_columns = ["policy_id", "customer_id"]

        with engine.begin() as conn:
            for _, row in cdc_df.iterrows():
                conn.execute(
                    text("""
                        DELETE FROM policy_claims_table
                        WHERE policy_id = :policy_id
                          AND customer_id = :customer_id
                    """),
                    {
                        "policy_id": row["policy_id"],
                        "customer_id": row["customer_id"]
                    }
                )

        rows_to_insert = cdc_df[cdc_df["cdc_flag"].isin(["INSERT", "UPDATE"])]

        if not rows_to_insert.empty:
            rows_to_insert.to_sql(
                "policy_claims_table",
                con=engine,
                if_exists="append",
                index=False
            )

        logger.info(f"Warehouse upsert completed successfully. Processed rows: {len(cdc_df)}")

        save_snapshot()
        update_pipeline_state()

    except Exception as e:
        logger.error(f"Warehouse loading failed: {e}")
        raise


if __name__ == "__main__":
    load_to_warehouse()