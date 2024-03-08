from cds_data_fetch import *
import pandas as pd
from pandas.tseries.offsets import MonthEnd, YearEnd

import numpy as np
import wrds

import config
from pathlib import Path
import cds_processing
import plot_interest_rates
from plot_interest_rates import plot_interest_rates
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats
import seaborn as sns
import cds_processing
from cds_processing import calc_cds_monthly
import plot_cds
from plot_cds import cds_spread_plot
import calc_cds_returns
from calc_cds_returns import calc_cds_return 
from calc_cds_returns import calc_difference

def plot_cds_returns_mean(start_date, end_date,Method='mean'):
    data = calc_cds_return(start_date, end_date,Method='mean')
    if data is None:
        print("No data available for the given date range.")
        return

    plt.figure(figsize=(15, 10))
    sns.boxplot(data=data)
    plt.title("Box Plot of CDS returns - mean method")
    plt.ylabel("Return (%)")
    plt.xticks(rotation=45)
    plt.show()

def plot_cds_returns_median(start_date, end_date,Method='median'):
    data = calc_cds_return(start_date, end_date,Method='median')
    if data is None:
        print("No data available for the given date range.")
        return

    plt.figure(figsize=(15, 10))
    sns.boxplot(data=data)
    plt.title("Box Plot of CDS returns - median method")
    plt.ylabel("Return (%)")
    plt.xticks(rotation=45)
    plt.show()

def plot_cds_returns_weighted(start_date, end_date,Method='weighted'):
    data = calc_cds_return(start_date, end_date,Method='weighted')
    if data is None:
        print("No data available for the given date range.")
        return

    plt.figure(figsize=(15, 10))
    sns.boxplot(data=data)
    plt.title("Box Plot of CDS returns - weighted method")
    plt.ylabel("Return (%)")
    plt.xticks(rotation=45)
    plt.show()

def performance_summary(asset_return, period):
    
    return_index = 1000*(1+asset_return).cumprod() 
    previous_peaks = return_index.cummax() 
    drawdowns = (return_index - previous_peaks)/previous_peaks 
    
    recovery_date = [] 
    for col in return_index.columns: 
        prev_max = previous_peaks[col][:drawdowns[col].idxmin()].max() 
        recovery_return = pd.DataFrame([return_index[col][drawdowns[col].idxmin():]]).T
        recovery_date.append(recovery_return[recovery_return[col] >= prev_max].index.min())
    
    df = pd.DataFrame({
    'Mean': asset_return.mean() * 12,
    'Volatility': asset_return.std() * np.sqrt(12),
    'Sharpe Ratio': (asset_return.mean() * 12) / (asset_return.std() * np.sqrt(12)),
    'Skewness': asset_return.skew(),
    'Excess Kurtosis': asset_return.kurtosis(),
    'VaR (.05)' : asset_return.quantile(0.05, axis = 0),
    'Max Drawdown' : drawdowns.min(),
    'Peak' : [previous_peaks[col][:drawdowns[col].idxmin()].idxmax() for col in previous_peaks.columns],
    'Bottom' : drawdowns.idxmin(),
    })

    return df    



def plot_sharpe_ratios(performance_mean, performance_median, performance_weighted):
    """
    This function plots the Sharpe Ratios for mean, median, and weighted performance data.

    :param performance_mean: DataFrame containing mean performance data including 'Sharpe Ratio'.
    :param performance_median: DataFrame containing median performance data including 'Sharpe Ratio'.
    :param performance_weighted: DataFrame containing weighted performance data including 'Sharpe Ratio'.
    """
    sharpe_ratio_mean = performance_mean['Sharpe Ratio']
    sharpe_ratio_median = performance_median['Sharpe Ratio']
    sharpe_ratio_weighted = performance_weighted['Sharpe Ratio']

    plt.figure(figsize=(14, 6))

    plt.plot(sharpe_ratio_mean, label='Mean')
    plt.plot(sharpe_ratio_median, label='Median')
    plt.plot(sharpe_ratio_weighted, label='Weighted')

    plt.title('Sharpe Ratios across different methods')
    plt.xlabel('CDS Portfolio')
    plt.ylabel('Sharpe Ratio')
    plt.legend()

    plt.show()
