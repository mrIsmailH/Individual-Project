import unittest
import time
from housing_market_model import HousingMarketModel

class TestSystem(unittest.TestCase):
    def test_extreme_values(self):
        #ExtremeValues1: Tests extreme values of more buyers than houses
        parameters = {'num_buyers': 1000, 'num_houses': 10, 'ltv_limit': 0.8}
        model = HousingMarketModel(parameters)
        model.setup()
        model.step()
        model.end()

        #ExtremeValues2: Tests extreme values of a high LTV limit
        parameters = {'num_buyers': 10, 'num_houses': 10, 'ltv_limit': 1.0}
        model = HousingMarketModel(parameters)
        model.setup()
        model.step()
        model.end()

        #ExtremeValues3: Tests extreme values of a low LTV limit
        parameters = {'num_buyers': 10, 'num_houses': 10, 'ltv_limit': 0.1}
        model = HousingMarketModel(parameters)
        model.setup()
        model.step()
        model.end()


    def test_runtime(self):
        #RunTime1: This test checks that the simulation runs within a reasonable time.
        start_time = time.time()
        model = HousingMarketModel(num_buyers=10, num_houses=10, ltv_limit=0.8)
        model.setup()
        model.step()
        model.end()
        end_time = time.time()
        self.assertTrue(end_time - start_time < 60)

    def test_randomness(self):
        #Randomness1: This test checks that the simulation produces different results with each time it is ran.
        model1 = HousingMarketModel(num_buyers=10, num_houses=10, ltv_limit=0.8)
        model1.setup()
        model1.step()
        model1.end()

        model2 = HousingMarketModel(num_buyers=10, num_houses=10, ltv_limit=0.8)
        model2.setup()
        model2.step()
        model2.end()

        self.assertNotEqual(model1, model2)

    def test_performance(self):
        #Performance1: This test checks that the simulation can handle large numbers of buyers and houses.
        model = HousingMarketModel(num_buyers=1000, num_houses=1000, ltv_limit=0.8)
        model.setup()
        model.step()
        model.end()

    def test_input_handling(self):
        #InputHandling1: This test checks that the simulation can handle invalid inputs.
        with self.assertRaises(ValueError):
            model = HousingMarketModel(num_buyers=-10, num_houses=10, ltv_limit=0.8)


if __name__ == '__main__':
    unittest.main(exit=False)
