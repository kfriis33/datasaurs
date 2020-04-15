import numpy as np
import pandas as pd
import GetOldTweets3 as got

# tweetCriteria = got.manager.TweetCriteria().setQuerySearch('trump')\
#                                            .setSince("2016-6-01")\
#                                            .setUntil("2016-7-01")\
#                                            .setNear('New York City')\
#                                            # .setWithin('1mi')

cities = ['Providence', 'Seattle', 'New York City', 'Buffalo'] #add all cities
query = 'climate'

# tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# print('there were', len(tweets), 'tweets in this period')
# for tweet in tweets[:10]:
#     print(tweet.permalink)
#     print(tweet.text)
#     print('retweets:', tweet.retweets)
#     print()


#create pandas dataframe
dict = {'city':[], 'month':[], 'tweets':[], 'likes':[], 'retweets':[]}
column_names = ['city', 'month', 'tweets', 'likes', 'retweets']
# dict['city'].append('octon')
# dict['month'].append('2008-05')
# dict['tweets'].append(15)
# dict['likes'].append(15)
# dict['retweets'].append(20)
months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# df = pd.DataFrame(dict, columns=column_names)
# print(df)
# df.to_csv('tweet_stats.csv')
# exit()
for city in cities:
    print('scraping tweets from', city)
    for year in range(2008, 2021):
        print('\tscraping tweets from', year)
        for month in range(1, 13):
            since = str(year) + '-' + str(month) + '-01'
            until = str(year) + '-' + str(month + 1) + '-01'
            if month == 12:
                until = str(year + 1) + '-01-01'

            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query)\
                                                       .setSince(since)\
                                                       .setUntil(until)\
                                                       .setNear(city)
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)

            num_tweets = len(tweets)
            print('\t\tscraping', num_tweets, 'tweets from', months[month])

            num_likes = 0
            num_retweets = 0
            for tweet in tweets:
                num_likes += tweet.favorites
                num_retweets += tweet.retweets
            dict['city'].append(city)
            dict['month'].append(since[:-3])
            dict['tweets'].append(num_tweets)
            dict['likes'].append(num_likes)
            dict['retweets'].append(num_retweets)

            #add to df
            # df.append([[city, since[:-3], num_tweets, num_likes, num_retweets]])

df = pd.DataFrame(dict, columns=column_names)
print(df)
df.to_csv('tweet_stats.csv', index=False)
#save df to file
