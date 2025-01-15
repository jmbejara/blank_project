from pathlib import Path
from settings import config

OUTPUT_DIR = config("OUTPUT_DIR")
DATA_DIR = config("DATA_DIR")
START_DATE = config("START_DATE")

from datetime import datetime

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pull_public_repo_data

pull_public_repo_data.series_descriptions

##################################
## Format series
##################################

df = pull_public_repo_data.load_all(data_dir=DATA_DIR)
df = df.loc[START_DATE:, :]

df["target_midpoint"] = (df["DFEDTARU"] + df["DFEDTARL"]) / 2
df["SOFR_less_IORB"] = df["SOFR"] - df["Gen_IORB"]

df["Fed Balance Sheet over GDP"] = df["WALCL"] / df["GDP"].ffill()
df["Tri-Party less Fed ON_RRP Rate"] = (
    df["REPO-TRI_AR_OO-P"] - df["RRPONTSYAWARD"]
) * 100
df["Tri-Party Rate Less Fed Funds Upper Limit"] = (
    df["REPO-TRI_AR_OO-P"] - df["DFEDTARU"]
) * 100
df["Tri-Party Rate Less Fed Funds Midpoint"] = (
    df["REPO-TRI_AR_OO-P"] - (df["DFEDTARU"] + df["DFEDTARL"]) / 2
) * 100

df["net_fed_repo"] = (
    df["RPONTSYD"] - df["RRPONTSYD"]
) / 1000  # Fed Repo minus reverse repo volume
df["Total Reserves over Currency"] = (
    df["TOTRESNS"] / df["CURRCIR"]
)  # total reserves among depository institutions vs currency in circulation
df["Total Reserves over GDP"] = df["TOTRESNS"] / df["GDP"]

df["SOFR_extended_with_Triparty"] = df["SOFR"].fillna(df["REPO-TRI_AR_OO-P"])

new_labels = {
    "REPO-TRI_AR_OO-P": "Tri-Party Overnight Average Rate",
    "RRPONTSYAWARD": "ON-RRP Facility Rate",
    "Gen_IORB": "Interest on Reserves",
    "DFEDTARU": "Fed Funds Target Upper",
    "DFEDTARL": "Fed Funds Target Lower",
}
df = df.rename(columns=new_labels)

## Rates Relative to Fed Funds Target Midpoint
df_norm = pd.DataFrame().reindex_like(df[["target_midpoint"]])
df_norm[["target_midpoint"]] = 0

for s in [
    "Fed Funds Target Upper",
    "Fed Funds Target Lower",
    "Tri-Party Overnight Average Rate",
    "EFFR",
    "target_midpoint",
    "Interest on Reserves",
    "ON-RRP Facility Rate",
    "SOFR",
    "SOFR_extended_with_Triparty",
    "FNYR-BGCR-A",
    "FNYR-TGCR-A",
]:
    df_norm[s] = df[s] - df["target_midpoint"]


## Other columns that need to be included
cols = [
    "Total Reserves over Currency", 
    "Total Reserves over GDP",
    "Fed Balance Sheet over GDP",
]
for col in cols:
    df_norm[col] = df[col]

df_formatted = df.copy()
df_norm_formatted = df_norm.copy()
df_formatted.columns = df.columns.str.replace("-", "_").str.replace(" ", "_")
df_norm_formatted.columns = df_norm.columns.str.replace("-", "_").str.replace(" ", "_")

col_name_to_short_name = {
    # "GDP": "",
    # "CPIAUCNS": "",
    # "GDPC1": "",
    # "DPCREDIT": "",
    # "EFFR": "",
    # "OBFR": "",
    # "SOFR": "",
    # "IORR": "",
    # "IOER": "",
    # "IORB": "",
    "Fed_Funds_Target_Upper": "Fed Funds Target Upper",
    "Fed_Funds_Target_Lower": "Fed Funds Target Lower",
    # "WALCL": "",
    # "TOTRESNS": "",
    # "TREAST": "",
    # "CURRCIR": "",
    # "GFDEBTN": "",
    # "WTREGEN": "",
    "ON_RRP_Facility_Rate": "ON-RRP Facility Rate",
    # "RRPONTSYD": "",
    # "RPONTSYD": "",
    # "WSDONTL": "",
    "Interest_on_Reserves": "Interest on Reserves",
    # "ONRRP_CTPY_LIMIT": "",
    # "ONRP_AGG_LIMIT": "",
    # "Tri_Party_Overnight_Average_Rate": "",
    # "REPO_TRI_TV_OO_P": "",
    # "REPO_TRI_TV_TOT_P": "",
    # "REPO_DVP_AR_OO_P": "",
    # "REPO_DVP_TV_OO_P": "",
    # "REPO_DVP_TV_TOT_P": "",
    # "REPO_DVP_OV_TOT_P": "",
    # "REPO_GCF_AR_OO_P": "",
    # "REPO_GCF_TV_OO_P": "",
    # "REPO_GCF_TV_TOT_P": "",
    # "FNYR_BGCR_A": "",
    # "FNYR_TGCR_A": "",
    # "target_midpoint": "",
    # "SOFR_less_IORB": "",
    "Fed_Balance_Sheet_over_GDP": "Fed Balance Sheet / GDP",
    # "Tri_Party_less_Fed_ON_RRP_Rate": "",
    # "Tri_Party_Rate_Less_Fed_Funds_Upper_Limit": "",
    # "Tri_Party_Rate_Less_Fed_Funds_Midpoint": "",
    # "net_fed_repo": "",
    # "Total_Reserves_over_Currency": "",
    "Total_Reserves_over_GDP": "Total Reserves / GDP",
    "SOFR_extended_with_Triparty": "SOFR (extended with Tri-Party)",
}
df_formatted.index.name = "date"
df_norm_formatted.index.name = "date"

