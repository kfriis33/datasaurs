import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import seaborn as sns
from scipy.stats import describe, spearmanr, pearsonr

with open ("data/recycling_by_place.csv", 'rb') as f:
    r_df = pd.read_csv(f)

# get rid of NYC data
r_df.drop(r_df[r_df['city'] == 'New York City'].index, inplace=True)
r_df = r_df.loc[:, ~r_df.columns.str.contains('^Unnamed')]
r_df.rename(columns={'city':'place'}, inplace=True)


r_agg = r_df.groupby(['year', 'month'])['diversion_rate'].mean().reset_index()

cities = np.unique(r_df['place'])
#colors = [plt.cm.tab10(i/float(len(cities)-1)) for i in range(len(cities))]
colors = ['mediumpurple', 'royalblue', 'forestgreen']


#r_agg.to_csv('data/recycling_aggregated.csv')

with open ("data/tweets_aggregated_w_normalization.csv", 'rb') as f:
    t_agg = pd.read_csv(f)
with open ("data/tweets_by_place.csv", 'rb') as f:
    t_df = pd.read_csv(f)

joined = pd.merge(r_agg, t_agg, on=['year', 'month'])
#joined.to_csv('data/all_aggregated.csv')

joined_place = pd.merge(r_df, t_df, on=['year', 'month', 'place'])
#joined_place.to_csv('data/all_by_place.csv')

#calculate engagement
with open ("data/tweets_aggregated_w_normalization.csv", 'rb') as f:
    tnorm = pd.read_csv(f)

perc_impressions = 0.1
importance = 2

tnorm['avg_followers'] = tnorm['MAU']*(707/68) #68 is the MAU for Dec 2019
tnorm['avg_views'] = tnorm['avg_followers'] * perc_impressions
tnorm['total_views'] = (tnorm['num_tweets'] + tnorm['retweets'])/tnorm['perc_geotagged']*tnorm['avg_views']
tnorm['engagement'] = ((tnorm['likes'] + tnorm['retweets'])/tnorm['perc_geotagged'])*importance + tnorm['total_views']

joined_norm = pd.merge(r_agg, tnorm, on=['year','month'])
# joined_norm.to_csv('data/all_w_engagement.csv')

# remove high outliers
joined_norm_adj = joined_norm[joined_norm['engagement'].between(0, joined_norm.quantile(.95).engagement)]

