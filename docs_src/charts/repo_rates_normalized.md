
**Description:** This chat plots repo rates relative the midpoint of the Federal Funds target range. The shaded area shows the Federal Funds target range. During 2019, the Secured Overnight Financing Rate (SOFR), a broad measure of the cost of borrowing cash overnight collateralized by Treasury securities via repurchase agreements, often exceeded the upper limit of the Federal Funds target range. Since SOFR does not extend back further than 2017, we use the average repo rate in the triparty repo market whenever SOFR is unavailable.

**Relevance for Financial Stability:** When SOFR exceeds the upper limit of the Federal Funds target range,
this is indicative of a relative scarcity of liquidity in short term funding markets.

**Direction of Risk:** When repo rates exceed the fed funds target range, risk is higher. Higher relative repo rates are likely more risky that lower relative rates.

**Formulas Used:**

```{math}
\begin{align*}
midpoint &= (upper\_limit - lower\_limit)/2 \\
relative\_rate &= rate - midpoint
\end{align*}
```

**Data Cleaning Information:** N/A

**Relation to a chart in an OFR public monitor:** N/A

**What does this add that other charts might not?** Repo rates must be measured in relative terms, here relative the prevailing Fed Funds target, to assess risk in short-term funding markets.


