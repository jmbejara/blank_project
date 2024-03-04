from cds_data_fetch import *
import pandas as pd
from pandas.tseries.offsets import MonthEnd, YearEnd

import numpy as np
import wrds

import config
from pathlib import Path

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME

def assign_quantiles(group, n_quantiles=20):
    # Use qcut to assign quantile bins; add 1 because bins are zero-indexed by default
    group['quantile'] = pd.qcut(group['parspread'], n_quantiles, labels=False) + 1
    return group

# Create a function to resample and select the last value for each month
def resample_end_of_month(data):
    return data.resample('M').last()

def process_cds_data():

    cds_data_dict = get_cds_data()

    cds_data = pd.concat(cds_data_dict.values(), axis=0)

    df = cds_data.groupby(['date','ticker']).mean().reset_index()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Apply the function to each group
    end_of_month_data = df.groupby('ticker').apply(resample_end_of_month)

    # Reset the index if needed
    end_of_month_data.reset_index(level=0, drop=True, inplace=True)

    # Ensure the 'date' column is the right datetime type
    end_of_month_data.reset_index(inplace=True)
    end_of_month_data['date'] = pd.to_datetime(end_of_month_data['date'])

    # Sort values by 'date' and 'parspread' to ensure proper quantile ranking
    end_of_month_data_sorted = end_of_month_data.sort_values(['date', 'parspread'])

    # Group by 'date' and apply the function to assign quantiles
    end_of_month_data_quantiled = end_of_month_data_sorted.groupby('date').apply(assign_quantiles)
    end_of_month_data_quantiled.rename(columns={'date': 'Date'}, inplace=True)


    end_of_month_data_quantiled.reset_index(inplace=True)
    #end_of_month_data_quantiled.drop(columns=['level_1','index','date'], inplace=True)
    return end_of_month_data_quantiled

def calc_cds_monthly(method = 'median'):
    if Path(OUTPUT_DIR / 'cds_monthly_spread_median.csv').exists() and method == 'median':
        return pd.read_csv(OUTPUT_DIR / 'cds_monthly_spread_median.csv')
    df = process_cds_data()
    df.set_index('quantile', inplace = True)

    def weighted_mean(data):
        weights = data['parspread']
        return (data['parspread'] * weights).sum() / weights.sum()

    if method == 'mean':

        comb_spread = df.groupby(['quantile', 'Date'])['parspread'].mean().reset_index()
    elif method == 'median':
        comb_spread = df.groupby(['quantile', 'Date'])['parspread'].median().reset_index()
    elif method == 'weighted':
        comb_spread = df.groupby(['quantile', 'Date']).apply(weighted_mean).reset_index(name = 'parspread')

    # Pivot the table to have 'date' as index, 'quantile' as columns, and mean 'parspread' as values
    pivot_table = comb_spread.pivot_table(index='Date', columns='quantile', values='parspread')

    # Rename the columns to follow the 'cds_{quantile}' format
    pivot_table.columns = [f'cds_{int(col)}' for col in pivot_table.columns]
    pivot_table.to_csv(OUTPUT_DIR / 'cds_monthly_spread_median.csv')
    return pivot_table
