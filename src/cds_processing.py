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

cds_data = get_cds_data()

with open('data/manual/cds_data.pkl', 'wb') as handle:
    pickle.dump(cds_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def process_cds_data():
    for year, data in cds_data.items():
        cds_data[year] = data.set_index('date')

    monthly_cds_data = {}
    for year, data in cds_data.items():
        monthly_cds_data[year] = data.resample('M').last()

    cds_data[2001].index = pd.to_datetime(cds_data[2001].index)

    a = cds_data[2001].groupby(['date','ticker']).mean()
    df = a.reset_index()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # Apply the function to each group
    end_of_month_data = df.groupby('ticker').apply(resample_end_of_month)

    # Reset the index if needed
    end_of_month_data.reset_index(level=0, drop=True, inplace=True)

    # Ensure the 'date' column is the right datetime type
    df.reset_index(inplace=True)
    df['date'] = pd.to_datetime(df['date'])

    # Sort values by 'date' and 'parspread' to ensure proper quantile ranking
    df_sorted = df.sort_values(['date', 'parspread'])

    # Group by 'date' and apply the function to assign quantiles
    df_quantiled = df_sorted.groupby('date').apply(assign_quantiles)
    df_quantiled.rename(columns={'date': 'Date'}, inplace=True)


    df_quantiled.reset_index(inplace=True)
    #df_quantiled.drop(columns=['level_1','index','date'], inplace=True)
    return df_quantiled
