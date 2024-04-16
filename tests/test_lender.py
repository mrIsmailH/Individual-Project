import unittest
from housing_market_model import HousingMarketModel
from lender import Lender

class TestLender(unittest.TestCase):
    def setUp(self):
        model = HousingMarketModel()
        self.lender = Lender(model)
        
    def test_decide(self):
        #Test case 1: Tests if the loan request is approved when the request amount is less than the maximum loan amount
        self.assertTrue(self.lender.decide(loan_request=70000, house_price=100000, ltv_limit=0.8), "Test Case 1 Failed")

        #Test case 2: Tests if the loan request is approved when the request amount is equal to the maximum loan amount
        self.assertTrue(self.lender.decide(loan_request=80000, house_price=100000, ltv_limit=0.8), "Test Case 2 Failed")

        #Test case 3: Tests if the loan request is rejected when the request amount is more than the maximum loan amount that the lender can give
        self.assertFalse(self.lender.decide(loan_request=90000, house_price=100000, ltv_limit=0.8), "Test Case 3 Failed")

        #Test case 4: Tests if the loan request is rejected when the amount is more than the house price
        self.assertFalse(self.lender.decide(loan_request=150000, house_price=100000, ltv_limit=0.8), "Test Case 6 Failed")

if __name__ == '__main__':
    unittest.main(exit=False)
