import pandas_datareader.data as web
import pandas as pd
import numpy as np

from pathlib import Path
from settings import config

DATA_DIR = Path(config("DATA_DIR"))
START_DATE = config("START_DATE")
END_DATE = config("END_DATE")


series_to_pull = {
    ## Macro
    "GDP": "GDP",
    "CPIAUCNS": "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average",
    "GDPC1": "Real Gross Domestic Product",
    ## Finance
    "DPCREDIT": "Discount Window Primary Credit Rate",
    # 'DISCOUNT': 'Discount Rate Changes (OLD)', #Discount Rate Changes:
    # Historical Dates of Changes and Rates (DISCONTINUED)
    "EFFR": "Effective Federal Funds Rate",
    "OBFR": "Overnight Bank Funding Rate",
    "SOFR": "SOFR",
    "IORR": "Interest on Required Reserves",
    "IOER": "Interest on Excess Reserves",
    "IORB": "Interest on Reserve Balances",
    "DFEDTARU": "Federal Funds Target Range - Upper Limit",
    "DFEDTARL": "Federal Funds Target Range - Lower Limit",
    "WALCL": "Federal Reserve Total Assets",  # Millions, converted to billions below
    # Assets: Total Assets: Total Assets (Less Eliminations from Consolidation):
    # Wednesday Level
    "TOTRESNS": "Reserves of Depository Institutions: Total",  # Billions
    "TREAST": "Treasuries Held by Federal Reserve",  # Millions, Converted to Billions below
    # Assets: Securities Held Outright:
    # U.S. Treasury Securities: All: Wednesday Level. ( total face value of U.S.
    # Treasury securities held by the Federal Reserve)
    "CURRCIR": "Currency in Circulation",  # Billions
    "GFDEBTN": "Federal Debt: Total Public Debt",  # Millions, Converted to Billions below
    "WTREGEN": "Treasury General Account",  # Billions # Liabilities and Capital: Liabilities: Deposits with F.R. Banks,
    # Other Than Reserve Balances: U.S. Treasury, General Account: Week Average
    "RRPONTSYAWARD": "Fed ON/RRP Award Rate",  # Overnight Reverse Repurchase Agreements
    # Award Rate: Treasury Securities Sold by the Federal Reserve in the Temporary
    # Open Market Operations
    "RRPONTSYD": "Treasuries Fed Sold In Temp Open Mark",  # Billions
    # Overnight Reverse Repurchase Agreements:
    # Total Securities Sold by the Federal Reserve in the Temporary Open Market Operations
    "RPONTSYD": "Treasuries Fed Purchased In Temp Open Mark",  # Billions
    # Overnight Repurchase Agreements:
    # Treasury Securities Purchased by the Federal Reserve in the Temporary
    # Open Market Operations
    "WSDONTL": "SOMA Sec Overnight Lending Volume",  # Millions, Converted to Billions below
    # Memorandum Items: Securities Lent to Dealers: Overnight Facility: Wednesday Level
}

series_descriptions = series_to_pull.copy()
series_descriptions["MY_RPONTSYAWARD"] = "Fed ON/RP Award Rate"  # As far as I can tell,
# the standing repo facility rate is set equal to the upper limit of the fed's target range.
# The ON/RRP rate appears to be set at 5 bps higher than the lower limit of the fed's
# target range.
# The ON/RRP has a counterparty limit. the ON/RP has an aggregate limit that appears to
# have been equal to $500 billion since it started in July 2021 until the time of writing
# (Oct 2023).
series_descriptions["Gen_IORB"] = "Interest on Reserves"  # Backfilled with
# interest on excess reserves
series_descriptions["ONRRP_CTPY_LIMIT"] = "Counter-party Limit at Fed ON/RRP Facility"
series_descriptions["ONRP_AGG_LIMIT"] = "Aggregate Limit at Fed Standing Repo Facility"
# For foreign official institutions, there is a $60 billion per counterparty limit

manual_ONRRP_cntypty_limits = {  # in $ Billions
    "2013-Sep-22": 0,
    "2013-Sep-23": 1,
    "2014-Jan-29": 3,
    "2014-Feb-3": 7,
    "2014-Feb-21": 10,
    "2014-Jul-11": 30,
    "2021-Mar-17": 80,
    "2021-Jun-3": 160,
}


def pull_fred(start_date=START_DATE, end_date=END_DATE, ffill=True):
    """
    Lookup series code, e.g., like this:
    https://fred.stlouisfed.org/series/RPONTSYD
    """
    df = web.DataReader(list(series_to_pull.keys()), "fred", start_date, end_date)

    millions_to_billions = ["TREAST", "GFDEBTN", "WALCL", "WSDONTL"]
    for s in millions_to_billions:
        df[s] = df[s] / 1_000

    # forward_fill = ['DISCOUNT', 'OBFR', 'DPCREDIT', 'TREAST', 'TOTRESNS']
    if ffill:
        forward_fill = [
            "OBFR",
            "DPCREDIT",
            "TREAST",
            "TOTRESNS",
            "WTREGEN",
            "WALCL",
            "CURRCIR",
            "RRPONTSYAWARD",
            "WSDONTL",
        ]
        for s in forward_fill:
            df[s] = df[s].ffill()

    # fill_zeros = ['RRPONTSYD', 'RPONTSYD']
    # for s in fill_zeros:
    #     df[s] = df[s].fillna(0)

    # When IORB is missing, use excess reserve rate
    df["Gen_IORB"] = df["IORB"].fillna(df["IOER"])
    # df['Gen_DISCOUNT'] = df['DPCREDIT'].fillna(df['DISCOUNT'])

    df["ONRRP_CTPY_LIMIT"] = np.nan
    for key in manual_ONRRP_cntypty_limits.keys():
        date = pd.to_datetime(key)
        df.loc[date, "ONRRP_CTPY_LIMIT"] = manual_ONRRP_cntypty_limits[key]
    df["ONRRP_CTPY_LIMIT"] = df["ONRRP_CTPY_LIMIT"].ffill()

    df["ONRP_AGG_LIMIT"] = np.nan
    df.loc["2021-Jul-28", "ONRP_AGG_LIMIT"] = 500
    df["ONRP_AGG_LIMIT"] = df["ONRP_AGG_LIMIT"].ffill()

    df_focused = df.drop(columns=["IORR", "IOER", "IORB"])
    # df_focused.isna().sum()
    # df_focused['WTREGEN'].plot()
    # df_focused['WTREGEN'].ffill().plot()
    return df_focused


def load_fred(data_dir=DATA_DIR):
    """
    Must first run this module as main to pull and save data.
    """
    file_path = Path(data_dir) / "fred.parquet"
    df = pd.read_parquet(file_path)
    # df = pd.read_csv(file_path, parse_dates=["DATE"])
    # df = df.set_index("DATE")
    return df


def demo():
    df = load_fred()


if __name__ == "__main__":

    today = pd.Timestamp.today().strftime("%Y-%m-%d")
    end_date = today
    df = pull_fred(START_DATE, end_date)
    filedir = Path(DATA_DIR) 
    filedir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(filedir / "fred.parquet")
    df.to_csv(filedir / "fred.csv")
