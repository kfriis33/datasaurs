import csv

with open('tweet_sample.csv') as file:
    csv_reader = csv.reader(file, delimiter=',')
    pos = 0
    neut = 0
    neg = 0
    total = 0
    for row in csv_reader:
        total +=1
        if row[4] == str(1):
            pos +=1
        elif row[4] == str(0):
            neut +=1
        elif row[4] == str(-1):
            neg +=1
        else:
            total -=1
            print("wtf", row[4])
print("total:", total)
print("pos:", pos, "perc:", pos/total)
print("neut:", neut, "perc:", neut/total)
print("neg:", neg, "perc:", neg/total)
