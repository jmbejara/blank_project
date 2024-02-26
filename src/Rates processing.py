import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import requests
import fred_rates_3_6
import one_year_rates


def process_rates_data(start_date, end_date):
    # pull rates data
    short_term_rates = fred_rates_3_6.process_fed_data()
    long_term_rates = one_year_rates.load_rates()

    # concat short and long term rates
    rates = pd.concat([short_term_rates, long_term_rates])
    #resample to monthly
    rates= rates.resample('M').last()
    rates = rates[(rates.index >= start_date) & (rates.index <= end_date)]
    return rates


def extrapolate_rates(rates):
    extrapolated_rates_df = pd.DataFrame(columns=np.arange(3, 121, 3), index=rates.index)  # Set column names and index

    months = np.array(rates.columns)
    for index, row in rates.iterrows():
        # Extract rates for a date
        rates = row[months].values
        # Fit a cubic spline to the data
        cs = CubicSpline(months, rates, bc_type='natural')

        # Use the spline to extrapolate quarterly rates
        quarterly_maturities = np.arange(3, 121, 3)  # From 3 to 120 months, every 3 months
        extrapolated_rates = cs(quarterly_maturities)
        # Append new row to the DataFrame
        extrapolated_rates_df.loc[index] = extrapolated_rates

    return extrapolated_rates_df

def calc_discount(start_date, end_date):
   rates = process_rates_data(start_date, end_date) 
   quarterly_rates = extrapolate_rates(rates)
   quarterly_rates = quarterly_rates.iloc[:, :20]
   quarterly_rates.columns = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
   quarterly_discount = pd.DataFrame(columns=quarterly_rates.columns, index=quarterly_rates.index)
   for col in quarterly_rates.columns:
        quarterly_discount[col] = quarterly_rates[col].apply(lambda x: np.exp(-(col * x)/4))
   
   return quarterly_discount