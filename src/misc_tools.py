"""Collection of miscelaneous tools useful in a variety of situations
(not specific to the current project)
"""

import numpy as np
import pandas as pd
import polars as pl
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

from dateutil.relativedelta import relativedelta
import datetime


########################################################################################
## Pandas Helpers
########################################################################################


def df_to_literal(df, missing_value="None"):
    """Convert a pandas dataframe to a literal string representing the code to recreate it.

    Converts a pandas DataFrame into a string representation that can be used to
    recreate the DataFrame, including both data and index information. Missing values
    (NaN) are represented as None.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to convert to a literal string representation.

    Returns
    -------
    str
        A string representation of the DataFrame that can be used to recreate it.

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'Name': ['Alice', 'Bob', None],
    ...     'Age': [25, None, 35],
    ...     'City': ['New York', 'Los Angeles', 'Chicago']
    ... }, index=['a', 'b', 'c'])
    >>> print(df_to_literal(df))
    df = pd.DataFrame(
    {
        'Name': ['Alice', 'Bob', None],
        'Age': [25, None, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }, index=['a', 'b', 'c']
    )

    Notes
    -----
    The function preserves:
    - Column names and data
    - Index values (if not default RangeIndex)
    - None values (converted from NaN)
    """
    cols = df.to_dict("list")
    lines = []
    lines.append("df = pd.DataFrame(")
    lines.append("{")
    for idx, (col, values) in enumerate(cols.items()):
        line = f"    '{col}': {values}"
        if idx < len(cols) - 1:
            line += ","
        lines.append(line)
    lines.append("}")

    # Add index if it's not default RangeIndex
    if (
        not isinstance(df.index, pd.RangeIndex)
        or not (df.index == pd.RangeIndex(len(df))).all()
    ):
        index_values = list(df.index)
        lines[-1] += f", index={index_values}"

    lines.append(")")
    output = "\n".join(lines)
    # Replace 'nan' with None in the output string
    output = output.replace("nan", missing_value)
    return output


def merge_stats(df_left, df_right, on=[]):
    """Provide statistics to assess the completeness of the merge.

    To assess the completeness of the merge, this function counts the number of unique
    elements in the index of the left and right dataframes. It produces the following:

    (First, ensure that the index of left and right are sets of unique elements.)

    'union': num of elements in union of indices.
    'intersection': num of elements in intersection of indices
    'union-intersection': difference between union and intersection (unmatched symmetric)
    'intersection/union': percentage of symmetric matched
    'left': num of elements in left index
    'right': num of elements in in right index
    'left-intersection': number of excess elements in left index
    'right-intersection': number of excess elements in right index
    'intersection/left': percentage of matched based on total in left index
    'intersection/right': percentage of matched based on total in right index

    """
    left_index = df_left.set_index(on).index.unique()
    right_index = df_right.set_index(on).index.unique()
    union = left_index.union(right_index)
    intersection = left_index.intersection(right_index)
    stats = [
        "union",
        "intersection",
        "union-intersection",
        "intersection/union",
        "left",
        "right",
        "left-intersection",
        "right-intersection",
        "intersection/left",
        "intersection/right",
    ]
    df_stats = pd.Series(index=stats, dtype=int)
    df_stats["union"] = len(union)
    df_stats["intersection"] = len(intersection)
    df_stats["union-intersection"] = len(union) - len(intersection)
    df_stats["intersection/union"] = len(intersection) / len(union)
    df_stats["left"] = len(left_index)
    df_stats["right"] = len(right_index)
    df_stats["left-intersection"] = len(left_index) - len(intersection)
    df_stats["right-intersection"] = len(right_index) - len(intersection)
    df_stats["intersection/left"] = len(intersection) / len(left_index)
    df_stats["intersection/right"] = len(intersection) / len(right_index)
    return df_stats


