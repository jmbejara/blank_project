import pandas as pd
import pandas_datareader
import config
from pathlib import Path

DATA_DIR = Path(config.data_dir)


def pull_and_save_fred_data(start="1913-01-01", end="2023-10-01", data_dir=DATA_DIR):
    # Load CPI data from FRED, seasonally adjusted
    df = pandas_datareader.get_data_fred(["CPIAUCNS", "GDP", "GDPC1"], start=start, end=end)
    file_dir = Path(data_dir) / "pulled"
    file_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_dir / "fred_cpi.csv")
    # df.to_parquet(file_dir / 'fred_cpi.parquet')


def load_fred(data_dir=DATA_DIR):
    """
    Must first run pull_and_save_fred_data
    """
    file_path = Path(data_dir) / "pulled" / "fred_cpi.csv"
    df = pd.read_csv(file_path, parse_dates=["DATE"])
    df = df.set_index("DATE")
    # df.info()
    # df = pd.read_parquet(file_path)
    return df


if __name__ == "__main__":
    pull_and_save_fred_data(start="1913-01-01", end="2023-10-01", data_dir=DATA_DIR)
