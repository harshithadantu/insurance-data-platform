import os
import pandas as pd
from utils.logger import get_logger

logger = get_logger()


def detect_cdc(
    current_file="data/curated/policy_claims_summary.parquet",
    previous_file="data/snapshots/policy_claims_summary_previous.parquet"
):
    try:
        key_columns = ["policy_id", "customer_id"]

        current_df = pd.read_parquet(current_file)
        logger.info(f"Current curated data loaded. Rows: {len(current_df)}")

        # First run: no previous snapshot
        if not os.path.exists(previous_file):
            current_df["cdc_flag"] = "INSERT"
            logger.info("No previous snapshot found. All rows marked as INSERT.")
            return current_df

        previous_df = pd.read_parquet(previous_file)
        logger.info(f"Previous snapshot loaded. Rows: {len(previous_df)}")

        # Fill null values to avoid comparison issues
        current_df = current_df.fillna("")
        previous_df = previous_df.fillna("")

        # Merge current and previous
        merged_df = current_df.merge(
            previous_df,
            on=key_columns,
            how="outer",
            suffixes=("_new", "_old"),
            indicator=True
        )

        non_key_columns = [col for col in current_df.columns if col not in key_columns]
        cdc_rows = []

        for _, row in merged_df.iterrows():
            if row["_merge"] == "left_only":
                # new record
                record = {}
                for col in current_df.columns:
                    if col in key_columns:
                        record[col] = row[col]
                    else:
                        record[col] = row[f"{col}_new"]
                record["cdc_flag"] = "INSERT"
                cdc_rows.append(record)

            elif row["_merge"] == "right_only":
                # deleted record
                record = {}
                for col in previous_df.columns:
                    if col in key_columns:
                        record[col] = row[col]
                    else:
                        record[col] = row[f"{col}_old"]
                record["cdc_flag"] = "DELETE"
                cdc_rows.append(record)

            else:
                # check if updated
                changed = False
                for col in non_key_columns:
                    if row[f"{col}_new"] != row[f"{col}_old"]:
                        changed = True
                        break

                if changed:
                    record = {}
                    for col in current_df.columns:
                        if col in key_columns:
                            record[col] = row[col]
                        else:
                            record[col] = row[f"{col}_new"]
                    record["cdc_flag"] = "UPDATE"
                    cdc_rows.append(record)

        cdc_df = pd.DataFrame(cdc_rows)
        logger.info(f"CDC detection completed. Changed rows: {len(cdc_df)}")
        return cdc_df

    except Exception as e:
        logger.error(f"CDC detection failed: {e}")
        raise