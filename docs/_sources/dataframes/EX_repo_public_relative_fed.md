# `EX_repo_public_relative_fed` - Public Repo Data, Relative to the Fed Funds Target Midpoint


## Description

This dataframe contains, among other things,repo rates relative the midpoint of the Federal Funds target range. The shaded area shows the Federal Funds target range. During 2019, the Secured Overnight Financing Rate (SOFR), a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range. Since SOFR does not extend back further than 2017, we use the average repo rate in the triparty repo market whenever SOFR is unavailable.

## Data Dictionary

- **DATE**: `datetime64[ns]`
- **target_midpoint**: `float64`
- **Fed_Funds_Target_Upper**: `float64` Upper limit rate less the Fed's target midpoint rate
- **Fed_Funds_Target_Lower**: `float64` Lower limit rate less the Fed's target midpoint rate
- **Tri_Party_Overnight_Average_Rate**: `float64` Triparty average rate less the Fed's target midpoint rate
- **EFFR**: `float64` Effective federal funds rate, less the Fed's target midpoint rate
- **Interest_on_Reserves**: `float64` Interest on reserve balances (backfilled with interest on excess reserves) rate, less the Fed's target midpoint rate
- **ON_RRP_Facility_Rate**: `float64` O/N Reserve Repurchase agreement facility rate, less the Fed's target midpoint rate
- **SOFR**: `float64` SOFR, less the Fed's target midpoint rate
- **SOFR_extended_with_Triparty**: `float64` SOFR, backfilled with the average triparty rate, less the Fed's target midpoint rate
- **FNYR_BGCR_A**: `float64` Broad General Collateral Rate, less the Fed's target midpoint rate
- **FNYR_TGCR_A**: `float64` Triparty general collateral rate, less the Fed's target midpoint rate
- **Total_Reserves_over_Currency**: `float64` Reserves of Depository Institutions: Total, divided by currency in circulation
- **Total_Reserves_over_GDP**: `float64` Reserves of Depository Institutions: Total, divided by nominal GDP
- **Fed_Balance_Sheet_over_GDP**: `float64` Size of Fed's balance sheet divided by nominal GDP




## Dataframe Specs

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
| Data available up to (min)     | 2024-07-01 00:00:00                                                             |
| Data available up to (max)     | 2025-01-24 00:00:00                                                             |
| Download Data as Parquet       | [Parquet](../download_dataframe/EX_repo_public_relative_fed.parquet)            |
| Download Data as Excel         | [Excel](../download_dataframe/EX_repo_public_relative_fed.xlsx)                 |
| Linked Charts                  |   [EX_repo_rates_normalized](../charts/EX_repo_rates_normalized.md)<br>  [EX_repo_rates_normalized_w_balance_sheet](../charts/EX_repo_rates_normalized_w_balance_sheet.md)<br>   |

## Pipeline Specs

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
