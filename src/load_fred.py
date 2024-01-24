import pandas as pd
import pandas_datareader
import config
from pathlib import Path

DATA_DIR = Path(config.DATA_DIR)


def load_fred(
    data_dir=DATA_DIR,
    from_cache=True,
    save_cache=False,
    start="1913-01-01",
    end="2023-10-01",
):
    """
    Must first run pull_and_save_fred_data. If loading from cache, then start
    and dates are ignored
    """
    if from_cache:
        file_path = Path(data_dir) / "pulled" / "fred.parquet"
        # df = pd.read_csv(file_path, parse_dates=["DATE"])
        df = pd.read_parquet(file_path)
        # df = df.set_index("DATE")
    else:
        # Load CPI, nominal GDP, and real GDP data from FRED, seasonally adjusted
        df = pandas_datareader.get_data_fred(
            ["CPIAUCNS", "GDP", "GDPC1"], start=start, end=end
        )
        if save_cache:
            file_dir = Path(data_dir) / "pulled"
            file_dir.mkdir(parents=True, exist_ok=True)
            # df.to_csv(file_dir / "fred_cpi.csv")
            df.to_parquet(file_dir / 'fred.parquet')

    # df.info()
    # df = pd.read_parquet(file_path)
    return df


def demo():
    df = load_fred()


if __name__ == "__main__":
    # Pull and save cache of fred data
    _ = load_fred(start="1913-01-01", end="2023-10-01", 
        data_dir=DATA_DIR, from_cache=False, save_cache=True)
