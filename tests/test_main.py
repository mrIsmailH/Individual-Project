import unittest
from main import run_simulation
class TestMain(unittest.TestCase):
    def setUp(self):
        self.num_buyers = 7
        self.num_houses = 60

    def test_run_simulation(self):
        #Test case 1: This tests if the 'run_simulation' method can be called without raising any exceptions
        #This is to make sure that the run_simulation method is implemented correctly and doesn't have any errors that would stop it from running
        try:
            successful_buyers, unsuccessful_buyers = run_simulation(self.num_buyers, self.num_houses)
            run_simulation_works = True
        except Exception as e:
            run_simulation_works = False
            print(f"Exception: {e}")
        self.assertTrue(run_simulation_works, "Test Case 1 Failed")

        #Test case 2: This tests if the 'run_simulation' method returns two lists
        #This is to check that the run_simulation method is correctly returning the 'successful_buyers' and 'unsuccessful_buyers' lists
        self.assertIsInstance(successful_buyers, list, "Test Case 2 Failed")
        self.assertIsInstance(unsuccessful_buyers, list, "Test Case 2 Failed")

        #Test case 3: This tests if the 'run_simulation' method returns lists of tuples
        #This is to check that the run_simulation method is correctly appending tuples to the 'successful_buyers' and 'unsuccessful_buyers' lists
        self.assertTrue(all(isinstance(i, tuple) for i in successful_buyers), "Test Case 3 Failed")
        self.assertTrue(all(isinstance(i, tuple) for i in unsuccessful_buyers), "Test Case 3 Failed")

if __name__ == '__main__':
    unittest.main(exit=False)
