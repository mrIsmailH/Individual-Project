import unittest
from main import Lender, HousingMarketModel

class TestLender(unittest.TestCase):
    def setUp(self):
        model = HousingMarketModel()
        self.lender = Lender(model)

    def test_decide(self):
        #Test case 1: loan_request is less than max_loan
        self.assertTrue(self.lender.decide(loan_request=70000, house_price=100000, ltv_limit=0.8), "Test Case 1 Failed")

        #Test case 2: loan_request is equal to max_loan
        self.assertTrue(self.lender.decide(loan_request=80000, house_price=100000, ltv_limit=0.8), "Test Case 2 Failed")

        #Test case 3: loan_request is more than max_loan
        self.assertFalse(self.lender.decide(loan_request=90000, house_price=100000, ltv_limit=0.8), "Test Case 3 Failed")

        #Test case 4: loan_request is more than house price
        self.assertFalse(self.lender.decide(loan_request=150000, house_price=100000, ltv_limit=0.8), "Test Case 6 Failed")

if __name__ == '__main__':
    unittest.main(exit=False)
