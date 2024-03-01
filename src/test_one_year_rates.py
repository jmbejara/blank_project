import pandas as pd
import pytest
from one_year_rates import fetch_yield_curve_data, combine_dataframes, process_dataframe, load_rates

'''
This file contains the tests for the one_year_rates.py file
The tests are used to ensure that the functions are working as expected

'''

def test_fetch_yield_curve_data():
    test_url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628_1.html"
    data = fetch_yield_curve_data(test_url)
    assert data is not None, "Failed to fetch yield curve data"
    assert isinstance(data, pd.DataFrame), "Fetched data is not a DataFrame"

def test_load_rates():
    rates_data = load_rates()
    assert rates_data is not None, "Failed to load rates data"
    assert isinstance(rates_data, pd.DataFrame), "Loaded rates data is not a DataFrame"
    assert not rates_data.empty, "Loaded rates data is empty"
