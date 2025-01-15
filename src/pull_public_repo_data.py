import pandas as pd

import pull_fred
import pull_ofr_api_data

import os
from pathlib import Path
from settings import config
OUTPUT_DIR = config("OUTPUT_DIR")
DATA_DIR = config("DATA_DIR")

def load_all(data_dir = DATA_DIR, normalize_timing=True):
    data_dir = Path(data_dir)
    # df_bloomberg = pd.read_parquet(data_dir / 'bloomberg_repo_rates.parquet')
    df_fred = pd.read_parquet(data_dir / 'fred.parquet')
    df_ofr_api = pd.read_parquet(data_dir / 'ofr_public_repo_data.parquet')
    # df_bloomberg.index.name = 'DATE'
    df_ofr_api.index.name = 'DATE'
    
    df = pd.concat([df_fred, df_ofr_api], axis=1)
    if normalize_timing:
        # Normalize end-of-day vs start-of-day difference
        df.loc['2016-12-14', ['DFEDTARU', 'DFEDTARL']] = df.loc['2016-12-13', ['DFEDTARU', 'DFEDTARL']]
        df.loc['2015-12-16', ['DFEDTARU', 'DFEDTARL']] = df.loc['2015-12-15', ['DFEDTARU', 'DFEDTARL']]
    return df

_descriptions_1 = pull_fred.series_descriptions
_descriptions = pull_ofr_api_data.series_descriptions
series_descriptions = {
    **_descriptions_1, 
    **_descriptions,
    }

if __name__ == "__main__":
    df = load_all()
    df[['DFEDTARU', 'DFEDTARL']].rename(columns=series_descriptions).plot()
    # df['BGCR'].plot()
    # df.loc['2019', :]