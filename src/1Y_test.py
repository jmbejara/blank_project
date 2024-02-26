import pandas as pd
import pytest


import config
import load_fred
import 1Y_rates

DATA_DIR = config.DATA_DIR

import pytest
from 1Y_rates import fetch_yield_curve_data

def test_fetch_yield_curve_data_valid_url():
    url = "https://www.example.com/valid_url_with_table.html"
    result = fetch_yield_curve_data(url)
    assert type(result) == pd.DataFrame, "The function should return a DataFrame for a valid URL"

"""""
def test_load_fred_functionality():
    df = load_fred.load_fred(data_dir=DATA_DIR, from_cache=False)
    # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame has the expected columns
    expected_columns = ['CPIAUCNS', 'GDP', 'GDPC1']
    assert all(col in df.columns for col in expected_columns)

    # Test if the function raises an error when given an invalid data directory
    with pytest.raises(FileNotFoundError):
        load_fred.load_fred(data_dir="invalid_directory")

def test_load_fred_data_validity():
    df = load_fred.load_fred(data_dir=DATA_DIR, from_cache=False)
    
    # Test if the default date range has the expected start date and end date
    assert df.index.min() == pd.Timestamp('1913-01-01')
    assert df.index.max() >= pd.Timestamp('2023-09-01')

    # Test if the average annualized growth rate is close to 3.08%
    ave_annualized_growth = 4 * 100 * df.loc['1913-01-01': '2023-09-01', 'GDPC1'].dropna().pct_change().mean()
    assert abs(ave_annualized_growth - 3.08) < 0.1
"""