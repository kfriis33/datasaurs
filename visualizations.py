import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statsmodels.tools import eval_measures
from statsmodels.stats.outliers_influence import variance_inflation_factor


#plot diversion rate/month aggregate
def plot_agg_divrate():
    with open ("data/all_aggregated.csv", "rb") as f:
        data_agg = pd.read_csv(f)



    strmonth = data_agg['month'].map(lambda y: str(y))
    data_agg['year/month'] = data_agg['year'].apply(lambda x: str(x)+'/')
    data_agg['year/month'] = data_agg['year/month'] + strmonth

    plt.plot(data_agg['year/month'], data_agg['diversion_rate'], color='#5c3c92')
    plt.xticks(np.arange(0, len(data_agg['month']), 12))
    plt.ylabel('Diversion Rate')
    plt.xlabel('Year/Month')
    plt.title('Diversion Rate Over Time (Aggregated)')
    plt.show()
plot_agg_divrate()

#If you want to plot diversion rate/month specific to city data, use this function. Just input city name
def plot_place(city):


    new = data_place.loc[data_place['place'] == city]
    strmonth = new['month'].map(lambda y: str(y))
    new['year/month'] = new['year'].apply(lambda x: str(x)+'/')
    new['year/month'] = new['year/month'] + strmonth

    plt.plot(new['year/month'], new['diversion_rate'])
    plt.xticks(np.arange(0, len(new['month']), 12))
    plt.ylabel('Diversion Rate', fontsize=7)
    plt.xlabel('Year/Month',fontsize=7)
    plt.title('Diversion Rate Over Time (' + city + ')', fontsize=10)

with open ("data/all_by_place.csv", "rb") as f:
    data_place = pd.read_csv(f)






#plt.show()






#Plots num_tweets vs. diversion, engagement normalized. Multiple linear regression done on both holiday data, and nonholiday data
#Input: city name if you want city-specific data, 'agg' if you want aggregate data
def plot_num_tweets(city):

    if city == 'agg':
        aggreg = {'diversion_rate':'mean', 'num_tweets':'sum', 'likes':'sum', 'retweets':'sum'}
        data = data_place.groupby(['year', 'month']).agg(aggreg).reset_index()
    else:
        data = data_place.loc[data_place['place'] == city]

    data['engagement'] = data['likes'] + data['retweets']
    data['holidays'] = [x == 11 or x == 12 or x == 1 for x in data['month']]

    data_Holiday = data.loc[data['holidays'] == True]
    data_nonHoliday = data.loc[data['holidays'] == False]


    dat = sm.add_constant(data_Holiday)
    eq = "diversion_rate ~ num_tweets + engagement"
    model = smf.ols(formula=eq, data=dat)
    results = model.fit()

    #X = data[['num_tweets', 'likes', 'retweets','const']]

    firstparams = results.params

    dat = sm.add_constant(data_nonHoliday)
    eq = "diversion_rate ~ num_tweets + engagement"
    model = smf.ols(formula=eq, data=dat)
    results = model.fit()



    x1 = data_Holiday['num_tweets']
    x2 = data_nonHoliday['num_tweets']
    y1 = firstparams[1]*x1 + firstparams[2] *np.mean(data_Holiday['engagement']) + firstparams[0]
    y2 = results.params[1]*x2 + results.params[2] * np.mean(data_nonHoliday['engagement']) + results.params[0]
    plt.plot(x1, y1, label='Holiday Months', color = '#5c3c92')
    plt.plot(x2, y2, label='Non-Holiday Months', color = '#79cbb8')
    plt.legend(loc='upper right')
    plt.scatter(data_Holiday['num_tweets'], data_Holiday['diversion_rate'], color='#5c3c92')
    plt.scatter(data_nonHoliday['num_tweets'], data_nonHoliday['diversion_rate'], color='#79cbb8')
    plt.xlabel('Number of Tweets')
    plt.ylabel('Diversion Rate')
    plt.title('Number of Tweets vs. Diversion Rate, Separated by Holiday/non-Holiday Months')
    plt.show()


#Plots engagement vs. diversion, num_tweets normalized. Multiple linear regression done on both holiday data, and nonholiday data
#Input: city name if you want city-specific data, 'agg' if you want aggregate data



#plot_num_tweets('agg')