# plot for engagement
plt.scatter(joined_norm_adj['engagement'], joined_norm_adj['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined_norm_adj['engagement'], joined_norm_adj['diversion_rate'], 1)
print ("Engagement -", "m:", m, "b:", b)
pearson, p = pearsonr(joined_norm_adj['engagement'], joined_norm_adj['diversion_rate'])
print("Pearson: %.02f (%.02f)"%(pearson, p))

plt.plot(joined_norm_adj['engagement'], m*joined_norm_adj['engagement'] + b)
plt.xlabel('Engagement')
plt.ylabel('Recycling Diversion Rate')
plt.title("Twitter engagement vs Diversion Rate")
plt.savefig('figs/analysis/engagement_vs_diversion')
plt.show()
plt.clf()


#plot 1

plt.scatter(joined['num_tweets'], joined['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined['num_tweets'], joined['diversion_rate'], 1)
print ("Tweets aggregate -", "m:", m, "b:", b)
plt.plot(joined['num_tweets'], m*joined['num_tweets'] + b)
pearson, p = pearsonr(joined['num_tweets'], joined['diversion_rate'])
print("Pearson: %.02f (%.02f)"%(pearson, p))

plt.xlabel('Number of Tweets')
plt.ylabel('Recycling Diversion Rate')
plt.title("Number of Tweets vs Diversion Rate")
plt.savefig('figs/analysis/tweets_vs_diversion')
#plt.show()
plt.clf()

# get rid of outliers
joined_adj = joined[joined['likes'].between(0, joined.quantile(.95).likes)]
joined_adj = joined_adj[joined_adj['retweets'].between(0, joined.quantile(.95).retweets)]
# joined_adj = joined_adj[joined_adj['diversion_rate'].between(joined.quantile(.05).diversion_rate, joined.quantile(.95).diversion_rate)]


#get rid of outliers for unaggregated data
joined_place_adj = joined_place[joined_place['likes'].between(0, joined_place.quantile(.95).likes)]
joined_place_adj = joined_place_adj[joined_place_adj['retweets'].between(0, joined_place.quantile(.95).retweets)]
# joined_place_adj = joined_place_adj[joined_place_adj['diversion_rate'].between(joined_place.quantile(.05).diversion_rate, joined_place.quantile(.95).diversion_rate)]


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
#plt.show()
plt.clf()

# break cities into separate plots
for i, city in enumerate(cities):
    data = joined_place.loc[joined_place.place==city, :]
    plt.scatter('num_tweets', 'diversion_rate',
                data= data, c=colors[i], alpha=0.7)
    m, b = np.polyfit(data['num_tweets'], data['diversion_rate'], 1)
    print ("Tweets", city, "-", "m:", m, "b:", b)
    plt.plot(data['num_tweets'], m*data['num_tweets'] + b, c=colors[i])
    pearson, p = pearsonr(data['num_tweets'], data['diversion_rate'])
    print("Pearson: %.02f (%.02f)"%(pearson, p))

    plt.gca().set(xlabel='Number of Tweets', ylabel='Diversion Rate')
    plt.title("Number of Tweets vs Diversion Rate, " + city)
    plt.savefig('figs/analysis/by_city/tweets_vs_diversion_' + str(i))
    #plt.show()
    plt.clf()


#plot3

plt.scatter(joined_adj['likes'], joined_adj['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined_adj['likes'], joined_adj['diversion_rate'], 1)
print ("Likes aggregate -", "m:", m, "b:", b)
plt.plot(joined_adj['likes'], m*joined_adj['likes'] + b)
pearson, p = pearsonr(joined_adj['likes'], joined_adj['diversion_rate'])
print("Pearson: %.02f (%.02f)"%(pearson, p))

plt.xlabel('Likes')
plt.ylabel('Recycling Diversion Rate')
plt.title("Number of Likes vs Diversion Rate")
plt.savefig('figs/analysis/likes_vs_diversion')
#plt.show()
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
#plt.show()
plt.clf()


# break cities into separate plots
for i, city in enumerate(cities):
    data = joined_place.loc[joined_place.place==city, :]
    # get rid of outliers by city
    data = data[data['likes'].between(0, data.quantile(.90).likes)]
    # data = data[data['diversion_rate'].between(0, data.quantile(.95).diversion_rate)]
    plt.scatter('likes', 'diversion_rate',
                data= data, c=colors[i], alpha=0.7)
    m, b = np.polyfit(data['likes'], data['diversion_rate'], 1)
    print ("Likes", city, "-", "m:", m, "b:", b)
    plt.plot(data['likes'], m*data['likes'] + b, c=colors[i])
    pearson, p = pearsonr(data['likes'], data['diversion_rate'])
    print("Pearson: %.02f (%.02f)"%(pearson, p))

    plt.gca().set(xlabel='Number of Likes', ylabel='Diversion Rate')
    plt.title("Number of Likes vs Diversion Rate, " + city)
    plt.savefig('figs/analysis/by_city/likes_vs_diversion_' + str(i))
    #plt.show()
    plt.clf()


#plot 5
plt.scatter(joined_adj['retweets'], joined_adj['diversion_rate'], alpha=0.7)
m, b = np.polyfit(joined_adj['retweets'], joined_adj['diversion_rate'], 1)
print ("Retweets aggregate -", "m:", m, "b:", b)
plt.plot(joined_adj['retweets'], m*joined_adj['retweets'] + b)
pearson, p = pearsonr(joined_adj['retweets'], joined_adj['diversion_rate'])
print("Pearson: %.02f (%.02f)"%(pearson, p))

plt.xlabel('retweets')
plt.ylabel('Recycling Diversion Rate')
plt.title("Number of Retweets vs Diversion Rate")
plt.savefig('figs/analysis/retweets_vs_diversion')
#plt.show()
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
#plt.show()
plt.clf()

# break cities into separate plots
for i, city in enumerate(cities):
    data = joined_place.loc[joined_place.place==city, :]
    # get rid of outliers by city
    data = data[data['retweets'].between(0, data.quantile(.90).retweets)]  # not sure if this is the right quantile to cut at
    # data = data[data['diversion_rate'].between(0, data.quantile(.95).diversion_rate)]
    plt.scatter('retweets', 'diversion_rate',
                data= data, c=colors[i], alpha=0.7)
    m, b = np.polyfit(data['retweets'], data['diversion_rate'], 1)
    print ("Retweets", city, "-", "m:", m, "b:", b)
    plt.plot(data['retweets'], m*data['retweets'] + b, c=colors[i])
    pearson, p = pearsonr(data['retweets'], data['diversion_rate'])
    print("Pearson: %.02f (%.02f)"%(pearson, p))

    plt.gca().set(xlabel='Number of Retweets', ylabel='Diversion Rate')
    plt.title("Number of Retweets vs Diversion Rate, " + city)
    plt.savefig('figs/analysis/by_city/retweets_vs_diversion_' + str(i))
    #plt.show()
    plt.clf()


# #plot7

joined_adj = joined[joined['likes'].between(0, joined.quantile(.95).likes)]
joined_adj = joined_adj[joined_adj['retweets'].between(0, joined.quantile(.80).retweets)]
# adjust outliers for better 3d graph

ax = plt.axes(projection='3d')
ax.scatter3D(joined_adj['retweets'], joined_adj['likes'], joined_adj['diversion_rate'])
ax.set_xlabel('retweets')
ax.set_ylabel('likes')
ax.set_zlabel('Recycling Diviersion Rate')
plt.savefig('figs/analysis/retweets+likes_vs_diversion')
#plt.show()
