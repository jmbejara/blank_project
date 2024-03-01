import pandas as pd
import pytest
from merging_rates import merge_data

'''
This file contains the tests for the merging_rates.py file
The tests are used to ensure that the functions are working as expected

'''


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

if __name__ == "__main__":
    pytest.main()
