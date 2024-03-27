import unittest
from main import Homebuyer, HousingMarketModel

class TestHomebuyer(unittest.TestCase):
    def setUp(self):
        model = HousingMarketModel() 
        self.homebuyer = Homebuyer(model)


    def test_setup(self):
        #Test case 1: Check that wealth is within the expected range
        self.assertTrue(20000 <= self.homebuyer.wealth <= 100000)
        print(f'Wealth is within the expected range. {self.homebuyer.wealth}')
        #Test case 2: Check that deposit is equal to wealth
        self.assertEqual(self.homebuyer.deposit, self.homebuyer.wealth)
        print('Deposit is equal to wealth')
        #Test case 3: Check if unsuccessful_bids is an empty list
        self.assertEqual(self.homebuyer.unsuccessful_bids, [])
        print('Wealth is within the expected range.')
        #Test case 4: Checks if the attempts is initialized to 0
        self.assertEqual(self.homebuyer.attempts, 0)
        print('Attempts are initialised at 0')

if __name__ == '__main__':
    unittest.main(exit=False)

