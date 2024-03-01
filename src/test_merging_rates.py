#Final version of the test_merging_rates.py file

'''
The test_merging_rates.py file contains the test cases for the merge_data function in the merging_rates.py file.

The merge_data function reads the exchange rates from the federal reserve and the FRED databases and merges them into a single DataFrame. 

The function then returns the merged DataFrame ans tested to ensure that it returns a non-empty DataFrame.

'''

import pandas as pd
import pytest
from merging_rates import merge_data

def test_merge_data():
    # Test the merge_data function
    merged_data = merge_data()
    assert merged_data is not None, "Merged data is None"
    assert isinstance(merged_data, pd.DataFrame), "Merged data is not a DataFrame"
    assert not merged_data.empty, "Merged DataFrame is empty"

    # Check if the data contains only the last date of each month
    all_dates = merged_data.index
    all_last_dates_of_month = all_dates == all_dates.to_period('M').to_timestamp('M')
    assert all_last_dates_of_month.all(), "Not all dates are the last date of their respective months"
