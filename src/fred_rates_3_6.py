import pandas_datareader.data as web
import pandas as pd
import numpy as np

##########################################################
#test 2

series_descriptions = {
    'DGS3MO': '3-Month Treasury Constant Maturity Rate',
    'DGS6MO': '6-Month Treasury Constant Maturity Rate',
}

def pull_fred_data(start_date, end_date, ffill=True):
    """
    Pull data for the specified series from FRED.
    """

    # Using the same structure from HW1
    df = web.DataReader(list(series_descriptions.keys()), 'fred', start_date, end_date)

    if ffill:
        for series in series_descriptions.keys():
            df[series].ffill(inplace=True)

    return df

# Call the function to get the data
start_date = '2001-01-02' # first value that is not NaN
end_date = '2024-02-15'
fred_data = pull_fred_data(start_date, end_date)


fred_data #all the data are 6033 rows and 2 columns

#store the data in a csv file
#fred_data.to_csv('data\manual\fred_data.csv')

