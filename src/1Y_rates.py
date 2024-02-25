import requests
import pandas as pd

def fetch_yield_curve_data(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        # Use pandas to read tables from the webpage content
        dfs = pd.read_html(response.content)
        
        # Check if there are at least two tables
        if len(dfs) >= 2:
            # Adjusted to select the second table (index 1)
            yield_curve_df = dfs[1]
        else:
            # Handle the case where there are fewer than two tables
            yield_curve_df = dfs[0]
        
        # You can process the dataframe further as needed
        return yield_curve_df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Base URL without the last number
base_url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628_"


dataframes = []

for i in range(1, 14):
    url = f"{base_url}{i}.html"
    yield_curve_data = fetch_yield_curve_data(url)
    
    if yield_curve_data is not None:
        
        dataframes.append(yield_curve_data)

all_data = pd.concat(dataframes, ignore_index=True)
all_data.set_index('Date', inplace=True)

## Dataframe processing - change column names, sort
columns_required = ['SVENY01','SVENY02','SVENY03','SVENY04','SVENY05','SVENY06','SVENY07','SVENY08','SVENY09','SVENY10']

all_data = all_data[columns_required]
all_data.columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
all_data.index = pd.to_datetime(all_data.index)
all_data= all_data.sort_index()

all_data