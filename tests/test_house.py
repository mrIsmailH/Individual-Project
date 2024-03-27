import unittest
from main import House, HousingMarketModel

class TestHouse(unittest.TestCase):
    def setUp(self):
        self.model = HousingMarketModel()
        self.house = House(self.model)

    def test_setup(self):
        #Test case 1: Check if the price of the house is set up correctly
        self.assertTrue(isinstance(self.house.price, int), "Test Case 1 Failed")
        self.assertTrue(150000 <= self.house.price <= 300000, "Test Case 1 Failed")

if __name__ == '__main__':
    unittest.main(exit=False)
