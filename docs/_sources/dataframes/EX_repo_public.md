# `EX_repo_public` - Public Repo Data


## Description

This dataframe contains, among other things,repo rates and the Federal Funds target range. The shaded area shows the Federal Funds target range. During 2019, the Secured Overnight Financing Rate (SOFR), a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range. Since SOFR does not extend back further than 2017, we use the average repo rate in the triparty repo market whenever SOFR is unavailable.


## Data Dictionary

- **DATE**: `datetime64[ns]`
- **GDP**: `float64` US Nominal GDP
- **CPIAUCNS**: `float64` Consumer Price Index for All Urban Consumers: All Items in U.S. City Average https://fred.stlouisfed.org/series/CPIAUCNS
- **GDPC1**: `float64`  Real Gross Domestic Product 
- **DPCREDIT**: `float64`  Discount Window Primary Credit Rate
- **EFFR**: `float64` Effective Federal Funds Rate
- **OBFR**: `float64` Overnight Bank Funding Rate 
- **SOFR**: `float64` Secured Overnight Financing Rate
- **IORR**: `float64` Interest Rate on Required Reserves (IORR Rate) (DISCONTINUED)
- **IOER**: `float64` Interest Rate on Excess Reserves (IOER Rate) (DISCONTINUED)
- **IORB**: `float64` Interest Rate on Reserve Balances (IORB Rate)
- **Fed_Funds_Target_Upper**: `float64`
- **Fed_Funds_Target_Lower**: `float64`
- **WALCL**: `float64` Assets: Total Assets: Total Assets (Less Eliminations from Consolidation): Wednesday Level 
- **TOTRESNS**: `float64` Reserves of Depository Institutions: Total 
- **TREAST**: `float64` Assets: Securities Held Outright: U.S. Treasury Securities: All: Wednesday Level
- **CURRCIR**: `float64` Currency in Circulation
- **GFDEBTN**: `float64` Federal Debt: Total Public Debt
- **WTREGEN**: `float64` Liabilities and Capital: Liabilities: Deposits with F.R. Banks, Other Than Reserve Balances: U.S. Treasury, General Account: Week Average
- **ON_RRP_Facility_Rate**: `float64` Overnight Reverse Repo Facility Rate
- **RRPONTSYD**: `float64` Overnight Reverse Repurchase Agreements: Treasury Securities Sold by the Federal Reserve in the Temporary Open Market Operations
- **RPONTSYD**: `float64` Overnight Repurchase Agreements: Treasury Securities Purchased by the Federal Reserve in the Temporary Open Market Operations 
- **WSDONTL**: `float64` Memorandum Items: Securities Lent to Dealers: Overnight Facility: Wednesday Level
- **Interest_on_Reserves**: `float64` IORB rate, backfilled with IOER reserves when IORB is not available.
- **ONRRP_CTPY_LIMIT**: `float64` Overnight Reverse Repo Facility Counterparty Limits
- **ONRP_AGG_LIMIT**: `float64` Standing Repo Facility (SRF) aggregate limit, not updated since late 2023
- **Tri_Party_Overnight_Average_Rate**: `float64`
- **REPO_TRI_TV_OO_P**: `float64` Triparty overnight transaction volume
- **REPO_TRI_TV_TOT_P**: `float64` Triparty transaction volume on all repos
- **REPO_DVP_AR_OO_P**: `float64` DVP average rate on overnight repos
- **REPO_DVP_TV_OO_P**: `float64` DVP transaction volume on overnight repos
- **REPO_DVP_TV_TOT_P**: `float64` DVP transaction volume on all repos
- **REPO_DVP_OV_TOT_P**: `float64` DVP outstanding volume on all repos  
- **REPO_GCF_AR_OO_P**: `float64` GCF average rate on overnight repos
- **REPO_GCF_TV_OO_P**: `float64` GCF transaction volume on overnight repos
- **REPO_GCF_TV_TOT_P**: `float64` GCF transaction volume on all repos
- **FNYR_BGCR_A**: `float64` Federal Reserve Bank of New York Reference Rates. Broad General Collateral Rate
- **FNYR_TGCR_A**: `float64` Federal Reserve Bank of New York Reference Rates. Tri-Party General Collateral Rate
- **target_midpoint**: `float64` Fed Funds target midpoint
- **SOFR_less_IORB**: `float64` SOFR less interest on reserve balances (backfilled with IOER)
- **Fed_Balance_Sheet_over_GDP**: `float64` Size of Fed's balance sheet divided by nominal GDP
- **Tri_Party_less_Fed_ON_RRP_Rate**: `float64` Triparty average rate less the Fed's overnight reverse repurchase agreement facility awared rate
- **Tri_Party_Rate_Less_Fed_Funds_Upper_Limit**: `float64` Triparty average rate less the Fed Fund's target upper limit
- **Tri_Party_Rate_Less_Fed_Funds_Midpoint**: `float64` Triparty average rate less the Fed Fund's target range midpoint
- **net_fed_repo**: `float64` `RPONTSYD - RRPONTSYD`, Fed's total repos minus Fed's reverse repos
- **Total_Reserves_over_Currency**: `float64` Reserves of Depository Institutions: Total, divided by currency in circulation
- **Total_Reserves_over_GDP**: `float64` Reserves of Depository Institutions: Total, divided by nominal GDP
- **SOFR_extended_with_Triparty**: `float64` SOFR only goes back to around 2017. Before then, I use the average triparty repo rate to backfill.




## Dataframe Specs

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
| Data available up to (min)     | 2024-07-01 00:00:00                                                             |
| Data available up to (max)     | 2025-01-24 00:00:00                                                             |
| Download Data as Parquet       | [Parquet](../download_dataframe/EX_repo_public.parquet)            |
| Download Data as Excel         | [Excel](../download_dataframe/EX_repo_public.xlsx)                 |
| Linked Charts                  |   [EX_repo_rates](../charts/EX_repo_rates.md)<br>   |

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
