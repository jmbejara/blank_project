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