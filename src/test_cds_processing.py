import pytest
import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from cds_processing import *

def test_assign_quantiles():
    mock_data = pd.DataFrame({
        'parspread': np.random.rand(100)
    })
    n_quantiles = 5
    result = assign_quantiles(mock_data, n_quantiles)
    assert 'quantile' in result.columns
    assert not result['quantile'].isnull().any()
    assert result['quantile'].nunique() == n_quantiles

def test_calc_cds_monthly():
    monthly_data = calc_cds_monthly(method='median')
    assert not monthly_data.empty
    assert 'cds_20' in monthly_data.columns


def test_process_cds_monthly():
    processed_monthly_data = process_cds_monthly(method='median')
    assert not processed_monthly_data.empty
    assert 'cds_20' in processed_monthly_data.columns