def dataframe_set_difference(dff, df, library="pandas", show="rows_and_numbers"):
    """
    Gives the rows that appear in dff but not in df

    Example
    -------
    ```
    rows = data_frame_set_difference(dff, df)
    ```
    """
    if library == "pandas":
        # Reset index to ensure the row numbers are captured as a column
        # This is important for tracking the original row numbers after operations
        dff_reset = dff.reset_index().rename(columns={"index": "original_row_number"})
        df_reset = df.reset_index(drop=True)

        # Perform an outer merge with an indicator to identify rows present only in dff
        merged = dff_reset.merge(
            df_reset, how="left", indicator=True, on=dff.columns.tolist()
        )

        # Filter to rows only in dff (left_only)
        only_in_dff = merged[merged["_merge"] == "left_only"]

        # Extract the original row numbers of these rows
        row_numbers = only_in_dff["original_row_number"].tolist()
        ret = row_numbers

    elif library == "polars":
        # Assuming dff and df have the same schema (column names and types)
        assert dff.columns == df.columns

        # First, add a temporary column to each DataFrame with row numbers
        dff_with_index = dff.with_columns(pl.arange(0, dff.height).alias("row_number"))
        df_with_index = df.with_columns(
            pl.arange(0, df.height).alias("dummy_row_number")
        )

        # Perform an anti join to find rows in dff not present in df
        # Note: This requires the DataFrames to have columns to join on that define row uniqueness

        diff = dff_with_index.join(
            df_with_index, on=list(dff.columns), how="anti", join_nulls=True
        )

        # Extract the row numbers of the differing rows
        row_numbers = diff.select("row_number").to_series(0).to_list()
        ret = row_numbers

    else:
        raise ValueError("Unknown library")
    if show == "rows_and_numbers":
        rows = dff[row_numbers]
        ret = row_numbers, rows

    return ret


def freq_counts(df, col=None, with_count=True, with_cum_freq=True):
    """Like value_counts, but normalizes to give frequency
    Polars function
    df is a polars dataframe

    Example
    -------
    ```
    df.filter(
        (pl.col("fdate") > pl.datetime(2020,1,1)) &
        (pl.col("bus_dt") == pl.col("fdate"))
    ).pipe(freq_counts, col="bus_tenor_bin")
    ```
    """
    s = df[col]
    ret = (
        s.value_counts(sort=True)
        .with_columns(
            freq=pl.col("count") / s.shape[0] * 100,
        )
        .with_columns(cum_freq=pl.col("freq").cum_sum())
    )
    if not with_count:
        ret = ret.drop("count")
    if not with_cum_freq:
        ret = ret.drop("cum_freq")

    return ret


def move_column_inplace(df, col, pos=0):
    """
    https://stackoverflow.com/a/58686641

    Use pos=0 to move to the front
    """
    col = df.pop(col)
    df.insert(pos, col.name, col)


def move_columns_to_front(df, cols=[]):
    """Move a list of columns `cols` so that they appear first"""
    for col in cols[::-1]:
        move_column_inplace(df, col, pos=0)


def weighted_average(data_col=None, weight_col=None, data=None):
    """Simple calculation of weighted average.

    Examples
    --------
    ```
    >>> df_nccb = pd.DataFrame({
    ...     'rate': [2, 3, 2],
    ...     'start_leg_amount': [100, 200, 100]},
    ... )
    >>> weighted_average(data_col='rate', weight_col='start_leg_amount', data=df_nccb)
    2.5

    ```
    """

    def weights_function(row):
        return data.loc[row.index, weight_col]

    def wm(row):
        return np.average(row, weights=weights_function(row))

    result = wm(data[data_col])
    return result


