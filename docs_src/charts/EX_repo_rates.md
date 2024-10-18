{% include "_templates/chart_entry_top.md" %}

**Description:** This chat plots repo rates over time. It uses the Secured Overnight Financing Rate (SOFR), a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range. Since SOFR does not extend back further than 2017, we use the average repo rate in the triparty repo market whenever SOFR is unavailable.

**Interpretation:** SOFR is a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range.

**Direction of Risk:** When repo rates exceed the fed funds target range, risk is higher. Higher relative repo rates are likely more risky that lower relative rates.

**Formulas Used:** N/A

**Data Cleaning Information:** N/A

**What does this add that other charts might not?** It is helpful to visualize repo rates in the context of the fed fund's target range.



{% include "_templates/chart_entry_bottom.md" %}