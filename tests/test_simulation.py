import unittest

from main import HousingMarketModel

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.parameters = {
            'num_buyers': 10,
            'num_houses': 5,
            'ltv_limit': 0.8
        }
        self.model = HousingMarketModel(self.parameters)
        self.model.setup()

def test_extreme_values(self):
    #More buyers than houses
    self.parameters['num_buyers'] = 1000
    self.parameters['num_houses'] = 1
    self.model = HousingMarketModel(self.parameters)
    self.model.run(24)
   

    #High LTV limit
    self.parameters['ltv_limit'] = 0.99
    self.model = HousingMarketModel(self.parameters)
    self.model.run(24)
  

    #Low LTV limit
    self.parameters['ltv_limit'] = 0.01
    self.model = HousingMarketModel(self.parameters)
    self.model.run(24)

if __name__ == '__main__':
    unittest.main(exit=False)