def groupby_weighted_average(
    data_col=None,
    weight_col=None,
    by_col=None,
    data=None,
    transform=False,
    new_column_name="",
):
    """
    Faster method for calculating grouped weighted average.

    From:
    https://stackoverflow.com/a/44683506

    Examples
    --------

    ```
    >>> df_nccb = pd.DataFrame({
    ...     'trade_direction': ['RECEIVED', 'RECEIVED', 'DELIVERED'],
    ...     'rate': [2, 3, 2],
    ...     'start_leg_amount': [100, 200, 100]},
    ... )
    >>> groupby_weighted_average(data=df_nccb, data_col='rate', weight_col='start_leg_amount', by_col='trade_direction')
    trade_direction
    DELIVERED   2.00
    RECEIVED    2.67
    dtype: float64

    ```

    """
    data["_data_times_weight"] = data[data_col] * data[weight_col]
    data["_weight_where_notnull"] = data[weight_col] * pd.notnull(data[data_col])
    g = data.groupby(by_col)
    result = g["_data_times_weight"].sum() / g["_weight_where_notnull"].sum()
    del data["_data_times_weight"], data["_weight_where_notnull"]

    if transform:
        result.name = f"__{data_col}"
        result = data.merge(result.reset_index(), how="left", on=by_col)[
            f"__{data_col}"
        ]
        result.name = new_column_name

    return result


def groupby_weighted_std(
    data_col=None, weight_col=None, by_col=None, data=None, ddof=1
):
    """
    Method for calculating grouped weighted standard devation.

    From:
    https://stackoverflow.com/a/72915123

    Examples
    --------

    ```
    >>> df_nccb = pd.DataFrame({
    ...     'trade_direction': ['RECEIVED', 'RECEIVED', 'RECEIVED', 'RECEIVED',
    ...         'DELIVERED', 'DELIVERED', 'DELIVERED', 'DELIVERED'],
    ...     'rate': [2, 2, 2, 3, 2, 2, 2, 3],
    ...     'start_leg_amount': [300, 300, 300, 0, 200, 200, 200, 200]},
    ... )
    >>> groupby_weighted_std(data=df_nccb, data_col='rate', weight_col='start_leg_amount', by_col='trade_direction', ddof=1)
    trade_direction
    DELIVERED   0.50
    RECEIVED    0.00
    dtype: float64
    >>> np.std([2,2,2,3], ddof=1)
    0.5
    >>> np.std([2,2,2], ddof=1)
    0.0
    >>> groupby_weighted_std(data=df_nccb, data_col='rate', weight_col='start_leg_amount', by_col='trade_direction', ddof=0)
    trade_direction
    DELIVERED   0.43
    RECEIVED    0.00
    dtype: float64
    >>> np.std([2,2,2,3])
    0.4330127018922193
    >>> np.std([2,2,2])
    0.0

    ```

    """

    def weighted_sd(input_df):
        weights = input_df[weight_col]
        vals = input_df[data_col]

        weighted_avg = np.average(vals, weights=weights)

        numer = np.sum(weights * (vals - weighted_avg) ** 2)
        denom = ((vals.count() - ddof) / vals.count()) * np.sum(weights)

        return np.sqrt(numer / denom)

    return data.groupby(by_col).apply(weighted_sd)


def weighted_quantile(
    values, quantiles, sample_weight=None, values_sorted=False, old_style=False
):
    """Very close to numpy.percentile, but supports weights.

    Parameters
    ----------
    values:
        numpy.array with data
    quantiles :
        array-like with many quantiles needed
    sample_weight :
        array-like of the same length as `array`
    values_sorted : bool, Default False
        if True, then will avoid sorting of initial array
    old_style:
        if True, will correct output to be consistent with numpy.percentile.

    Returns
    -------
    numpy.array
        with computed quantiles.

    Notes
    -----
    quantiles should be in [0, 1]!

    FROM: https://stackoverflow.com/a/29677616

    NOTE: that a groupby weighted quantile can look like this:
    ```
    median_SD_spread = data.groupby('date').apply(
        lambda x: weighted_quantile(x['rate_SD_spread'], 0.5, sample_weight=x['Volume']))
    ```
    """
    values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    assert np.all(quantiles >= 0) and np.all(
        quantiles <= 1
    ), "quantiles should be in [0, 1]"

    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    if old_style:
        # To be convenient with numpy.percentile
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]
    else:
        weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)


