import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats
import seaborn as sns
import pandas as pd

import cds_processing
from cds_processing import calc_cds_monthly

cds_monthly = calc_cds_monthly()
cds_monthly.set_index('Date', inplace=True)

def cds_spread_plot(start_date, end_date):
    cds_data = cds_monthly
    if cds_data is None:
        print("No data available for the given date range.")
        return
    
    # First plot "Historical CDS spreads" 
    if isinstance(cds_monthly.index[0], str):
        cds_monthly.index = pd.to_datetime(cds_monthly.index)
    
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    
    ax = sns.lineplot(data=cds_monthly)
    
    ax.set_title('CDS spread by portfolio')
    ax.set_xlabel('Date')
    ax.set_ylabel('CDS spread')
    yearly_ticks = pd.date_range(start=cds_monthly.index.min(), end=cds_monthly.index.max(), freq='YS')
    ax.set_xticks(yearly_ticks)
    ax.set_xticklabels([t.strftime('%Y') for t in yearly_ticks])
    #plt.xticks(rotation=90)
    plt.show()

    # Second plot "Box plot of CDS spreads"
    plt.figure(figsize=(15, 10))
    sns.boxplot(data=cds_data)
    plt.title("Box Plot of CDS spread by portfolio")
    plt.ylabel("CDS spread")
    #plt.xticks(rotation=90)
    plt.show()

    # Create a describe function that give us the statistics of the data
    print(cds_monthly.describe())


if __name__ == "__main__":
    start_date = '2001-01-02'
    end_date = '2024-01-31'
    cds_spread_plot(start_date, end_date)

