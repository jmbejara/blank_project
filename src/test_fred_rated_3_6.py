import pandas as pd
import pytest
from fred_rates_3_6 import pull_fred_data, process_fed_data, get_fred_data

'''
This file contains the tests for the fred_rates_3_6.py file

The tests are used to ensure that the functions are working as expected

'''

def test_pull_fred_data():
    # Test the pull_fred_data function with a known date range
    start_date = '2021-01-01'
    end_date = '2021-01-31'
    data = pull_fred_data(start_date, end_date, ffill=True)
    assert data is not None, "Failed to pull data from FRED"
    assert isinstance(data, pd.DataFrame), "Returned data is not a DataFrame"
    assert not data.empty, "Returned DataFrame is empty"

def test_process_fed_data():
    # Test the process_fed_data function
    data = process_fed_data()
    assert data is not None, "Failed to process FRED data"
    assert isinstance(data, pd.DataFrame), "Processed data is not a DataFrame"
    assert '3' in data.columns, "Column '3' is missing in processed data"
    assert '6' in data.columns, "Column '6' is missing in processed data"

def test_get_fred_data():
    data = get_fred_data()
    assert data is not None, "Failed to get FRED data"
    assert isinstance(data, pd.DataFrame), "Returned data is not a DataFrame"

if __name__ == "__main__":
    pytest.main()
