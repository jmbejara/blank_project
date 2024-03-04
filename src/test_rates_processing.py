import pytest
import pandas as pd
import numpy as np
from rates_processing import extrapolate_rates, calc_discount

test_data = pd.DataFrame({
    12: [0.01, 0.011],
    24: [0.012, 0.013],
    36: [0.014, 0.015],
}, index=pd.to_datetime(['2020-01-01', '2020-02-01']))

@pytest.fixture
def sample_rates():
    return test_data

def test_extrapolate_rates(sample_rates):
    result = extrapolate_rates(sample_rates)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert result.shape[1] == 40  # Number of columns should be 40 as per your settings (3 to 120 every 3 months)

def test_calc_discount():
    start_date = '2020-01-01'
    end_date = '2020-02-01'
    result = calc_discount(start_date, end_date)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert all(col in result.columns for col in range(1, 21))  # Check if all expected columns are present