filepath = DATA_DIR / "repo_public.parquet"
df_formatted.to_parquet(filepath)
filepath = DATA_DIR / "repo_public.xlsx"
df_formatted.to_excel(filepath)

filepath = DATA_DIR / "repo_public_relative_fed.parquet"
df_norm_formatted.to_parquet(filepath)

filepath = DATA_DIR / "repo_public_relative_fed.xlsx"
df_norm_formatted.to_excel(filepath)

df = df_formatted.rename(columns=col_name_to_short_name)
df_norm = df_norm_formatted.rename(columns=col_name_to_short_name)

##################################
## Chart Unnormalized spikes
##################################

## Matplotlib
fig, ax = plt.subplots()
ax.fill_between(
    df.index, df["Fed Funds Target Upper"], df["Fed Funds Target Lower"], alpha=0.5
)
df[["SOFR (extended with Tri-Party)", "EFFR"]].plot(ax=ax)

## Plotly
fig = make_subplots()
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Fed Funds Target Lower"],
        name="Fed Funds Target Lower",
        mode="lines",
        line=dict(color="rgba(0, 0, 255, 0.08)"),
    )
)
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Fed Funds Target Upper"],
        name="Fed Funds Target Upper",
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(0, 0, 255, 0.08)",
        line=dict(color="rgba(0, 0, 255, 0.08)"),
    )
)
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["SOFR (extended with Tri-Party)"],
        name="SOFR (extended with Tri-Party)",
        mode="lines",
    )
)
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["EFFR"],
        name="EFFR",
        mode="lines",
    )
)
# # Add range slider
# fig.update_layout(
#     xaxis=dict(
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1,
#                      label="1m",
#                      step="month",
#                      stepmode="backward"),
#                 dict(count=6,
#                      label="6m",
#                      step="month",
#                      stepmode="backward"),
#                 dict(count=1,
#                      label="YTD",
#                      step="year",
#                      stepmode="todate"),
#                 dict(count=1,
#                      label="1y",
#                      step="year",
#                      stepmode="backward"),
#                 dict(step="all")
#             ])
#         ),
#         rangeslider=dict(
#             visible=True
#         ),
#         type="date"
#     )
# )

start_date = "2015-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')
fig.update_xaxes(type="date", range=[start_date, end_date])
fig.update_layout(title_text="Repo Rates and the Fed Funds Rate")
fig.update_yaxes(title_text="Percent")
fig.write_html(OUTPUT_DIR / "repo_rates.html", include_plotlyjs="cdn")

##################################
## Normalized repo rates plot
##################################

## Matplotlib
fig, ax = plt.subplots()
date_start = "2014-Aug"
date_end = "2019-Dec"
_df = df_norm.loc[date_start:, :].copy()

ax.fill_between(
    _df.index, _df["Fed Funds Target Upper"], _df["Fed Funds Target Lower"], alpha=0.2
)
_df[
    [
        "SOFR (extended with Tri-Party)",
        "EFFR",
        "Interest on Reserves",
        "ON-RRP Facility Rate",
    ]
].rename(columns=new_labels).plot(ax=ax)
plt.ylim(-0.4, 1.0)
plt.ylabel("Spread of federal feds target midpoint (percent)")
arrowprops = dict(arrowstyle="->")
ax.annotate(
    "Sep. 17, 2019: 3.06%",
    xy=("2019-Sep-17", 0.95),
    xytext=("2017-Oct-27", 0.9),
    arrowprops=arrowprops,
)


## Plotly
# fig = go.Figure(layout=layout)
fig = make_subplots()
# Add traces
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["Fed Funds Target Lower"],
        name="Fed Funds Target Lower",
        mode="lines",
        line=dict(color="rgba(0, 0, 255, 0.08)"),
    )
)
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["Fed Funds Target Upper"],
        name="Fed Funds Target Upper",
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(0, 0, 255, 0.08)",
        line=dict(color="rgba(0, 0, 255, 0.08)"),
    )
)
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["SOFR (extended with Tri-Party)"],
        name="SOFR (extended with Tri-Party)",
        mode="lines",
    )
)
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["EFFR"],
        name="EFFR",
        mode="lines",
    )
)

