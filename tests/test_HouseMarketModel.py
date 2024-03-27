import unittest
from main import HousingMarketModel, Lender
import agentpy as ap


class TestHousingMarketModel(unittest.TestCase):
    def setUp(self):
        #Define the parameters for the HousingMarketModel
        self.parameters = {
            'num_buyers': 7,
            'num_houses': 60,
            'ltv_limit': 0.8
        }
        self.model = HousingMarketModel(self.parameters)
        self.model.setup()  # Call the setup method

    def test_setup(self):
        #Test case 1: Check if the model has a 'buyers' attribute
        print(f"Buyers: {self.model.buyers}")
        self.assertTrue(hasattr(self.model, 'buyers'), "Test Case 1 Failed")

        #Test case 2: Check if the model has a 'houses' attribute
        print(f"Houses: {self.model.houses}")
        self.assertTrue(hasattr(self.model, 'houses'), "Test Case 2 Failed")

    def test_step(self):
        #Test case 3: Check if the 'step' method can be called without raising an exception
        try:
            self.model.step()
            step_works = True
        except Exception as e:
            step_works = False
            print(f"Exception: {e}")
        self.assertTrue(step_works, "Test Case 3 Failed")

        #Test case 4: Check if the number of buyers and houses decreases after calling the 'step' method
        print(f"Buyers after step: {self.model.buyers}")
        print(f"Houses after step: {self.model.houses}")
        self.assertTrue(len(self.model.buyers) <= self.parameters['num_buyers'], "Test Case 4 Failed")
        self.assertTrue(len(self.model.houses) <= self.parameters['num_houses'], "Test Case 4 Failed")

    def test_end(self):
        #Test case 5: Check if the 'end' method can be called without raising an exception
        try:
            self.model.end()
            end_works = True
        except Exception as e:
            end_works = False
            print(f"Exception: {e}")
        self.assertTrue(end_works, "Test Case 5 Failed")

        #Test case 6: Check if all buyers and houses are removed after calling the 'end' method
        print(f"Buyers after end: {self.model.buyers}")
        print(f"Houses after end: {self.model.houses}")
        self.assertEqual(len(self.model.buyers), 0, "Test Case 6 Failed")
        self.assertEqual(len(self.model.houses), 0, "Test Case 6 Failed")

if __name__ == '__main__':
    unittest.main(exit=False)
