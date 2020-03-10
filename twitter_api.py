
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


with open('2019-2021-tweets.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["year", "place", "month", "num_tweets", "likes", "retweets"])

    for year in range(2019, 2021):
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
