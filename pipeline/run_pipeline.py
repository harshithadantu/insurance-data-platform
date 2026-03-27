import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ingestion.api_ingestion import ingest_api
from ingestion.database_ingestion import ingest_data
from ingestion.csv_ingestion import ingest_csv

from standardization.standardize_claims import claims_standardization
from standardization.standardize_policies import standardize_policies
from standardization.standardized_db_claims import standardize_db_claims

from validation.claims_validation import validate_claims
from validation.validate_policies import validate_policies
from validation.validate_db_claims import db_claims_validation

from transformation.join_policy_claim import join_policy_claims

from loading.load_to_warehouse import load_to_warehouse
from quality_checks.warehouse_checks import run_warehouse_checks

from utils.logger import get_logger

logger = get_logger()


def run_pipeline():
    try:
        # ingest data
        logger.info("Starting data ingestion...")
        ingest_csv()
        ingest_api()
        ingest_data()
        logger.info("Data ingestion completed.")

        # standardize data
        logger.info("Starting data standardization...")
        standardize_policies()
        claims_standardization()
        standardize_db_claims()
        logger.info("Data standardization completed.")

        # validate data
        logger.info("Starting data validation...")
        validate_claims()
        validate_policies()
        db_claims_validation()
        logger.info("Data validation completed.")

        # transform data
        logger.info("Starting data transformation...")
        join_policy_claims()
        logger.info("Data transformation completed.")

        # load to warehouse
        logger.info("Starting data loading to warehouse...")
        load_to_warehouse()
        logger.info("Data loading to warehouse completed.")

        # warehouse checks
        logger.info("Starting warehouse quality checks...")
        run_warehouse_checks()
        logger.info("Warehouse quality checks completed.")

        logger.info("Data pipeline execution completed successfully.")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()