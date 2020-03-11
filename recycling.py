import pandas as pd
import matplotlib.pyplot as plt

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

pvd_df['date'] = pvd_df['month'].map(str) + '/' + pvd_df['year'].map(str)
pvd_df['date'] = pd.to_datetime(pvd_df['date'], format='%m/%Y').dt.strftime('%m/%Y')

plt.plot(pvd_df['date'], pvd_df['diversion_rate'])
plt.title('Providence Diversion Rate')
plt.savefig('figs/pvd_graph')
plt.clf()

# NYC data cleaning
nyc_df.rename(columns={'Diversion Rate-Total (Total Recycling / Total Waste)': 'diversion_rate', \
    'Month Name': 'month', 'Fiscal Year': 'year'}, inplace=True)

months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
nyc_df.month = nyc_df.month.map(months)
nyc_df = nyc_df[['year', 'month', 'diversion_rate']]
nyc_df.sort_values(['year', 'month'], ascending = (True, True), inplace=True)
nyc_df = nyc_df.groupby(['year','month']).mean()
nyc_df.reset_index(inplace=True)
nyc_df['city'] = 'New York City'
nyc_df = nyc_df[['city','year', 'month', 'diversion_rate']]

nyc_df['date'] = nyc_df['month'].map(str) + '/' + nyc_df['year'].map(str)
nyc_df['date'] = pd.to_datetime(nyc_df['date'], format='%m/%Y').dt.strftime('%m/%Y')

plt.plot(nyc_df['date'], nyc_df['diversion_rate'])
plt.title('NYC Diversion Rate')
plt.savefig('figs/nyc_graph')
plt.clf()

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

buff_df['date'] = buff_df['month'].map(str) + '/' + buff_df['year'].map(str)
buff_df['date'] = pd.to_datetime(buff_df['date'], format='%m/%Y').dt.strftime('%m/%Y')

plt.plot(buff_df['date'], buff_df['diversion_rate'])
plt.title('Buffalo Diversion Rate')
plt.savefig('figs/buff_graph')
plt.clf()

# Seattle data cleaning
sea_df['total_garb'] = sea_df['total_garb'].astype(str).map(lambda x: float(x.replace(',', '')))
sea_df['total_org'] = sea_df['total_org'].astype(str).map(lambda x: float(x.replace(',', '')))
sea_df['total_rec'] = sea_df['total_rec'].astype(str).map(lambda x: float(x.replace(',', '')))
sea_df['diversion_rate'] = sea_df['total_rec'] /(sea_df['total_rec'] + sea_df['total_org'] + sea_df['total_garb']) * 100
sea_df['city'] = 'Seattle'
sea_df = sea_df[['city', 'year', 'month', 'diversion_rate']]

sea_df['date'] = sea_df['month'].map(str) + '/' + sea_df['year'].map(str)
sea_df['date'] = pd.to_datetime(sea_df['date'], format='%m/%Y').dt.strftime('%m/%Y')

plt.plot(sea_df['date'], sea_df['diversion_rate'])
plt.title('Seattle Diversion Rate')
plt.savefig('figs/sea_graph')
plt.clf()

final_df = pd.concat([pvd_df, nyc_df, buff_df, sea_df])
plot = final_df.groupby(['year', 'month'])['diversion_rate'].mean().reset_index()

plot['date'] = plot['month'].map(str) + '/' + plot['year'].map(str)
plot['date'] = pd.to_datetime(plot['date'], format='%m/%Y').dt.strftime('%m/%Y')

plt.plot(plot['date'], plot['diversion_rate'])
plt.title('Total Diversion Rate')
plt.savefig('figs/total_graph')
plt.clf()

print("Finished cleaning data!")

final_df.to_pickle('data/cleaned_final_data')
final_df.drop(columns=['date']).to_csv('data/cleaned_final_data.csv')
