import pandas_datareader.data as web
import pandas as pd
import numpy as np

##########################################################
'''
Selectiong the 3 and 6 month treasury constant maturity rates
The source file was from
3-Month Treasury Constant Maturity Rate: https://fred.stlouisfed.org/series/DGS3MO
6-Month Treasury Constant Maturity Rate: https://fred.stlouisfed.org/series/DGS6MO 
'''
############################################################
series_descriptions = {
    'DGS3MO': '3-Month Treasury Constant Maturity Rate',
    'DGS6MO': '6-Month Treasury Constant Maturity Rate',
}

def pull_fred_data(start_date, end_date, ffill=True):
    """
    Pull data for the specified series from FRED.
    """
    df = web.DataReader(list(series_descriptions.keys()), 'fred', start_date, end_date)

    if ffill:
        for series in series_descriptions.keys():
            df[series].ffill(inplace=True)

    return df

def process_fed_data():
        
    # Call the function to get the data
    start_date = '2001-01-02' # first value that is not NaN
    end_date = '2024-02-15'
    fred_data = pull_fred_data(start_date, end_date)
    fred_data = fred_data.rename(columns ={'DGS3MO': '3',
    'DGS6MO': '6'})

    return fred_data #all the data are 6033 rows and 2 columns

def get_fred_data():
    #Setting a function to store the data
    fred_data = process_fed_data()
    return fred_data

if __name__ == "__main__":
    data = get_fred_data()
    print(data)

