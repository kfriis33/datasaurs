import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
#from scipy.stats import describe, spearmanr, pearsonr

with open ("data/recycling_by_place.csv", 'rb') as f:
    r_df = pd.read_csv(f)

# get rid of NYC data
r_df.drop(r_df[r_df['city'] == 'New York City'].index, inplace=True)
r_df = r_df.loc[:, ~r_df.columns.str.contains('^Unnamed')]
r_df.rename(columns={'city':'place'}, inplace=True)


r_agg = r_df.groupby(['year', 'month'])['diversion_rate'].mean().reset_index()

print(r_df)
print(r_agg)

cities = np.unique(r_df['place'])
colors = [plt.cm.tab10(i/float(len(cities)-1)) for i in range(len(cities))]



#r_agg.to_csv('data/recycling_aggregated.csv')

with open ("data/tweets_aggregated_w_normalization.csv", 'rb') as f:
    t_agg = pd.read_csv(f)
with open ("data/tweets_by_place.csv", 'rb') as f:
    t_df = pd.read_csv(f)

joined = pd.merge(r_agg, t_agg, on=['year', 'month'])
#joined.to_csv('data/all_aggregated.csv')

joined_place = pd.merge(r_df, t_df, on=['year', 'month', 'place'])
#joined_place.to_csv('data/all_by_place.csv')

#plot 1

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


#get rid of outliers for unaggregated data
joined_place_adj = joined_place[joined_place['likes'].between(0, joined_place.quantile(.95).likes)]
joined_place_adj = joined_place_adj[joined_place_adj['retweets'].between(0, joined_place.quantile(.95).retweets)]


#plot2

plt.figure(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')

for i, city in enumerate(cities):
    plt.scatter('num_tweets', 'diversion_rate',
                data=joined_place.loc[joined_place.place==city, :],
                s=20, c=colors[i], label=str(city))

plt.gca().set(xlabel='Number of Tweets', ylabel='Diversion Rate')
plt.xticks(fontsize=12); plt.yticks(fontsize=12)
plt.title("Scatterplot of Number of Tweets vs Diversion Rate, colorcoded by city", fontsize=22)
plt.legend(fontsize=12)
plt.savefig('figs/analysis/tweets_vs_diversion_color')
plt.show()
plt.clf()


#plot3

plt.scatter(joined_adj['likes'], joined_adj['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined_adj['likes'], joined_adj['diversion_rate'], 1)
plt.plot(joined_adj['likes'], m*joined_adj['likes'] + b)
plt.xlabel('Likes')
plt.ylabel('Recycling Diversion Rate')
plt.savefig('figs/analysis/likes_vs_diversion')
plt.show()
plt.clf()


#plot 4

plt.figure(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')

for i, city in enumerate(cities):
    plt.scatter('likes', 'diversion_rate',
                data=joined_place_adj.loc[joined_place_adj.place==city, :],
                s=20, c=colors[i], label=str(city))

plt.gca().set(xlabel='Number of Likes', ylabel='Diversion Rate')
plt.xticks(fontsize=12); plt.yticks(fontsize=12)
plt.title("Scatterplot of Number of Likes vs Diversion Rate, colorcoded by city", fontsize=22)
plt.legend(fontsize=12)
plt.savefig('figs/analysis/likes_vs_diversion_color')
plt.show()
plt.clf()


#plot 5
plt.scatter(joined_adj['retweets'], joined_adj['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined_adj['retweets'], joined_adj['diversion_rate'], 1)
plt.plot(joined_adj['retweets'], m*joined_adj['retweets'] + b)
plt.xlabel('retweets')
plt.ylabel('Recycling Diversion Rate')
plt.savefig('figs/analysis/retweets_vs_diversion')
plt.show()
plt.clf()


#plot 6
plt.figure(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')

for i, city in enumerate(cities):
    plt.scatter('retweets', 'diversion_rate',
                data=joined_place_adj.loc[joined_place_adj.place==city, :],
                s=20, c=colors[i], label=str(city))

plt.gca().set(xlabel='Number of Retweets', ylabel='Diversion Rate')
plt.xticks(fontsize=12); plt.yticks(fontsize=12)
plt.title("Scatterplot of Number of Retweets vs Diversion Rate, colorcoded by city", fontsize=22)
plt.legend(fontsize=12)
plt.savefig('figs/analysis/retweets_vs_diversion_color')
plt.show()
plt.clf()


#plot7

ax = plt.axes(projection='3d')
ax.scatter3D(joined_adj['retweets'], joined_adj['likes'], joined_adj['diversion_rate'])
ax.set_xlabel('retweets')
ax.set_ylabel('likes')
ax.set_zlabel('Recycling Diviersion Rate')
plt.savefig('figs/analysis/retweets+likes_vs_diversion')
plt.show()
