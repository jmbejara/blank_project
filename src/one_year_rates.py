import requests
import pandas as pd


'''
# The function fetch_yield_curve_data is used to fetch the yield curve data from a given URL.
# The function returns a DataFrame containing the yield curve data.
# If the URL is invalid or the data cannot be fetched, the function returns None.

'''

def fetch_yield_curve_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
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
    # Start of the inline code
    base_url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628_"
    dataframes = []

    for i in range(1, 14):
        url = f"{base_url}{i}.html"
        yield_curve_data = fetch_yield_curve_data(url)
        if yield_curve_data is not None:
            dataframes.append(yield_curve_data)

    if dataframes:
        all_data = combine_dataframes(dataframes)
        columns_required = ['SVENY01','SVENY02','SVENY03','SVENY04','SVENY05','SVENY06','SVENY07','SVENY08','SVENY09','SVENY10']
        all_data_processed = process_dataframe(all_data, columns_required)
        return all_data_processed
    else:
        return None


def get_rates_data():
    rates_data = load_rates()
    return rates_data

#the output is "all_data_processed" which is the processed dataframe
rates_data = load_rates()
if rates_data is not None:
    print(rates_data.head())  
else:
    print("No data loaded.")
