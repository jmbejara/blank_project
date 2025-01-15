"""
Pull from the short-term funding API
Info here:
https://www.financialresearch.gov/short-term-funding-monitor/api/
"""
import pandas as pd
import numpy as np

import os
from pathlib import Path
from settings import config

def pull_series_from_ofr_api(mnemonic=None):
    """
    An example:
    https://data.financialresearch.gov/v1/series/timeseries?mnemonic=REPO-TRI_AR_TOT-F
    """
    df = pd.read_json(
        f'https://data.financialresearch.gov/v1/series/timeseries?mnemonic={mnemonic}',
                )
    
    df.columns=['Date', mnemonic]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    return df

series_descriptions = {
    'REPO-TRI_AR_OO-P': 'Tri-Party Average Rate: Overnight/Open (Preliminary)',
    'REPO-TRI_TV_OO-P': 'Tri-Party Transaction Volume: Overnight/Open (Preliminary)',
    'REPO-TRI_TV_TOT-P': 'Tri-Party Transaction Volume: Total (Preliminary)',
    'REPO-DVP_AR_OO-P': 'DVP Service Average Rate: Overnight/Open (Preliminary)',
    # 'REPO-DVP_OV_OO-P': 'DVP Service Outstanding Volume: Overnight/Open (Preliminary)',
    'REPO-DVP_TV_OO-P': 'DVP Service Transaction Volume: Overnight/Open (Preliminary)',
    'REPO-DVP_TV_TOT-P': 'DVP Service Transaction Volume: Total (Preliminary)',  
    'REPO-DVP_OV_TOT-P': 'DVP Service Outstanding Volume: Total (Preliminary)',
    'REPO-GCF_AR_OO-P': 'GCF Repo Service Average Rate: Overnight/Open (Preliminary)',
    'REPO-GCF_TV_OO-P': 'GCF Repo Service Transaction Volume: Overnight/Open (Preliminary)',
    # 'REPO-GCF_OV_OO-P': 'GCF Repo Service Outstanding Volume: Overnight/Open (Preliminary)',
    'REPO-GCF_TV_TOT-P': 'GCF Repo Service Transaction Volume: Total (Preliminary)',
    'FNYR-BGCR-A':'Broad General Collateral Rate',
    'FNYR-TGCR-A':'Tri-Party General Collateral Rate',
}

def pull_series_list(series_list = list(series_descriptions.keys())):
    df_list = []
    for s in series_list:
        df = pull_series_from_ofr_api(mnemonic=s)
        df_list.append(df)
    df = pd.concat(df_list, axis=1)
    return df

if __name__ == "__main__":
    df = pull_series_list(series_list = list(series_descriptions.keys()))
    
    DATA_DIR = config("DATA_DIR")
    filedir = Path(DATA_DIR)
    filedir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(filedir / 'ofr_public_repo_data.parquet')
