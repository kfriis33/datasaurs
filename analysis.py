import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from scipy.stats import describe, spearmanr, pearsonr


with open ("data/recycling_by_place.csv", 'rb') as f:
    r_df = pd.read_csv(f)

# get rid of NYC data
r_df.drop(r_df[r_df['city'] == 'New York City'].index, inplace=True)
r_df = r_df.loc[:, ~r_df.columns.str.contains('^Unnamed')]
r_df.rename(columns={'city':'place'}, inplace=True)

r_agg = r_df.groupby(['year', 'month'])['diversion_rate'].mean().reset_index()
#r_agg.to_csv('data/recycling_aggregated.csv')

with open ("data/tweets_aggregated_w_normalization.csv", 'rb') as f:
    t_agg = pd.read_csv(f)
with open ("data/tweets_by_place.csv", 'rb') as f:
    t_df = pd.read_csv(f)

joined = pd.merge(r_agg, t_agg, on=['year', 'month'])
#joined.to_csv('data/all_aggregated.csv')

joined_place = pd.merge(r_df, t_df, on=['year', 'month', 'place'])
#joined_place.to_csv('data/all_by_place.csv')

plt.scatter(joined['num_tweets'], joined['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined['num_tweets'], joined['diversion_rate'], 1)
plt.plot(joined['num_tweets'], m*joined['num_tweets'] + b)
plt.xlabel('Number of Tweets')
plt.ylabel('Recycling Diversion Rate')
plt.savefig('figs/analysis/tweets_vs_diversion')
plt.show()
plt.clf()

# get rid of outliers
joined_adj = joined[joined['likes'].between(0, joined.quantile(.95).likes)]
joined_adj = joined_adj[joined_adj['retweets'].between(0, joined.quantile(.95).retweets)]


plt.scatter(joined_adj['likes'], joined_adj['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined_adj['likes'], joined_adj['diversion_rate'], 1)
plt.plot(joined_adj['likes'], m*joined_adj['likes'] + b)
plt.xlabel('Likes')
plt.ylabel('Recycling Diversion Rate')
plt.savefig('figs/analysis/likes_vs_diversion')
plt.show()
plt.clf()

plt.scatter(joined_adj['retweets'], joined_adj['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined_adj['retweets'], joined_adj['diversion_rate'], 1)
plt.plot(joined_adj['retweets'], m*joined_adj['retweets'] + b)
plt.xlabel('retweets')
plt.ylabel('Recycling Diversion Rate')
plt.savefig('figs/analysis/retweets_vs_diversion')
plt.show()
plt.clf()
