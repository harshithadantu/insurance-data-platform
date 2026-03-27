import pandas as pd
import numpy as np

rows = 1000

data = {
    "policy_id": np.arange(1000, 1000 + rows),
    "customer_id": np.random.randint(5000, 8000, rows),
    "policy_type": np.random.choice(["auto", "health", "life", "home"], rows),
    "premium_amount": np.random.uniform(300, 2000, rows),
    "policy_start_date": pd.date_range(start="2023-01-01", periods=rows, freq="D"),
    "status": np.random.choice(["active", "expired", "cancelled"], rows)
}

df = pd.DataFrame(data)

df.to_csv("data/source/policies.csv", index=False)

print("policies.csv created")