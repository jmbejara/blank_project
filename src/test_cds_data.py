import pandas as pd
import pytest

import config
import cds_processing    

DATA_DIR = config.DATA_DIR


def test_cds_data():
    df = cds_processing.process_cds_data()
    # Test if the function returns a pandas DataFrame
    assert isinstance(df, pd.DataFrame)

    # Test if the DataFrame has the expected columns
    expected_columns = ['ticker', 'parspread']
    assert all(col in df.columns for col in expected_columns)

def test_calc_cds_monthly():
    # Assert that 20 portfolios are created
    assert len(cds_processing.calc_cds_monthly().columns) == 20


