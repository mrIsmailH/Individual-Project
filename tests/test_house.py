import unittest
from house import House
from housing_market_model import HousingMarketModel

class TestHouse(unittest.TestCase):
    def setUp(self):
        model = HousingMarketModel()
        self.house = House(model)

    def test_price(self):
        #Test 1: Tests that the price of the house is an integer
        self.assertIsInstance(self.house.price, int)

        #Test 2: Tests that the price of the house is within the expected range of 150000 to 300000
        self.assertTrue(150000 <= self.house.price <= 300000)

    def test_bedrooms(self):
        #Test 3: Tests that the number of bedrooms in the house is an integer
        self.assertIsInstance(self.house.bedrooms, int)

        #Test 4: Tests that the number of bedrooms in the house is within the expected range of 2 to 4
        self.assertTrue(2 <= self.house.bedrooms <= 4)


if __name__ == '__main__':
    unittest.main(exit=False)
