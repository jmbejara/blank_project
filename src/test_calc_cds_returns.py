import pytest
import pandas as pd
import numpy as np
from calc_cds_returns import *
import config

DATA_DIR = config.DATA_DIR

def test_process_real_cds_return():
    df = process_real_cds_return()
    assert (df.empty == False)

def test_calc_cds_return():
    start_date = '2001-01-01'
    end_date = '2021-01-31'
    m = 'mean'
    df = calc_cds_return(start_date, end_date,m)
    assert (df.empty == False)
    
    total_values = df.size
    nan_values = df.isna().sum().sum()
    tolerance_level = 0.1 * total_values
    assert nan_values < tolerance_level

def test_calc_difference():
    start_date = '2001-01-01'
    end_date = '2021-01-31'
    m = 'mean'
    df = calc_cds_return(start_date, end_date,m)
    df2 = process_real_cds_return()
    actual_return, cds_return, diff = calc_difference(df, df2)
    assert actual_return.shape == diff.shape
    assert cds_return.shape == actual_return.shape
    assert list(actual_return.columns) == list(cds_return.columns)

