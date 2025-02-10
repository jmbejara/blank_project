---
date: 2025-02-10 00:55:32
tags: FRED, Office of Financial Research
category: Short Term Funding, Repo
---

# Chart: Repo Rates
SOFR, the Effective Funds Rate, and the Fed's Target Range

```{raw} html
<iframe src="../_static/EX_repo_rates.html" height="500px" width="100%"></iframe>
```
[Full Screen Chart](../download_chart/EX_repo_rates.html)


**Description:** This chat plots repo rates over time. It uses the Secured Overnight Financing Rate (SOFR), a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range. Since SOFR does not extend back further than 2017, we use the average repo rate in the triparty repo market whenever SOFR is unavailable.

**Relevance for Financial Stability:** SOFR is a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range.

**Direction of Risk:** When repo rates exceed the fed funds target range, risk is higher. Higher relative repo rates are likely more risky that lower relative rates.

**Formulas Used:** N/A

**Data Cleaning Information:** N/A

**Relation to a chart in an OFR public monitor:** N/A

**What does this add that other charts might not?** It is helpful to visualize repo rates in the context of the fed fund's target range.





| Chart Name             | Repo Rates                                             |
|------------------------|------------------------------------------------------------|
| Chart ID               | repo_rates                                               |
| Topic Tags             | Short Term Funding, Repo                                |
| Data Series Start Date | 2/29/2012                                 |
| Data Frequency         | Daily                                         |
| Observation Period     | Weekday                                     |
| Lag in Data Release    | One day                                    |
| Data Release Date(s)   | Weekday                                     |
| Seasonal Adjustment    | None                                    |
| Units                  | Percent                                                  |
| Data Series            |                                             |
| HTML Chart             | [HTML](../download_chart/EX_repo_rates.html)    |

## Data

| Dataframe Name                 | Public Repo Data                                                   |
|--------------------------------|--------------------------------------------------------------------------------------|
| Dataframe ID                   | [EX_repo_public](../dataframes/EX_repo_public.md)                       |
| Data Sources                   | FRED, Office of Financial Research                                        |
| Data Providers                 | FRED, Office of Financial Research                                      |
| Links to Providers             | https://fred.stlouisfed.org/, https://www.financialresearch.gov/short-term-funding-monitor/api/                             |
| Topic Tags                     | Short Term Funding, Repo                                          |
| Type of Data Access            | Public                                              |
| Data License                   | No                                                     |
| License Expiration Date        | N/A                                          |
| Contact Provider Before Use?   | No                                         |
| Provider Contact Information   |                                             |
| Restrictions on Use of Data    | No                                               |
| How is data pulled?            | Web API via Python                                                    |
| Data available up to (min)     |                                                              |
| Data available up to (max)     |                                                              |
| Download Data as Parquet       | [Parquet](../download_dataframe/EX_repo_public.parquet)            |
| Download Data as Excel         | [Excel](../download_dataframe/EX_repo_public.xlsx)                 |
| Linked Charts                  |   [EX_repo_rates](../charts/EX_repo_rates.md)<br>   |

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