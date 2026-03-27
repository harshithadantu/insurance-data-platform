import pandas as pd
import numpy as np

rows=10000

data={'Policy_Id':np.random.randint(1000,2000,rows),
      'customer_id':np.random.randint(5000,6000,rows),
      'claim_amount':np.random.uniform(100,5000,rows),
      'status':np.random.choice(['Approved','Rejected','Pending'],rows)
      }

df=pd.DataFrame(data)

df.to_json("data/raw/claims.json",orient='records')
