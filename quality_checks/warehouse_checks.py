import pandas as pd
from sqlalchemy import create_engine
from utils.logger import get_logger

logger = get_logger()


def run_warehouse_checks():
    try:
        engine = create_engine("sqlite:///data/warehouse/insurance_warehouse.db")
        df = pd.read_sql("SELECT * FROM policy_claims_table", con=engine)

        logger.info(f"Warehouse row count: {len(df)}")

        if df.empty:
            logger.warning("Warehouse table is empty")
            return

        # Null check
        null_counts = df.isnull().sum()
        logger.info(f"Null counts:\n{null_counts}")

        # Duplicate check on business key
        duplicate_count = df.duplicated(subset=["policy_id", "customer_id"]).sum()
        logger.info(f"Duplicate key count: {duplicate_count}")

        if duplicate_count == 0:
            logger.info("No duplicate business keys found")
        else:
            logger.warning("Duplicate business keys found in warehouse")

    except Exception as e:
        logger.error(f"Warehouse quality checks failed: {e}")
        raise


if __name__ == "__main__":
    run_warehouse_checks()