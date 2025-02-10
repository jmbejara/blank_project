---
date: 2025-02-10 00:55:32
tags: FRED, Office of Financial Research
category: Short Term Funding, Repo, Monetary Policy
---

# Chart: Repo Rate Spikes and the Fed's Balance Sheet
Repo rate spikes relative to the size of the Fed's balance sheet.

```{raw} html
<iframe src="../_static/EX_repo_rates_normalized_w_balance_sheet.html" height="500px" width="100%"></iframe>
```
[Full Screen Chart](../download_chart/EX_repo_rates_normalized_w_balance_sheet.html)


**Description:** This chat plots repo rates relative the midpoint of the Federal Funds target range. The shaded area shows the Federal Funds target range. During 2019, the Secured Overnight Financing Rate (SOFR), a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range. This chart also shows the ratio of the size of the Fed's balance sheet to US GDP. Since SOFR does not extend back further than 2017, we use the average repo rate in the triparty repo market whenever SOFR is unavailable.

**Relevance for Financial Stability:** When SOFR exceeds the upper limit of the Federal Funds target range,
this is indicative of a relative scarcity of liquidity in short term funding markets.
The size of the Fed's balance sheet relative to the GDP gives a broad measure of the supply of money in the economy. This chart suggests that spikes in repo markets were more common when the relative supply of money was lower. It also demonstrates that, as of 2024 as the growth of the Fed's balance sheet is slowing, repo rates relative to the Fed Funds's target midpoint are increasing.

**Direction of Risk:** When repo rates exceed the fed funds target range, risk is higher. Higher relative repo rates are likely more risky that lower relative rates.

**Formulas Used:**

```{math}
\begin{align*}
midpoint &= (upper\_limit - lower\_limit)/2 \\
relative\_rate &= rate - midpoint \\
balance\_sheet\_ratio &= balance\_sheet / GDP
\end{align*}
```

**Data Cleaning Information:** N/A

**Relation to a chart in an OFR public monitor:** N/A

**What does this add that other charts might not?** Repo rates must be measured in relative terms, here relative the prevailing Fed Funds target, to assess risk in short-term funding markets.





| Chart Name             | Repo Rate Spikes and the Fed's Balance Sheet                                             |
|------------------------|------------------------------------------------------------|
| Chart ID               | repo_rates_normalized_w_balance_sheet                                               |
| Topic Tags             | Short Term Funding, Repo, Monetary Policy                                |
| Data Series Start Date | 2/29/2012                                 |
| Data Frequency         | Daily                                         |
| Observation Period     | Weekday                                     |
| Lag in Data Release    | One day                                    |
| Data Release Date(s)   | Weekday                                     |
| Seasonal Adjustment    | None                                    |
| Units                  | Percent (left) and Ratio (right)                                                  |
| Data Series            |                                             |
| HTML Chart             | [HTML](../download_chart/EX_repo_rates_normalized_w_balance_sheet.html)    |

## Data

| Dataframe Name                 | Public Repo Data, Relative to the Fed Funds Target Midpoint                                                   |
|--------------------------------|--------------------------------------------------------------------------------------|
| Dataframe ID                   | [EX_repo_public_relative_fed](../dataframes/EX_repo_public_relative_fed.md)                       |
| Data Sources                   | FRED, Office of Financial Research                                        |
| Data Providers                 | FRED, Office of Financial Research                                      |
| Links to Providers             | NA                             |
| Topic Tags                     | Short Term Funding, Repo                                          |
| Type of Data Access            | Public                                              |
| Data License                   | No                                                     |
| License Expiration Date        |                                           |
| Contact Provider Before Use?   | No                                         |
| Provider Contact Information   |                                             |
| Restrictions on Use of Data    | No                                               |
| How is data pulled?            | Web API via Python                                                    |
| Data available up to (min)     |                                                              |
| Data available up to (max)     |                                                              |
| Download Data as Parquet       | [Parquet](../download_dataframe/EX_repo_public_relative_fed.parquet)            |
| Download Data as Excel         | [Excel](../download_dataframe/EX_repo_public_relative_fed.xlsx)                 |
| Linked Charts                  |   [EX_repo_rates_normalized](../charts/EX_repo_rates_normalized.md)<br>  [EX_repo_rates_normalized_w_balance_sheet](../charts/EX_repo_rates_normalized_w_balance_sheet.md)<br>   |

## Pipeline

| Pipeline Name                   | Pipeline Template - Example                       |
|---------------------------------|--------------------------------------------------------|
| Pipeline ID                     | [EX](../index.md)              |
| Lead Pipeline Developer         | Jeremiah Bejarano             |
| Contributors                    | Jeremiah Bejarano, John Doe           |
| Bitbucket Repo URL              | https://github.com/jmbejara/blank_project                        |
| Pipeline Web Page               | <a href="https://github.com/jmbejara/blank_project">https://github.com/jmbejara/blank_project</a>      |
| Date of Last Code Update        | 2025-02-10 00:55:32           |
| Runs on Linux, Windows, Both, or Other? |Windows/Linux/MacOS|
| Linked Dataframes               |  [EX_repo_public](../dataframes/EX_repo_public.md)<br>  [EX_repo_public_relative_fed](../dataframes/EX_repo_public_relative_fed.md)<br>  |


In addition to the `requirements.txt` and `r_requirements.txt`, the pipeline code relies
on first loading modules using the following command:
```
module load anaconda3/3.11.4 TeXLive/2023 R/4.4.0 pandoc/3.1.6 gcc/14.1.0 stata/17
```