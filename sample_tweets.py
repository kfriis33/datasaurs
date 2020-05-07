import random
import csv
from searchtweets import ResultStream, gen_rule_payload, load_credentials
from searchtweets import collect_results

places = ["Providence", "Buffalo", "Seattle"]

#"01":31, "02":28, "03":31,
months = {"01":31, "02":28, "03":31} #"04":30, "05":31, "06":30, "07":31, "08":31, "09":30, "10":31, "11":30, "12":31}

premium_search_args = load_credentials("twitter_keys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)

q = []
with open('2013_1_tweet_sample.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["place", "date_created", "text", "hashtags"])


    #for year in range(2019, 2012, -1):
    year = "2013"

    for month, days in months.items():
        day = random.sample([i for i in range(1, days)], 1)[0]
        next_day = str(day+1)
        day = str(day)
        if (len(day) ==1):
            day = "0"+day
            #q.append()
                #print(day)
        print(day)

        rule_q ="climate (place:Seattle OR place:Buffalo OR place:Providence)" #"climate place:"+place #" OR place:Buffalo OR place:Seattle)"#" AND since:2019-01-07 until:2019-01-08"  #point_radius:[41.8240 71.4128 10.0mi])"
        rule = gen_rule_payload(rule_q, results_per_call=100, from_date=year+"-"+month+"-"+day, to_date=year+"-"+month+"-"+next_day) # testing with a sandbox account
        tweets = collect_results(rule,
                                max_results=500,
                                result_stream_args=premium_search_args)

        for t in tweets:
            print(t)
            if t['place'] is None:
                place = t['location']
            else:
                place = t['place']['name']
            if (t['truncated'] == True):
                writer.writerow([place, t["created_at"], t['extended_tweet']["full_text"], t["entities"]["hashtags"]])
            else:
                writer.writerow([place, t["created_at"], t['text'], t["entities"]["hashtags"]])

    #print(len(tweets))
