"""
Functions used in NYISO project
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import math

def get_slope(y):
    x = range(len(y))
    slope = np.polyfit(x, y, 1)[0]
    return slope

def get_acceleration(y):
    x = range(len(y))
    acc = 0.5*np.polyfit(x, y, 2)[0]
    return acc

def cyc_feats(data, feat):
    start = data.index[0].date().year-1
    data['cyc_{0}_x'.format(str(feat))] = np.cos(((2*np.pi)/data[feat])*(data['year']-(start))) #x-coord
    data['cyc_{0}_y'.format(str(feat))] = np.sin(((2*np.pi)/data[feat])*(data['year']-(start))) #y-coord
    return data


def create_features(data, tar):
    """
    Creates time series features from datetime index
    """
    data['date'] = data.index
    data['hour'] = data['date'].dt.hour
    data['dayofweek'] = data['date'].dt.dayofweek
    data['quarter'] = data['date'].dt.quarter
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    data['dayofyear'] = data['date'].dt.dayofyear
    data['dayofmonth'] = data['date'].dt.day
    data['weekofyear'] = data['date'].dt.weekofyear

    """
    Creates features based on trends of the target
    """
    for i in [14, 28, 60, 90]:
        data['MA_{0}'.format(str(i))] = data[tar].rolling(24*i).mean() # rolling average
        data['MMAX_{0}'.format(str(i))] = data[tar].rolling(24*i).max() # rolling maximum
        data['MMIN_{0}'.format(str(i))] = data[tar].rolling(24*i).min() # rolling minimum
        data['MSTD_{0}'.format(str(i))] = data[tar].rolling(24*i).std() # rolling standard deviation
        data['MSLOPE_{0}'.format(str(i))] = data[tar].rolling(24*i).apply(lambda x: get_slope(x), raw=True) # rolling slope
        data['MACC_{0}'.format(str(i))] = data[tar].rolling(24*i).apply(lambda x: get_acceleration(x),raw=True) # rolling acceleration
    for i in [1, 7, 30, 60, 90, 180, 365]:
        # add the lagged Load as a feature
        data['lag_{0}'.format(str(i))] = data[tar].shift(24*i)
        # as well as the percentage of the current Load for each lagged closing price
        data['pct_{0}'.format(str(i))] = data['lag_{0}'.format(str(i))] / data[tar]
   
    """
    Creates cyclical features based on seasonal data
    """
    feats = ['month', 'dayofmonth', 'dayofyear', 'weekofyear']
    for feat in feats:
        data = cyc_feats(data, feat) #create cyclical features
    return data

def split_data(data, split_date):
    return data[data.index < split_date].copy(), \
               data[data.index >=  split_date].copy()

def data_prep(data, target, _id, isTest=0):
    """
    Separates columns used in model from target and identifier columns
    returns a list of columns to be used in model and columns that may have use
    """
    used_cols = [col for col in data.columns.tolist() if col not in [target, _id]]
    keep_cols = used_cols
    if isTest:
        pass
    else:
        keep_cols += [target]
    used_cols = [col for col in keep_cols if col not in [target, _id]]
    return data[keep_cols].copy(), keep_cols, used_cols

def plot_(data, target, begin, end, title=None):
    plt.figure(figsize=(15,3))
    if title == None:
        plt.title('From {0} To {1}'.format(begin, end))
    else:
        plt.title(title)
    plt.xlabel('time')
    plt.ylabel('energy consumed')
    plt.plot(data.index, target, '-', label='actual')
    plt.plot(test.index, y_pred, '-', label='prediction')
    plt.legend()
    plt.xlim(left=begin, right=end)

def mean_absolute_percentage_error(y_true, y_pred): 
    """Calculates MAPE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def symmetric_mape(A, F):
    """Calculates Symmetric MAPE given y_true and y_pred"""
    return (100/len(A)) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))

def forecast_error(y_true, y_pred):
    return y_true - y_pred

def mean_forecast_error(forecast_error):
    return forecast_error.mean()

def create_split(X, n_splits):
    """
    creates splits for time series data for cross validation
    """
    split_points = []
    n = len(X)
    for split in range(n_splits):
        split_points.append((0, n * (split + 1) // n_splits))
#         split_points.append((n * split // n_splits, n * (split + 1) // n_splits))
    result = []
    for i in range(len(split_points)):
        result.append(split_points[i])
#         for j in range(i + 1, len(split_points)):
#             result.append((split_points[i][0], split_points[j][1]))
    return result


