import config
from pathlib import Path
OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME
import pickle
import wrds
import pandas as pd



def get_cds_data():
    db = wrds.Connection(wrds_username=WRDS_USERNAME)
    cds_data = {} 
    for year in range(2001, 2002):  # Loop from 2001 to 2023
        table_name = f"markit.CDS{year}"  # Generate table name dynamically
        query = f"""
        SELECT
            date, ticker, parspread
        FROM 
            {table_name} a 
        WHERE
            a.tenor = '5Y' AND
            a.country = 'United States'
        """
        cds_data[year] = db.raw_sql(query, date_cols=['date'])
    return cds_data