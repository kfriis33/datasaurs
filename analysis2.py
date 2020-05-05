import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from statsmodels.tools import eval_measures
from statsmodels.stats.outliers_influence import variance_inflation_factor

with open ("data/all_aggregated.csv", 'rb') as f:
    data = pd.read_csv(f)

data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
data['engagement'] = data['likes'] + data['retweets']

print ("Coefficients for aggregated data (with outliers): ")
pearson, p = pearsonr(data['month'], data['diversion_rate'])
print("Pearson (month): %.02f (%.02f)"%(pearson, p))
pearson, p = pearsonr(data['num_tweets'], data['diversion_rate'])
print("Pearson (num_tweets): %.02f (%.02f)"%(pearson, p))
pearson, p = pearsonr(data['likes'], data['diversion_rate'])
print("Pearson (likes): %.02f (%.02f)"%(pearson, p))
pearson, p = pearsonr(data['retweets'], data['diversion_rate'])
print("Pearson (retweets): %.02f (%.02f)"%(pearson, p))
pearson, p = pearsonr(data['MAU'], data['diversion_rate'])
print("Pearson (MAU): %.02f (%.02f)"%(pearson, p))
pearson, p = pearsonr(data['year'], data['diversion_rate'])
print("Pearson (year): %.02f (%.02f)"%(pearson, p))
pearson, p = pearsonr(data['engagement'], data['diversion_rate'])
print("Pearson (engagement): %.02f (%.02f)"%(pearson, p))

data = sm.add_constant(data)
eq = "diversion_rate ~ num_tweets + engagement + C(month) + MAU"
model = smf.ols(formula=eq, data=data)
results = model.fit()
print(results.summary())
print ("MSE:", eval_measures.mse(data['diversion_rate'], results.predict()))

X = data[['num_tweets', 'engagement', 'MAU','const']]
print("VIF:")
print(pd.Series([variance_inflation_factor(X.values, i) for i in range(X.shape[1])], index=X.columns))
