import numpy as np
import pandas as pd
import requests
from rates_processing import *
from cds_processing import *
import config
from pathlib import Path
from pandas.tseries.offsets import MonthEnd

OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)



def process_real_cds_return():
    actual_return = pd.read_csv('~/Documents/GitHub/P15_DANK/data/manual/He_Kelly_Manela_Factors_And_Test_Assets_monthly.csv')
    actual_return = actual_return[['yyyymm','CDS_01','CDS_02','CDS_03','CDS_04','CDS_05','CDS_06','CDS_07','CDS_08','CDS_09','CDS_10','CDS_11','CDS_12','CDS_13','CDS_14','CDS_15','CDS_16','CDS_17','CDS_18','CDS_19','CDS_20']]
    actual_return = actual_return.dropna(axis=0)
    actual_return['yyyymm'] = pd.to_datetime(actual_return['yyyymm'], format='%Y%m')
    actual_return['yyyymm']= actual_return['yyyymm'] + MonthEnd(1)
    actual_return = actual_return.set_index('yyyymm')
    return actual_return

def calc_cds_return(start_date, end_date,Method):

    loss_given_default =0.6

    quarterly_discount = calc_discount(start_date, end_date)
    quarterly_discount = quarterly_discount[:-1]

    cds_spread = process_cds_monthly(method=Method)
    cds_spread= cds_spread.bfill()
    cds_spread = cds_spread.set_index('Date')
    cds_spread.index = pd.to_datetime(cds_spread.index)

    lambda_df = 4 * np.log(1+(cds_spread/(4*loss_given_default)))
    quarters = range(1, 21)  # 1 to 20 quarters
    risky_duration = pd.DataFrame(index=lambda_df.index, columns=lambda_df.columns)
    for col in lambda_df.columns:
        quarterly_survival_probability = pd.DataFrame(index=lambda_df.index, columns=quarters)
        for quarter in quarters:
            quarterly_survival_probability[quarter] = np.exp(-((quarter * lambda_df[col]) / 4))
        temp_df = quarterly_survival_probability * quarterly_discount
        risky_duration[col] = 0.25 * temp_df.sum(axis=1)
    risky_duration_shifted = risky_duration.shift(1)
    cds_spread_shifted = cds_spread.shift(1)
    cds_spread_change = cds_spread.diff()
    cds_return = ((cds_spread_shifted/12) + (cds_spread_change * risky_duration_shifted))
    return cds_return

def calc_difference(cds_return, actual_return):
    '''
    Function inputs - calculated cds returns, actual returns from He-Kelly paper

    output - Actual returns, cds returns and Difference of Actual return - Calculated return
    Finally, all have same index and column names
    
    '''
    cds_return = cds_return[cds_return.index <= '2012-12-31']
    cds_return = cds_return.dropna(axis=0)
    actual_return = actual_return.reindex(cds_return.index)
    actual_return.columns = cds_return.columns
    diff = (actual_return - cds_return)*100
    return actual_return, cds_return, diff