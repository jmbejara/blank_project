import pandas as pd
import pandas_datareader.data as web
import requests

##########################################################
# FRED Data Pulling
##########################################################

'''
Description:
Selectiong the 3 and 6 month treasury constant maturity rates
The source file was from
3-Month Treasury Constant Maturity Rate: https://fred.stlouisfed.org/series/DGS3MO
6-Month Treasury Constant Maturity Rate: https://fred.stlouisfed.org/series/DGS6MO 
'''

series_descriptions = {
    'DGS3MO': '3-Month Treasury Constant Maturity Rate',
    'DGS6MO': '6-Month Treasury Constant Maturity Rate',
}

def pull_fred_data(start_date, end_date, ffill=True):
    df = web.DataReader(list(series_descriptions.keys()), 'fred', start_date, end_date)
    if ffill:
        for series in series_descriptions.keys():
            df[series].ffill(inplace=True)
    return df

def process_fed_data(start_date, end_date):
    fred_data = pull_fred_data(start_date, end_date)
    fred_data = fred_data.rename(columns={'DGS3MO': '3', 'DGS6MO': '6'})
    return fred_data

##########################################################
# Federal Reserve Data Pulling
##########################################################
'''
# The function fetch_yield_curve_data is used to fetch the yield curve data from a given URL.
# The function returns a DataFrame containing the yield curve data.
# If the URL is invalid or the data cannot be fetched, the function returns None.

'''

def fetch_yield_curve_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        dfs = pd.read_html(response.content)
        yield_curve_df = dfs[1] if len(dfs) >= 2 else dfs[0]
        return yield_curve_df
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

def combine_dataframes(dataframes):
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.set_index('Date', inplace=True)
    return combined_df

def process_dataframe(dataframe, columns_required):
    processed_df = dataframe[columns_required]
    processed_df.columns = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
    processed_df.index = pd.to_datetime(processed_df.index)
    processed_df = processed_df.sort_index()
    return processed_df

def load_rates():
    base_url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628_"
    dataframes = []
    for i in range(1, 14):
        url = f"{base_url}{i}.html"
        yield_curve_data = fetch_yield_curve_data(url)
        if yield_curve_data is not None:
            dataframes.append(yield_curve_data)
    if dataframes:
        all_data = combine_dataframes(dataframes)
        columns_required = ['SVENY01', 'SVENY02', 'SVENY03', 'SVENY04', 'SVENY05', 'SVENY06', 'SVENY07', 'SVENY08', 'SVENY09', 'SVENY10']
        all_data_processed = process_dataframe(all_data, columns_required)
        return all_data_processed
    else:
        return None

##########################################################
# Merging and Processing Data
##########################################################
    
'''
In this file we will merge the data from the two sources:
- The 3 and 6 month treasury constant maturity rates from FRED
- The 1 year treasury constant maturity rates from the Federal Reserve

We will then filter the data to only include the last date for each month
'''

def merge_and_process_data(start_date, end_date):
    # Pull and process FRED data
    fred_data = process_fed_data(start_date, end_date)

    # Load and process Federal Reserve data
    fed_reserve_data = load_rates()
    if fed_reserve_data is None:
        print("No Federal Reserve data loaded.")
        return None

    # Merge the datasets
    merged_data = pd.concat([fred_data, fed_reserve_data], axis=1)

    # Resample to get the last entry of each month
    rates = merged_data.resample('M').last()

    # Filter by the specified date range
    rates = rates[(rates.index >= pd.to_datetime(start_date)) & (rates.index <= pd.to_datetime(end_date))]

    return rates

##########################################################
# Main Execution
##########################################################
if __name__ == "__main__":
    start_date = '2001-01-02'
    end_date = '2024-01-31'
    rates = merge_and_process_data(start_date, end_date)
    if rates is not None:
        print(rates)
