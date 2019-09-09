# -*- coding: utf-8 -*-
"""stockpredictionHW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/yossi94/50892dc7e17533237da378885845985b/stockpredictionhw.ipynb

# **Setup and Dependencies**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Data import
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

!pip install yfinance --upgrade --no-cache-dir
yf.pdr_override()

#For mounting to drive
from google.colab import drive

#Modeling
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn import preprocessing 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

#Modeling Metrics
from sklearn import metrics

# Commented out IPython magic to ensure Python compatibility.
#Mount folder to save and retrieve outputs 
drive.mount('/content/drive',force_remount=True)
# %cd "/content/drive/My Drive/siraj_homework"

"""# Import Data and Discovery"""

df_full = pdr.get_data_yahoo("RELIANCE.NS", start="2018-01-01").reset_index()

df_full.to_csv('output/RELIANCE.NS.csv',index=False)

df_full.shape

df_full.head()

df_full.describe()

df_full["Adj Close"].plot()

"""# Data Preproccesing"""

df_full.set_index("Date", inplace=True)

df_full.head()

window_size=32
num_samples=len(df_full)-window_size

# Get indices of access for the data
indices=np.arange(num_samples).astype(np.int)[:,None]+np.arange(window_size+1).astype(np.int)

data = df_full['Adj Close'].values[indices] # Create the 2D matrix of training samples
x = data[:,:-1] # Each row represents 32 days in the past 
y = data[:,-1] # Each output value represents the 33rd day

y

split_fraction=0.8
ind_split=int(split_fraction*num_samples)

x_train = x[:ind_split]
y_train = y[:ind_split]
x_test = x[ind_split:]
y_test = y[ind_split:]

x_test.shape

"""# Modeling"""

#Help Functions 
def get_performance (model_pred):
  #Function returns standard  performance metrics
  print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, model_pred).round(4))
  print('Mean Squared Error:', metrics.mean_squared_error(y_test, model_pred).round(4))
  print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, model_pred)).round(4))
  
  
  
def get_plot (model_pred):
   plt.scatter(model_pred, y_test, color="gray")
   plt.plot(y_test, y_test, color='red', linewidth=2)

y

"""# Baseline"""

y_pred_lag=np.roll(y_test, 1)

get_performance(y_pred_lag)

get_plot(y_pred_lag)

"""# Linear Regression"""

model_lr=LinearRegression()
model_lr.fit(x_train, y_train)

y_pred_lr=model_lr.predict(x_test)

get_performance(y_pred_lr)

get_plot(y_pred_lr)

x

get_performance(y_pred_lr)

"""# Method #1-Ridge Regression"""

model_ridge = Ridge()
model_ridge.fit(x_train, y_train)

#generate predictions
y_pred_ridge=model_ridge.predict(x_test)

get_performance(y_pred_ridge)

get_plot(y_pred_ridge)

"""#          Gradient Boosting Trees"""

# Model #2 -  Gradient Boosting Trees
model_gb = GradientBoostingRegressor()
model_gb.fit(x_train, y_train)

# Infer
y_pred_gb = model_gb.predict(x_test)

get_performance(y_pred_gb)

get_plot(y_pred_gb)

"""# Comparison"""

df_comp=pd.DataFrame({"lag":np.absolute(y_test-y_pred_lag),
                     "lr":np.absolute(y_test-y_pred_lr),
                     "ridge":np.absolute(y_test-y_pred_ridge),
                     "gb":np.absolute(y_test-y_pred_gb)})

df_comp.plot.bar(figsize=(18,8))
plt.ylim(0,10)
plt.xlim(5,20)

"""# Conclusion 

I have used Reliance Industries Ltd to perform the following stock prediction using Regression models
"""