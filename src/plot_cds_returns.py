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