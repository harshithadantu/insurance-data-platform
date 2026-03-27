import pandas as pd

#load JSON file
df=pd.read_json("data/raw/claims.json")

# show columns
print("Columns in dataset:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nData Info:")
print(df.info())

print("\nDistinct values in each column:")
for col in df.columns:
    print(f"\nColumn: {col}")
    print(df[col].unique())