import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats
import seaborn as sns
import pandas as pd

from interest_rates import merge_and_process_data
from rates_processing import extrapolate_rates


def plot_interest_rates(start_date, end_date):
    rates_data = merge_and_process_data(start_date, end_date)
    if rates_data is None:
        print("No data available for the given date range.")
        return
    
    # First plot "Historical Interest Rates" from Interest_rates.py
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.lineplot(data=rates_data)
    ax.set_title('Interest Rates')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate (%)')
    plt.show()

    # Second plot "Historical Interest Rates" from Interest_rates.py
    plt.figure(figsize=(15, 10))
    sns.boxplot(data=rates_data)
    plt.title("Box Plot of Interest Rates")
    plt.ylabel("Rate")
    plt.xticks(rotation=45)
    plt.show()


    # Third plot "Extrapolated Interest Rates" from rates_processing.py
    extrapolated_rates = extrapolate_rates(rates_data)
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.lineplot(data=extrapolated_rates)
    ax.set_title('Extrapolated Interest Rates')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate (%)')
    plt.show()

    # Fourth plot "Extrapolated Interest Rates" from rates_processing.py
    quarterly_discount = pd.DataFrame(columns=extrapolated_rates.columns, index=extrapolated_rates.index)
    for col in extrapolated_rates.columns:
        quarterly_discount[col] = extrapolated_rates[col].apply(lambda x: 1 / (1 + x / 100) ** (col / 4))
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.lineplot(data=quarterly_discount)
    ax.set_title('Quarterly Discount Factors')
    ax.set_xlabel('Date')
    ax.set_ylabel('Discount Factor')
    plt.show()

    # Fourth plot
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.boxplot(data=quarterly_discount)
    ax.set_title('Quarterly Discount Factors')
    ax.set_xlabel('Maturity')
    ax.set_ylabel('Discount Factor')
    plt.show()

    # Fifth plot histogram
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.histplot(data=quarterly_discount, kde=True)
    ax.set_title('Quarterly Discount Factors')
    ax.set_xlabel('Discount Factor')
    ax.set_ylabel('Frequency')
    plt.show()

    # Create a describe function that give us the statistics of the data
    print(quarterly_discount.describe())


if __name__ == "__main__":
    start_date = '2001-01-02'
    end_date = '2024-01-31'
    plot_interest_rates(start_date, end_date)


'''

    # First plot "Historical Interest Rates" from interest_rates.py
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.lineplot(data=rates_data)
    ax.set_title('Interest Rates')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate (%)')
    plt.show()

    # Second plot "Box Plot" from interest_rates.py
    plt.figure(figsize=(15, 10))
    sns.boxplot(data=rates_data)
    plt.title("Box Plot of Interest Rates")
    plt.ylabel("Rate")
    plt.xticks(rotation=45)
    plt.show()

    # Third plot "Historical Extrapolate Rate" from rates_processing.py
    extrapolated_rates = extrapolate_rates(rates_data)
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.lineplot(data=extrapolated_rates)
    ax.set_title('Extrapolated Interest Rates')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate (%)')
    plt.show()

    # Fourth plot "quarterly_discount" from rates_processing.py 
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.lineplot(data=quarterly_discount)
    ax.set_title('Quarterly Discount Factors')
    ax.set_xlabel('Date')
    ax.set_ylabel('Discount Factor')
    plt.show()

    # Fourth plot
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.boxplot(data=quarterly_discount)
    ax.set_title('Quarterly Discount Factors')
    ax.set_xlabel('Maturity')
    ax.set_ylabel('Discount Factor')
    plt.show()

    # Fifth plot histogram
    plt.figure(figsize=(15, 10))
    sns.set(style="whitegrid")
    ax = sns.histplot(data=quarterly_discount, kde=True)
    ax.set_title('Quarterly Discount Factors')
    ax.set_xlabel('Discount Factor')
    ax.set_ylabel('Frequency')
    plt.show()

    # Create a describe function that give us the statistics of the data
    print(quarterly_discount.describe())

if __name__ == "__main__":
    start_date = '2001-01-02'
    end_date = '2024-01-31'
    plot_interest_rates(start_date, end_date)

'''