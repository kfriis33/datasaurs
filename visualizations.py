import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statsmodels.tools import eval_measures
from statsmodels.stats.outliers_influence import variance_inflation_factor


with open ("data/all_aggregated.csv", "rb") as f:
    data_agg = pd.read_csv(f)



strmonth = data_agg['month'].map(lambda y: str(y))
data_agg['year/month'] = data_agg['year'].apply(lambda x: str(x)+'/')
data_agg['year/month'] = data_agg['year/month'] + strmonth

plt.subplot(2,2,1)
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)
plt.plot(data_agg['year/month'], data_agg['diversion_rate'])
plt.xticks(np.arange(0, len(data_agg['month']), 12))
plt.ylabel('Diversion Rate', fontsize=7)
plt.xlabel('Year/Month', fontsize=7)
plt.title('Diversion Rate Over Time (Aggregated)', fontsize=10)

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

plt.subplot(2,2,2)
plot_place('Providence')
plt.subplot(2,2,3)
plot_place('Seattle')
plt.subplot(2,2,4)
plot_place('Buffalo')




plt.show()





#
# # function to print pearson coefficients for dataframe
# def printCoeff(d):
#     pearson, p = pearsonr(d['num_tweets'], d['diversion_rate'])
#     print("Pearson (num_tweets): %.02f (%.02f)"%(pearson, p))
#     pearson, p = pearsonr(d['likes'], d['diversion_rate'])
#     print("Pearson (likes): %.02f (%.02f)"%(pearson, p))
#     pearson, p = pearsonr(d['retweets'], d['diversion_rate'])
#     print("Pearson (retweets): %.02f (%.02f)"%(pearson, p))
#     pearson, p = pearsonr(d['engagement'], d['diversion_rate'])
#     print("Pearson (engagement): %.02f (%.02f)"%(pearson, p))
#
# # analysis for aggregated
# aggreg = {'diversion_rate':'mean', 'num_tweets':'sum', 'likes':'sum', 'retweets':'sum'}
# data = data_place.groupby(['year', 'month']).agg(aggreg).reset_index()
# data['engagement'] = data['likes'] + data['retweets']
# data['holidays'] = [x == 11 or x == 12 or x == 1 for x in data['month']]
#
# num_tweets_std = np.std(data['num_tweets'])
# num_tweets_mean = np.mean(data['num_tweets'])
#
# data['num_tweets_normalized']
#
# print(data)
#
# print("Analysis for aggregated:")
# printCoeff(data)
#
# data = sm.add_constant(data)
# eq = "diversion_rate ~ num_tweets + engagement + C(holidays)"
# model = smf.ols(formula=eq, data=data)
# results = model.fit()
# print(results.summary())
# print ("MSE:", eval_measures.mse(data['diversion_rate'], results.predict()))
#
# X = data[['num_tweets', 'likes', 'retweets','const']]
# print("VIF (large numbers show collinearity):")
# print(pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns))
