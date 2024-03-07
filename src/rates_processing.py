import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import requests
from interest_rates import merge_and_process_data  # Import the function from Interest_rates.py


##########################################################
# Processing the Rates
##########################################################

'''
It has as inputs: "Fred data" and "Federal Reserve Data Pulling" from the Interest_rates.py file.
the start_date: '2001-01-02' and end_date: '2024-01-31'

The function extrapolate_rates is used to extrapolate the rates for the given maturities.
The function returns a DataFrame containing the extrapolated rates.
'''


def extrapolate_rates(rates):
    extrapolated_rates_df = pd.DataFrame(columns=np.arange(3, 121, 3), index=rates.index)

    months = np.array(rates.columns)
    for index, row in rates.iterrows():
        rates_values = row[months].values
        cs = CubicSpline(months, rates_values, bc_type='natural')

        quarterly_maturities = np.arange(3, 121, 3)
        extrapolated_rates = cs(quarterly_maturities)
        extrapolated_rates_df.loc[index] = extrapolated_rates

    return extrapolated_rates_df

def calc_discount(start_date, end_date):
    # Call the function to get rates
    rates_data = merge_and_process_data(start_date, end_date)  
    if rates_data is None:
        print("No data available for the given date range.")
        return None

    quarterly_rates = extrapolate_rates(rates_data)
    quarterly_rates = quarterly_rates.iloc[:, :20]  # Adjust to only include the first 20 columns
    quarterly_rates.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    quarterly_discount = pd.DataFrame(columns=quarterly_rates.columns, index=quarterly_rates.index)
    for col in quarterly_rates.columns:
        quarterly_discount[col] = quarterly_rates[col].apply(lambda x: np.exp(-(col * x) / 4))

    return quarterly_discount

# Example Usage
if __name__ == "__main__":
    start_date = '2001-01-02'
    end_date = '2024-01-31'
    discount_rates = calc_discount(start_date, end_date)
    if discount_rates is not None:
        print(discount_rates)
