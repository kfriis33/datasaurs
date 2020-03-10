import pandas as pd

with open ("data/PVD_raw_recycling_rates.csv", 'rb') as f:
    pvd_df = pd.read_csv(f)
with open ("data/NYC_raw_recycling_rates.csv", 'rb') as f:
    nyc_df = pd.read_csv(f)
with open ("data/Buffalo_raw_recycling_rates.csv", 'rb') as f:
    buff_df = pd.read_csv(f)
with open ("data/Seattle_raw_recycling_rates.csv", 'rb') as f:
    sea_df = pd.read_csv(f)

print("Finished reading data!")

# PVD data cleaning
pvd_df = pvd_df[['Year/Month', 'Waste diversion rate']]
pvd_df['Year/Month'] = pd.to_datetime(pvd_df['Year/Month'])
pvd_df.sort_values('Year/Month', ascending = True, inplace=True)
pvd_df['year'] = pvd_df['Year/Month'].map(lambda x: x.year)
pvd_df['month'] = pvd_df['Year/Month'].map(lambda x: x.month)
pvd_df.drop(columns = ['Year/Month'], inplace = True)
pvd_df.rename(columns={'Waste diversion rate': 'diversion_rate'}, inplace = True)
pvd_df['diversion_rate'] = pvd_df['diversion_rate'].map(lambda x: x * 100)
pvd_df['city'] = "Providence"
pvd_df = pvd_df[['city','year', 'month', 'diversion_rate']]

#print(pvd_df.head())

# NYC data cleaning
nyc_df.rename(columns={'Diversion Rate-Total (Total Recycling / Total Waste)': 'diversion_rate', \
    'Fiscal Month Number': 'month', 'Fiscal Year': 'year'}, inplace=True)
nyc_df = nyc_df[['year', 'month', 'diversion_rate']]
nyc_df.sort_values(['year', 'month'], ascending = (True, True), inplace=True)
nyc_df = nyc_df.groupby(['year','month']).mean()
nyc_df.reset_index(inplace=True)
nyc_df['city'] = 'New York City'
nyc_df = nyc_df[['city','year', 'month', 'diversion_rate']]

#print(nyc_df.head())

# Buffalo data cleaning
recycling = ['Curb Recycling', 'Misc. Recycling', 'Bottle Bill', 'Scrap Metal', 'Recycled Tires']
waste = ['Yard Waste', 'Asphalt Debris', 'Sidewalk Debris', 'Haz Waste', 'E-Waste', 'Curb Garbage', 'Misc. Garbage']

buff_df['DATE'] = pd.to_datetime(buff_df['DATE'])
buff_df['year'] = buff_df['DATE'].map(lambda x: x.year)
buff_df['month'] = buff_df['DATE'].map(lambda x: x.month)
buff_df.drop(columns = ['DATE', 'MONTH'], inplace = True)

buff_grouped = buff_df.loc[buff_df['TYPE'].isin(recycling)].groupby(['year', 'month'])['TOTAL (IN TONS)'] \
    .sum().reset_index().rename(columns={'TOTAL (IN TONS)': 'total_rec'})
buff_grouped['total_garb'] = buff_df.loc[buff_df['TYPE'].isin(waste)].groupby(['year', 'month'])['TOTAL (IN TONS)'] \
    .sum().reset_index()['TOTAL (IN TONS)']
buff_df = buff_grouped
buff_df['diversion_rate'] = buff_df['total_rec']/(buff_df['total_rec'] + buff_df['total_garb']) * 100
buff_df['city'] = 'Buffalo'
buff_df = buff_df[['city','year', 'month', 'diversion_rate']]

#print(buff_df.head())

# Seattle data cleaning
print(sea_df.head())
# sea_df[['total_garb', 'total_org', 'total_rec']] = sea_df[['total_garb', 'total_org', 'total_rec']] \
#     .apply(convert_objects, convert_numeric=True)
sea_df['total_garb'] = sea_df['total_garb'].astype(str).map(lambda x: float(x.replace(',', '')))
sea_df['total_org'] = sea_df['total_org'].astype(str).map(lambda x: float(x.replace(',', '')))
sea_df['total_rec'] = sea_df['total_rec'].astype(str).map(lambda x: float(x.replace(',', '')))

print(sea_df.head())
print(sea_df.dtypes)

# print(sea_df.head())
# print(sea_df.tail())

#print("Finished cleaning data!")
