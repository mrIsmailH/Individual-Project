import unittest
from agentpy import AgentList
from housing_market_model import HousingMarketModel
from lender import Lender

class TestHousingMarketModel(unittest.TestCase):
    def setUp(self):
        parameters = {
            'num_buyers': 10,
            'num_houses': 10,
            'wealth_range': (20000, 100000),
            'ltv_limit': 0.8,
        }

        self.model = HousingMarketModel(parameters)
        self.model.setup() 
        self.homebuyer = self.model.buyers[0]  
        
    def test_setup(self):
        #Test 1: Tests that the 'buyers' agent is an instance of AgentList
        self.assertIsInstance(self.model.buyers, AgentList)

        #Test 2: Tests that the 'lender' is an instance of Lender
        self.assertIsInstance(self.model.lender, Lender)

        #Test 3: Tests that the 'houses' agent is an instance of AgentList
        self.assertIsInstance(self.model.houses, AgentList)

        #Test 4: Tests that the 'successful_buyers' attribute is an empty list
        self.assertEqual(self.model.successful_buyers, [])

        #Test 5: Tests that the 'unsuccessful_buyers' attribute is an empty list
        self.assertEqual(self.model.unsuccessful_buyers, [])

        #Test 6: Tests that the 'LoanRequests' attribute is an empty list
        self.assertEqual(self.model.LoanRequests, [])

        #Test 7: Tests that the 'bids' attribute is an empty list
        self.assertEqual(self.model.bids, [])

        #Test 8: Tests that the number of buyers matches up to the 'num_buyers' parameter
        self.assertEqual(len(self.model.buyers), self.model.p['num_buyers'])

        #Test 9: Tests that the number of houses matches up to the 'num_houses' parameter
        self.assertEqual(len(self.model.houses), self.model.p['num_houses'])

    def test_step(self):
        initial_num_buyers = len(self.model.buyers)
        initial_num_houses = len(self.model.houses)

        self.model.step()

        #Test 10: Tests that the 'step' method can be called without raising any exceptions
        #If an exception is raised, the test will fail
        try:
            self.model.step()
        except Exception as e:
            self.fail(f"model.step() raised {type(e).__name__} unexpectedly!")

        #Test 11: Tests that the number of buyers and houses decreases or stays the same after each step
        self.assertTrue(len(self.model.buyers) <= initial_num_buyers)
        self.assertTrue(len(self.model.houses) <= initial_num_houses)

        #Tets 12: Tests that the 'bids' list has data entries after each step
        self.assertTrue(len(self.model.bids) > 0)

        #Test 13: Tests that the 'successful_buyers' list has data entries after each step
        self.assertTrue(len(self.model.successful_buyers) > 0)

        #Test 14: Tests that the 'LoanRequests' list has data entries after each step
        self.assertTrue(len(self.model.LoanRequests) > 0)

    def test_end(self):
        self.model.end()

        #Test 15: Tests that the 'end' method can be called without raising any exceptions
        #If an exception is raised, the test will fail.
        try:
            self.model.end()
        except Exception as e:
            self.fail(f"model.end() raised {type(e).__name__} unexpectedly!")
            
        #Test 16: Tests that all buyers and houses are removed when the end method is called
        self.assertEqual(len(self.model.buyers), 0)
        self.assertEqual(len(self.model.houses), 0)

        #Test 17: Tests that the 'unsuccessful_buyers' list is populated with data entries after the end method is called
        self.assertTrue(len(self.model.unsuccessful_buyers) > 0)

if __name__ == '__main__':
    unittest.main(exit=False)
