
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

