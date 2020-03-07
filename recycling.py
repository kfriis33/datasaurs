import pandas as pd

with open ("data/PVD_raw_recycling_rates.csv", 'rb') as f:
    df = pd.read_csv(f)
print("Finished reading data!")

print(df.head())
