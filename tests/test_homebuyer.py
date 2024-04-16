import unittest
from housing_market_model import HousingMarketModel

class TestHomebuyer(unittest.TestCase):
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

    def test_wealth(self):
        #Test 1: Test that wealth is within the expected range
        self.assertTrue(20000 <= self.homebuyer.wealth <= 100000)

    def test_deposit(self):
        #Test 2: Test that deposit is equal to wealth
        self.assertEqual(self.homebuyer.deposit, self.homebuyer.wealth)

    def test_bids_made(self):
        #Test 3: Test that the number of bids made by the homebuyer is initialized to 0 at the start
        self.assertEqual(self.homebuyer.bids_made, 0)

    def test_bids_won(self):
        #Test 4: Test that the number of bids won by the homebuyer is initialized to 0 at the start
        self.assertEqual(self.homebuyer.bids_won, 0)

    def test_loans_requested(self):
        #Test 5: Test that the number of loans requested by the homebuyer is initialized to 0 at the start
        self.assertEqual(self.homebuyer.loans_requested, 0)

    def test_loans_rejected(self):
        #Test 6: Test that the number of loans rejected for the homebuyer is initialized to 0 at the start
        self.assertEqual(self.homebuyer.loans_rejected, 0)

    def test_ltv(self):
        #Test 7: Test that the LTV attribute is initialized to 0
        self.assertEqual(self.homebuyer.ltv, 0)

    def test_bid_on_any_house_after_10_steps(self):
        #Test 8: Test that the homebuyer bids on any house after 10 steps
        self.model.t = 11
        initial_bids_made = self.homebuyer.bids_made
        self.model.step()
        self.assertTrue(self.homebuyer.bids_made > initial_bids_made)

    def test_wealth_range(self):
        #Test 9 : Test that the homebuyer's wealth is within range
        self.assertTrue(self.parameters['wealth_range'][0] <= self.homebuyer.wealth <= self.parameters['wealth_range'][1])

    
if __name__ == '__main__':
    unittest.main(exit=False)