# layout = go.Layout(
#     yaxis=dict(
#         range=[date_start, date_end]
#     ),
#     xaxis=dict(
#         range=[-0.2, 0.3]
#     )
# )
start_date = "2015-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')
fig.update_xaxes(type="date", range=[start_date, end_date])
fig.update_yaxes(range=[-0.2, 0.2])
fig.update_layout(title_text="Rates Relative to Fed Funds Target Midpoint")
fig.update_yaxes(title_text="Percent Less Midpoint")
fig.write_html(OUTPUT_DIR / "repo_rates_normalized.html", include_plotlyjs="cdn")


##################################
## Normalized plot with GDP line
##################################

## Matplotlib
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

date_start = "2016-Jan"
date_end = None

_df = df_norm.loc[date_start:date_end, :].copy()
_df = _df[
    [
        "SOFR (extended with Tri-Party)",
        # "FNYR-BGCR-A",
        # 'EFFR',
        # "FNYR-BGCR-A",
        # "FNYR-TGCR-A",
        "Interest on Reserves",
        "ON-RRP Facility Rate",
        "Fed Funds Target Upper",  # Fed Funds Upper Limit
        "Fed Funds Target Lower",  # Fed Funds Lower Limit
    ]
].rename(columns=new_labels)

ax1.fill_between(
    _df.index, _df["Fed Funds Target Upper"], _df["Fed Funds Target Lower"], alpha=0.1
)

cols = [
    "SOFR (extended with Tri-Party)",
    # "FNYR-BGCR-A",
    # 'EFFR',
    # "FNYR-BGCR-A",
    # "FNYR-TGCR-A",
    "Interest on Reserves",
    "ON-RRP Facility Rate",
]
_df[cols].plot(ax=ax1)
plt.ylim(-0.4, 1.0)
plt.ylabel("Rate relative to Federal Funds target midpoint (percent)")
arrowprops = dict(arrowstyle="->")
ax1.annotate(
    "Sep. 17, 2019: 3.06%",
    xy=("2019-Sep-17", 0.95),
    xytext=("2020-Oct-27", 0.9),
    arrowprops=arrowprops,
)

_df.loc[date_start:date_end, "Fed Balance Sheet / GDP"] = df_norm.loc[date_start:date_end, "Fed Balance Sheet / GDP"]
_df.loc[date_start:, ["Fed Balance Sheet / GDP"]].plot(
    ax=ax2, color="black", alpha=0.75
)

ax1.set_ylabel("Basis Points")
ax2.set_ylabel("Ratio")
ax1.set_ylim([-0.2, 0.4])
ax2.set_ylim([0.10, 0.4])
ax2.legend("")
plt.title("Black line is Fed Balance Sheet / GDP")


## Plotly
# _df = df_norm.loc[date_start:date_end, :].copy()
# _df = _df[
#     [
#         "SOFR (extended with Tri-Party)",
#         "Fed Funds Target Upper",
#         "Fed Funds Target Lower",
#         # "FNYR-BGCR-A",
#         # "FNYR-TGCR-A",
#         "Interest on Reserves",
#         "ON-RRP Facility Rate",
#     ]
# ]
# fig = go.Figure(layout=layout)
fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["Fed Funds Target Lower"],
        name="Fed Funds Target Lower (left)",
        mode="lines",
        line=dict(color="rgba(0, 0, 255, 0.08)"),
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["Fed Funds Target Upper"],
        name="Fed Funds Target Upper (left)",
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(0, 0, 255, 0.08)",
        line=dict(color="rgba(0, 0, 255, 0.08)"),
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["SOFR (extended with Tri-Party)"],
        name="SOFR (extended with Tri-Party) (left)",
        mode="lines",
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["Interest on Reserves"],
        name="Interest on Reserves (left)",
        mode="lines",
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["ON-RRP Facility Rate"],
        name="ON-RRP Facility Rate (left)",
        mode="lines",
    ),
    secondary_y=False,
)
# fig.update_yaxes(range=[0.2, 0.2])
fig.add_trace(
    go.Scatter(
        x=_df.index,
        y=_df["Fed Balance Sheet / GDP"],
        name="Fed Balance Sheet / GDP (right)",
        mode="lines",
    ),
    secondary_y=True,
)
# layout = go.Layout(
#     yaxis=dict(
#         range=[date_start, date_end]
#     ),
#     xaxis=dict(
#         range=[-0.2, 0.3]
#     )
# )
start_date = "2016-01-01"
end_date = datetime.today().strftime("%Y-%m-%d")
fig.update_xaxes(type="date", range=[start_date, end_date])
# fig.update_yaxes(range=[0.2, 0.2])
fig.update_layout(
    title_text="Rates Relative to Fed Funds Target Midpoint against Fed Balance Sheet"
)
fig.update_yaxes(title_text="Percent Less Midpoint", secondary_y=False)
fig.update_yaxes(title_text="Ratio", secondary_y=True)
fig.write_html(
    OUTPUT_DIR / "repo_rates_normalized_w_balance_sheet.html", include_plotlyjs="cdn"
)

