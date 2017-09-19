import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
style.use('fivethirtyeight')

# To avoid directly listing api on file
api_key = open('quandlapikey.txt', 'r').read().rstrip()

# If the hpi increase, the current features are given a label of 1 
def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

# Not necessary -- for practice
def moving_average(values):
    return mean(values)    

# Read in the pickle with HPI data
housing_data = pd.read_pickle('HPI.pickle')

housing_data = housing_data.pct_change()

# Handling erroneous data
housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
housing_data['US_HPI_Future'] = housing_data['United States'].shift(-1)
housing_data.dropna(inplace=True)

#print(housing_data[['US_HPI_Future', 'United States']].head())

housing_data['label'] = list(map(create_labels, housing_data['United States'], housing_data['US_HPI_Future']))
print(housing_data.head())          

#housing_data['ma_apply_example'] = pd.rolling_apply(housing_data['M30'], 10, moving_average)
housing_data['ma_apply_example'] = housing_data['M30'].rolling(10).apply(moving_average)
print(housing_data.tail())
