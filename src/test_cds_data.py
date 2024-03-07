import pandas as pd
import pytest

import config
import cds_processing    

DATA_DIR = config.DATA_DIR

def test_calc_cds_monthly():
    # Assert that 20 portfolios are created
    assert len(cds_processing.calc_cds_monthly().columns) == 21


