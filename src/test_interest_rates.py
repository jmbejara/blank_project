import unittest
import pandas as pd
from datetime import datetime
from interest_rates import pull_fred_data, process_fed_data, fetch_yield_curve_data, load_rates, merge_and_process_data


'''
This test case class tests the functions in the Interest_rates.py file.

'''

class TestInterestRates(unittest.TestCase):

    def test_pull_fred_data(self):
        start_date = '2020-01-01'
        end_date = '2020-01-31'
        data = pull_fred_data(start_date, end_date)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)

    def test_process_fed_data(self):
        start_date = '2020-01-01'
        end_date = '2020-01-31'
        data = process_fed_data(start_date, end_date)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertIn('3', data.columns)
        self.assertIn('6', data.columns)

    def test_fetch_yield_curve_data(self):
        url = "https://www.federalreserve.gov/data/yield-curve-tables/feds200628_1.html"
        data = fetch_yield_curve_data(url)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)

    def test_load_rates(self):
        data = load_rates()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)

    def test_merge_and_process_data(self):
        start_date = '2020-01-01'
        end_date = '2020-01-31'
        data = merge_and_process_data(start_date, end_date)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

