import pandas as pd
from fred_rates_3_6 import get_fred_data
from one_year_rates import get_rates_data


##########################################################
'''
In this file we will merge the data from the two sources:
- The 3 and 6 month treasury constant maturity rates from FRED
- The 1 year treasury constant maturity rates from the Federal Reserve

We will then filter the data to only include the last date for each month
'''
############################################################


def merge_data():
    fred_data = get_fred_data()
    rates_data = get_rates_data()

    # Concatenate the dataframes along the columns
    merged_data = pd.concat([fred_data, rates_data], axis=1)

    # Filter by date range
    start_date = '2001-01-02'  # first date in the fred_data that is not NaN
    end_date = '2024-01-31'
    merged_data = merged_data.loc[start_date:end_date]

    # Select the last date for each month
    monthly_last_date = merged_data.groupby(pd.Grouper(freq='M')).last()

    return monthly_last_date

if __name__ == "__main__":
    monthly_data = merge_data()
    print(monthly_data)