_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*@#"


@np.vectorize
def calc_check_digit(number):
    """Calculate the check digits for the 8-digit cusip.
    This function is taken from
    https://github.com/arthurdejong/python-stdnum/blob/master/stdnum/cusip.py
    """
    # convert to numeric first, then sum individual digits
    number = "".join(
        str((1, 2)[i % 2] * _alphabet.index(n)) for i, n in enumerate(number)
    )
    return str((10 - sum(int(n) for n in number)) % 10)


def convert_cusips_from_8_to_9_digit(cusip_8dig_series):
    dig9 = calc_check_digit(cusip_8dig_series)
    new9 = cusip_8dig_series + dig9
    return new9


def _with_lagged_column_no_resample(
    df=None,
    columns_to_lag=None,
    id_columns=None,
    lags=1,
    # date_col="date",
    prefix="L",
):
    """This can be easily accomplished with the shift method. For example,

    ```
    df.groupby("id")["value"].shift(1)
    ```

    This function is
    to remind myself of this older method.
    """

    ## Old Method
    # all_dates = df[date_col].drop_duplicates().sort_values().reset_index(drop=True)
    # date_to_lag_date = pd.concat([all_dates, all_dates.shift(-lags)], axis=1)
    # date_to_lag_date.columns = [date_col, '_lagged_date']

    # sub_df = df[[date_col, *id_columns, *columns_to_lag]]
    # lag_sub_df = sub_df.merge(date_to_lag_date, on=[date_col])

    # for col in columns_to_lag:
    #     lag_sub_df = lag_sub_df.rename(columns={col: f'{prefix}{lags}_' + col})

    # lag_sub_df = lag_sub_df.drop(columns=[date_col])
    # lag_sub_df = lag_sub_df.rename(columns={'_lagged_date':date_col})

    ## New Method
    subsub_df = df.groupby(id_columns)[columns_to_lag].shift(lags)
    lag_sub_df = df.copy()
    for col in columns_to_lag:
        lag_sub_df[f"{prefix}{lags}_{col}"] = subsub_df[col]

    return lag_sub_df


