import os
import pandas as pd
import unittest
from main import run_simulation, simulate

class TestMain(unittest.TestCase):
    def setUp(self):
        self.parameters = {
            'num_buyers': 5,
            'num_houses': 10,
            'wealth_range': (20000, 100000),
            'ltv_limit': 0.8,
        }
        self.plot_types = ['Scatter', 'Histogram']
        self.save_results = False 

    def test_run_simulation(self):
        #Test case 1: This tests if the 'simulate' method can be called without raising any exceptions
        #This is to make sure that the simulate method is implemented correctly and doesn't have any errors that would stop it from running
        try:
            successful_buyers, unsuccessful_buyers = simulate(self.parameters)
            run_simulation_works = True
        except Exception as e:
            run_simulation_works = False
            print(f"Exception: {e}")
        self.assertTrue(run_simulation_works, "Test Case 1 Failed")

        #Test case 2: This tests if the 'simulate' method returns two lists
        #This is to check that the simulate method is correctly returning the 'successful_buyers' and 'unsuccessful_buyers' lists
        self.assertIsInstance(successful_buyers, list, "Test Case 2 Failed")
        self.assertIsInstance(unsuccessful_buyers, list, "Test Case 2 Failed")


        #Test case 3: This tests if the 'simulate' method returns lists of tuples
        #This is to check that the simulate method is correctly appending tuples to the 'successful_buyers' and 'unsuccessful_buyers' lists
        self.assertTrue(all(isinstance(i, tuple) for i in successful_buyers), "Test Case 3 Failed")
        self.assertTrue(all(isinstance(i, tuple) for i in unsuccessful_buyers), "Test Case 3 Failed")

    def test_run_simulation_with_plots(self):
        #Test case 4: This tests if the 'run_simulation' method can be called with plot types without raising any exceptions
        try:
            self.plot_types = ['Scatter', 'Histogram']
            run_simulation(self.parameters, self.plot_types, self.save_results, test_mode=True)
            run_simulation_works = True
        except Exception as e:
            run_simulation_works = False
            print(f"Exception: {e}")
        self.assertTrue(run_simulation_works, "Test Case 4 Failed")

    def test_simulation_results_contents(self):
        #Test case 5: This tests if the 'simulation_results.xlsx' file contains the expected sheets
        if os.path.isfile('simulation_results.xlsx'):
            with pd.ExcelWriter('simulation_results.xlsx', engine='openpyxl', mode='a') as writer:
                sheet_names = writer.sheets.keys()
            expected_sheet_names = [f'Successful Buyers {i/10}' for i in range(1, 11)] + \
                                   [f'Unsuccessful Buyers {i/10}' for i in range(1, 11)] + \
                                   [f'Bids {i/10}' for i in range(1, 11)] + \
                                   [f'Loan Requests {i/10}' for i in range(1, 11)]
            self.assertTrue(all(name in sheet_names for name in expected_sheet_names), "Test Case 6 Failed")


if __name__ == '__main__':
    unittest.main(exit=False)
