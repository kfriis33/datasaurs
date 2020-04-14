import csv
import pandas as pd

# code for combining csvs
'''
import os
import glob

os.chdir("./csvs")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
'''

months = {"Dec": 12, "Nov": 11, "Oct": 10, "Sep": 9, "Aug": 8, "Jul": 7, "Jun": 6, "May": 5, "Apr": 4, "Mar": 3, "Feb": 2, "Jan": 1}

'''
with open('./csvs/combined_csv.csv') as old_file, open('interim_processed_by_place.csv', mode='w') as new_file:
    #fieldnames = ['year', 'place', 'month', 'num_tweets', 'likes', 'retweets']
    fieldnames = ['year', 'place', 'month', 'num_tweets', 'likes', 'retweets']
    csv_reader = csv.reader(old_file, delimiter=',')
    csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    line_count = 0
    for row in csv_reader:
        #print(len(row))
        #print(row)
        if line_count == 0:  #or len(row) != 5:
            line_count += 1
            print("line_count == 0 or len(row) != 5")
            continue

        month = row[2].split(' ')[1]
        csv_writer.writerow({'year': int(row[0]), 'place': row[1], 'month': months[month], 'num_tweets': 1, 'likes': int(row[3]), 'retweets': int(row[4])})
'''

''' sum rows '''
'''
df = pd.read_csv("interim_processed_by_place.csv")
by_place = df.groupby(['year','place','month']).sum()
aggregated = df.groupby(['year','month']).sum()

by_place.to_csv( "processed_by_place.csv", encoding='utf-8-sig')
aggregated.to_csv( "processed_aggregated.csv", encoding='utf-8-sig')
'''


''' by place --> aggregate '''
df = pd.read_csv("data/recycling_by_place.csv")
aggregated = df.groupby(['year','month']).sum()
aggregated.to_csv( "full_processed_aggregated.csv", encoding='utf-8-sig')
