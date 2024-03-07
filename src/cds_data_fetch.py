import config
from pathlib import Path
OUTPUT_DIR = Path(config.OUTPUT_DIR)
DATA_DIR = Path(config.DATA_DIR)
WRDS_USERNAME = config.WRDS_USERNAME
import pickle
import wrds
import pandas as pd



def get_cds_data():
    """
    Connects to a WRDS (Wharton Research Data Services) database and fetches Credit Default Swap (CDS) data 
    for each year from 2001 to 2023 from tables named `markit.CDS{year}`. The data fetched includes the date, 
    ticker, and parspread where the tenor is '5Y' and the country is 'United States'. The fetched data for each 
    year is stored in a dictionary with the year as the key. The function finally returns this dictionary.

    Returns:
        dict: A dictionary where each key is a year from 2001 to 2023 and each value is a DataFrame containing 
        the date, ticker, and parspread for that year.
    """
    db = wrds.Connection(wrds_username=WRDS_USERNAME)
    cds_data = {} 
    for year in range(2001, 2024):  # Loop from 2001 to 2005
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