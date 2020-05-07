import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statsmodels.tools import eval_measures
from statsmodels.stats.outliers_influence import variance_inflation_factor


## analysis for aggregated data
with open ("data/all_by_place.csv", "rb") as f:
    data_place = pd.read_csv(f)

# function to print pearson coefficients for dataframe
def printCoeff(d):
    pearson, p = pearsonr(d['num_tweets'], d['diversion_rate'])
    print("Pearson (num_tweets): %.02f (%.02f)"%(pearson, p))
    pearson, p = pearsonr(d['likes'], d['diversion_rate'])
    print("Pearson (likes): %.02f (%.02f)"%(pearson, p))
    pearson, p = pearsonr(d['retweets'], d['diversion_rate'])
    print("Pearson (retweets): %.02f (%.02f)"%(pearson, p))
    pearson, p = pearsonr(d['engagement'], d['diversion_rate'])
    print("Pearson (engagement): %.02f (%.02f)"%(pearson, p))

# analysis for aggregated
aggreg = {'diversion_rate':'mean', 'num_tweets':'sum', 'likes':'sum', 'retweets':'sum'}
data = data_place.groupby(['year', 'month']).agg(aggreg).reset_index()
data['engagement'] = data['likes'] + data['retweets']
data['holidays'] = [x == 11 or x == 12 or x == 1 for x in data['month']]

print("Analysis for aggregated:")
printCoeff(data)

data = sm.add_constant(data)
eq = "diversion_rate ~ num_tweets + engagement + C(holidays)"
model = smf.ols(formula=eq, data=data)
results = model.fit()
print(results.summary())
print ("MSE:", eval_measures.mse(data['diversion_rate'], results.predict()))

X = data[['num_tweets', 'likes', 'retweets','const']]
print("VIF (large numbers show collinearity):")
print(pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns))


## analysis by city
data_place = data_place.loc[:, ~data_place.columns.str.contains('^Unnamed')]
data_place['engagement'] = data_place['likes'] + data_place['retweets']
data_place['holidays'] = [x == 11 or x == 12 or x == 1 for x in data_place['month']]
prov = data_place.loc[data_place.place=="Providence", :]
buff = data_place.loc[data_place.place=="Buffalo", :]
sea = data_place.loc[data_place.place=="Seattle", :]

# Providence
col = prov.apply(lambda row: row.year >= 2016, axis=1)
prov = prov.assign(campaign=col.values)
print ("\nAnalysis for Providence: ")
printCoeff(prov)

prov = sm.add_constant(prov)
eq = "diversion_rate ~ num_tweets + engagement + C(holidays) + C(campaign)"
model = smf.ols(formula=eq, data=prov)
results = model.fit()
print(results.summary())
print ("MSE:", eval_measures.mse(prov['diversion_rate'], results.predict()))

X = prov[['num_tweets', 'likes', 'retweets','const']]
print("VIF (large numbers show collinearity):")
print(pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns))

# Buffalo
col = buff.apply(lambda row: row.year >= 2015, axis = 1)
buff = buff.assign(campaign=col.values)
print ("\nAnalysis for Buffalo: ")
printCoeff(buff)

buff = sm.add_constant(buff)
eq = "diversion_rate ~ num_tweets + engagement + C(holidays) + C(campaign)"
model = smf.ols(formula=eq, data=buff)
results = model.fit()
print(results.summary())
print ("MSE:", eval_measures.mse(buff['diversion_rate'], results.predict()))

X = buff[['num_tweets', 'likes', 'retweets','const']]
print("VIF (large numbers show collinearity):")
print(pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns))

# Seattle
print ("\nAnalysis for Seattle: ")
printCoeff(sea)

sea = sm.add_constant(sea)
eq = "diversion_rate ~ num_tweets + engagement + C(holidays)"
model = smf.ols(formula=eq, data=sea)
results = model.fit()
print(results.summary())
print ("MSE:", eval_measures.mse(sea['diversion_rate'], results.predict()))

X = sea[['num_tweets', 'likes', 'retweets','const']]
print("VIF (large numbers show collinearity):")
print(pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns))
