import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.logger import get_logger
logger = get_logger()


def join_policy_claims():
    # load data
    df_policy = pd.read_parquet("data/processed/policies_clean.parquet")
    df_claims = pd.read_parquet("data/processed/claims_clean.parquet")
    logger.info("Policy and claims data loaded successfully")

    # aggregate claims
    claims_agg = df_claims.groupby(["policy_id", "customer_id"], as_index=False).agg(
        total_claims_amount=("claim_amount", "sum"),
        claim_count=("claim_amount", "count")
    )

    # join policy and claims
    merged = pd.merge(df_policy, claims_agg, on=["policy_id", "customer_id"], how="left")

    # fill missing values
    merged["total_claims_amount"] = merged["total_claims_amount"].fillna(0.0)
    merged["claim_count"] = merged["claim_count"].fillna(0).astype(int)

    # calculate loss ratio
    merged["loss_ratio"] = merged.apply(
        lambda row: row["total_claims_amount"] / row["premium_amount"] if row["premium_amount"] > 0 else 0,
        axis=1
    )

    # logging counts
    logger.info(
        f"policy count:{df_policy.shape[0]}, claims count:{df_claims.shape[0]}, merged count:{merged.shape[0]}"
    )

    logger.info("Policy and claims data joined successfully")

    # remove duplicates before saving
    merged = merged.drop_duplicates(subset=["policy_id","customer_id"])

    # save curated data
    os.makedirs("data/curated", exist_ok=True)
    merged.to_parquet("data/curated/policy_claims_summary.parquet", engine="pyarrow", index=False)
    logger.info("Merged data saved successfully")


if __name__ == "__main__":
    join_policy_claims()