def with_lagged_columns(
    df=None,
    column_to_lag=None,
    id_column=None,
    lags=1,
    date_col="date",
    prefix="L",
    freq=None,
    resample=True,
):
    """
    Add lagged columns to a dataframe, respecting frequency of the data.

    Examples
    --------

    ```
    >>> a=[
    ... ["A",'1990/1/1',1],
    ... ["A",'1990/2/1',2],
    ... ["A",'1990/3/1',3],
    ... ["B",'1989/12/1',12],
    ... ["B",'1990/1/1',1],
    ... ["B",'1990/2/1',2],
    ... ["B",'1990/3/1',3],
    ... ["B",'1990/4/1',4],
    ... ["B",'1990/6/1',6]]

    >>> df=pd.DataFrame(a,columns=['id','date','value'])
    >>> df['date']=pd.to_datetime(df['date'])

    >>> df
      id       date  value
    0  A 1990-01-01      1
    1  A 1990-02-01      2
    2  A 1990-03-01      3
    3  B 1989-12-01     12
    4  B 1990-01-01      1
    5  B 1990-02-01      2
    6  B 1990-03-01      3
    7  B 1990-04-01      4
    8  B 1990-06-01      6

    >>> df_lag = _with_lagged_column_no_resample(df=df, columns_to_lag=['value'], id_columns=['id'], lags=1)
    >>> df_lag
      id       date  value  L1_value
    0  A 1990-01-01      1       NaN
    1  A 1990-02-01      2      1.00
    2  A 1990-03-01      3      2.00
    3  B 1989-12-01     12       NaN
    4  B 1990-01-01      1     12.00
    5  B 1990-02-01      2      1.00
    6  B 1990-03-01      3      2.00
    7  B 1990-04-01      4      3.00
    8  B 1990-06-01      6      4.00

    The issue with leaving out the resample is that the lagged value
    for 1990-06-01 is 4.0, but it should be NaN. This is because the
    the value for group B in 1990-05-01 is missing.

    Rather, it should look like this:

    >>> df_lag = with_lagged_columns(df=df, column_to_lag='value', id_column='id', lags=1, freq="MS", resample=True)
    >>> df_lag
       id       date  value  L1_value
    2   A 1990-01-01   1.00       NaN
    4   A 1990-02-01   2.00      1.00
    6   A 1990-03-01   3.00      2.00
    8   A 1990-04-01    NaN      3.00
    1   B 1989-12-01  12.00       NaN
    3   B 1990-01-01   1.00     12.00
    5   B 1990-02-01   2.00      1.00
    7   B 1990-03-01   3.00      2.00
    9   B 1990-04-01   4.00      3.00
    11  B 1990-05-01    NaN      4.00
    13  B 1990-06-01   6.00       NaN

    ```

    Some valid frequencies are
    ```
    # "B": Business Day
    # "D": Calendar day
    # "W": Weekly
    # "ME": Month end
    # "BM": Business month end
    # "MS": Month start
    # "BMS": Business month start
    # "Q": Quarter end
    # "BQ": Business quarter end
    # "QS": Quarter start
    # "BQS": Business quarter start
    # "A" or "Y": Year end
    # "BA" or "BY": Business year end
    # "AS" or "YS": Year start
    # "BAS" or "BYS": Business year start
    # "H": Hourly
    # "T" or "min": Minutely
    # "S": Secondly
    # "L" or "ms": Milliseconds
    # "U": Microseconds
    # "N": Nanoseconds
    ```

    as seen here: https://business-science.github.io/pytimetk/guides/03_pandas_frequency.html

    """
    if resample:
        df_wide = df.pivot(index=date_col, columns=id_column, values=column_to_lag)
        new_col = f"{prefix}{lags}_{column_to_lag}"
        df_resampled = df_wide.resample(freq).last()
        df_lagged = df_resampled.shift(lags)
        df_lagged = df_lagged.stack(dropna=False).reset_index(name=new_col)
        df_lagged = df.merge(df_lagged, on=[date_col, id_column], how="right")
        df_lagged = df_lagged.dropna(subset=[column_to_lag, new_col], how="all")
        df_lagged = df_lagged.sort_values(by=[id_column, date_col])
    else:
        df_lagged = _with_lagged_column_no_resample(
            df=df,
            columns_to_lag=[column_to_lag],
            id_columns=[id_column],
            lags=lags,
            date_col=date_col,
            prefix=prefix,
        )

    return df_lagged


def leave_one_out_sums(df, groupby=[], summed_col=""):
    """
    Compute leave-one-out sums,

    $x_i = \\sum_{\\ell'\\neq\\ell} w_{i, \\ell'}$

    This is helpful for constructing the shift-share instruments
    in Borusyak, Hull, Jaravel (2022).

    Examples
    --------

    ```
    >>> df = pd.DataFrame({
    ...     'A' : ['foo', 'bar', 'foo', 'bar', 'foo', 'bar'],
    ...     'B' : ['one', 'one', 'one', 'two', 'two', 'two'],
    ...     'C' : [1, 5, 5, 2, 5, 3],
    ...     'D' : [2.0, 5., 8., 1., 2., 9.],
    ...     'LOO_Sum_C_groupby_B': [10, 6, 6, 8, 5, 7]
    ...                })
    >>> LOO_Sum_C_groupby_B = df.groupby(['B'])['C'].transform(lambda x: x.sum() - x)
    >>> pd.testing.assert_series_equal(
    ...     df['LOO_Sum_C_groupby_B'],
    ...     df.groupby(['B'])['C'].transform(lambda x: x.sum() - x),
    ...     check_names=False)

    >>> s = leave_one_out_sums(df, groupby=['B'], summed_col='C')
    >>> pd.testing.assert_series_equal(
    ...     df['LOO_Sum_C_groupby_B'],
    ...     s,
    ...     check_names=False)

    ```

    """
    s = df.groupby(groupby)[summed_col].transform(lambda x: x.sum() - x)
    return s


