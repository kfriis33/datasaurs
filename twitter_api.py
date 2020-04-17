
from searchtweets import ResultStream, gen_rule_payload, load_credentials
from searchtweets import collect_results
import csv

premium_search_args = load_credentials("twitter_keys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

places = ["Providence", "Seattle", "Buffalo"]

months = [("-01-01","-01-31"), ("-02-01","-02-28"), ("-03-01","-03-31"),
("-04-01","-04-30"), ("-05-01","-05-31"), ("-06-01","-06-30"), ("-07-01","-07-31"),
("-08-01","-08-31"), ("-09-01","-09-30"), ("-10-01","-10-31"), ("-11-01","-11-30"),
("-12-01","-12-31")]

'''
rule_q = """
(climate change)
place:"Manhattan"
"""
rule = gen_rule_payload(rule_q, results_per_call=100,
from_date="2018-01-01", to_date="2018-01-31") # testing with a sandbox account


tweets = collect_results(rule,
                         max_results=500,
                         result_stream_args=premium_search_args)

print([
    len(tweets), sum([tweet.favorite_count for tweet in tweets]),
    sum([tweet.retweet_count for tweet in tweets])])
print(len(tweets))



'''
'''
with open('full-data-tweets.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["year", "place", "month", "num_tweets", "likes", "retweets"])

    for year in range(2019, 2009, -1):
        for place in places:
            month_counter = 1
            for start, end in months:
                rule_q = "climate place:" + place  #point_radius:[41.8240 71.4128 10.0mi])"
                rule = gen_rule_payload(rule_q, results_per_call=100,
                from_date=str(year)+start, to_date=str(year)+end) # testing with a sandbox account


                tweets = collect_results(rule,
                                         max_results=500,
                                         result_stream_args=premium_search_args)

                writer.writerow([year, place, month_counter,
                    len(tweets), sum([tweet.favorite_count for tweet in tweets]),
                    sum([tweet.retweet_count for tweet in tweets])])
                print(len(tweets))
                month_counter+=1
'''

with open('2013-seattle-all.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["year", "place", "date_created", "num_tweets", "num_likes", "num_retweets"])

    # for year in range(2018, 2009, -1):
    #     for place in places:

    year = "2013"
    place= "Seattle"

    rule_q = "climate place:"+place  #point_radius:[41.8240 71.4128 10.0mi])"
    rule = gen_rule_payload(rule_q, results_per_call=100,
    from_date=year+"-01-01", to_date=year+"-12-31") # testing with a sandbox account

    tweets = collect_results(rule,
                             max_results=500,
                             result_stream_args=premium_search_args)
    month_counter = 1
    for t in tweets:
        print(t)
        writer.writerow([year, place, t["created_at"], t.favorite_count, t.retweet_count])
    print(len(tweets))