def get_most_recent_quarter_end(d):
    """
    Take a datetime and find the most recent quarter end date

    ```
    >>> d = pd.to_datetime('2019-10-21')
    >>> get_most_recent_quarter_end(d)
    datetime.datetime(2019, 9, 30, 0, 0)

    ```
    """
    quarter_month = (d.month - 1) // 3 * 3 + 1
    quarter_end = datetime.datetime(d.year, quarter_month, 1) - relativedelta(days=1)
    return quarter_end


def get_next_quarter_start(d):
    """
    Take a datetime and find the start date of the next quarter

    ```
    >>> d = pd.to_datetime('2019-10-21')
    >>> get_next_quarter_start(d)
    datetime.datetime(2020, 1, 1, 0, 0)

    ```
    """
    quarter_month = (d.month - 1) // 3 * 3 + 4
    years_to_add = quarter_month // 12
    quarter_month_mod = quarter_month % 12
    quarter_start = datetime.datetime(d.year + years_to_add, quarter_month_mod, 1)
    return quarter_start


def get_end_of_current_month(d):
    """
    Take a datetime and find the last date of the current month
    and also reset time to zero.

    ```
    >>> d = pd.to_datetime('2019-10-21')
    >>> get_end_of_current_month(d)
    Timestamp('2019-10-31 00:00:00')

    >>> d = pd.to_datetime('2023-03-31 12:00:00')
    >>> get_end_of_current_month(d)
    Timestamp('2023-03-31 00:00:00')

    ```

    From https://stackoverflow.com/a/13565185
    """
    # Reset tiem part of datetime to zero: https://stackoverflow.com/a/26883852
    d = pd.DatetimeIndex([d]).normalize()[0]

    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = d.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    end_of_current_month = next_month - datetime.timedelta(days=next_month.day)
    return end_of_current_month


def get_end_of_current_quarter(d):
    """
    Take a datetime and find the last date of the current quarter
    and also reset time to zero.

    ```
    >>> d = pd.to_datetime('2019-10-21')
    >>> get_end_of_current_quarter(d)
    datetime.datetime(2019, 12, 31, 0, 0)

    # TODO: Note that he behavior below may be unwanted. Might consider
    # fixing in the future
    >>> d = pd.to_datetime('2023-03-31 12:00:00')
    >>> get_end_of_current_quarter(d)
    datetime.datetime(2023, 3, 31, 0, 0)

    ```
    """
    quarter_start = get_next_quarter_start(d)
    quarter_end = quarter_start - datetime.timedelta(days=1)
    return quarter_end


def add_vertical_lines_to_plot(
    start_date,
    end_date,
    ax=None,
    freq="Q",
    adjust_ticks=True,
    alpha=0.1,
    extend_to_nearest_quarter=True,
):
    # start_date = '2019-09-10'
    # end_date = '2022-09-01'
    if extend_to_nearest_quarter:
        start_date = get_most_recent_quarter_end(start_date)
        end_date = get_next_quarter_start(end_date)
    if freq == "Q":
        dates = pd.date_range(
            pd.to_datetime(start_date),
            pd.to_datetime(end_date) + pd.offsets.QuarterBegin(1),
            freq="Q",
        )
        mask = (dates >= start_date) & (dates <= end_date)
        dates = dates[mask]
        months = mdates.MonthLocator((1, 4, 7, 10))
        if adjust_ticks:
            for d in dates:
                plt.axvline(d, color="k", alpha=alpha)
            ax.xaxis.set_major_locator(months)
        ax.xaxis.set_tick_params(rotation=90)
    else:
        raise ValueError


def plot_weighted_median_with_distribution_bars(
    data=None,
    variable_name=None,
    date_col="date",
    weight_col=None,
    percentile_bars=True,
    percentiles=[0.25, 0.75],
    rolling_window=1,
    rolling=False,
    rolling_min_periods=None,
    rescale_factor=1,
    ax=None,
    add_quarter_lines=True,
    ylabel=None,
    xlabel=None,
    label=None,
):
    """Plot the weighted median of a variable over time. Optionally, plot the 25th and 75th percentiles

    Examples
    --------

    ```
    ax = plot_weighted_median_with_distribution_bars(
            data=df,
            variable_name='rate_SD_spread',
            date_col='date',
            weight_col='Volume',
            percentile_bars=True,
            percentiles=[0.25, 0.75],
            rolling_window=5,
            rescale_factor=100,
            ax=None,
            add_quarter_lines=True,
            ylabel=None,
            xlabel=None,
            label='Median Spread'
            )
    plt.title('Volume-weighted median rate spread (bps)\nShaded region shows 25/75 percentiles')
    other_bbg['2019-10-21':].plot(ax=ax)
    plt.legend()

    fig, ax = plt.subplots()
    ax = plot_weighted_median_with_distribution_bars(
            data=df,
            variable_name='rate_SD_spread',
            date_col='date',
            weight_col='Volume',
            percentile_bars=True,
            percentiles=[0.25, 0.75],
            rolling_window=5,
            rescale_factor=100,
            ax=ax,
            add_quarter_lines=True,
            ylabel=None,
            xlabel=None,
            label=None
            )
    plt.title('Volume-weighted median rate spread (bps)\nShaded region shows 25/75 percentiles')
    other_bbg['2019-10-21':].plot(ax=ax)
    plt.legend()
    ```

    Notes
    -----
    rolling_window=1 means that there is no rolling aggregation applied.


    """
    if ax is None:
        plt.clf()
        _, ax = plt.subplots()

    median_series = data.groupby(date_col).apply(
        lambda x: weighted_quantile(x[variable_name], 0.5, sample_weight=x[weight_col])
    )
    if rolling:
        wavrs = median_series.rolling(
            rolling_window, min_periods=rolling_min_periods
        ).mean()
    else:
        wavrs = median_series
    (wavrs * rescale_factor).plot(ax=ax, label=label)

    if percentile_bars:
        lower = data.groupby(date_col).apply(
            lambda x: weighted_quantile(
                x[variable_name], percentiles[0], sample_weight=x[weight_col]
            )
        )
        upper = data.groupby(date_col).apply(
            lambda x: weighted_quantile(
                x[variable_name], percentiles[1], sample_weight=x[weight_col]
            )
        )
        if rolling:
            lower = lower.rolling(
                rolling_window, min_periods=rolling_min_periods
            ).mean()
            upper = upper.rolling(
                rolling_window, min_periods=rolling_min_periods
            ).mean()
        ax.plot(wavrs.index, lower * rescale_factor, color="tab:blue", alpha=0.1)
        ax.plot(wavrs.index, upper * rescale_factor, color="tab:blue", alpha=0.1)
        ax.fill_between(
            wavrs.index, lower * rescale_factor, upper * rescale_factor, alpha=0.2
        )

    if add_quarter_lines:
        start_date = data[date_col].min()
        end_date = data[date_col].max()
        add_vertical_lines_to_plot(
            start_date, end_date, ax=ax, freq="Q", adjust_ticks=True, alpha=0.05
        )
        ax.xaxis.set_tick_params(rotation=90)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    if ylabel is None:
        if rolling_window > 1:
            ylabel = f"{variable_name} ({rolling_window}-day ave.)"
        else:
            ylabel = f"{variable_name}"
    ax.set_ylabel(ylabel)

    if xlabel is not None:
        ax.set_xlabel(xlabel)

    plt.tight_layout()
    return ax


if __name__ == "__main__":
    pass
