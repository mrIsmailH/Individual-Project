import random
import agentpy as ap

#House Class
class House(ap.Agent):
    def setup(self):
        #Initialises the attributes of the house including the bedrooms
        self.price = random.randint(150000, 300000)
        self.bedrooms = random.randint(2, 4)  #Randomly assigns each house a number of bedrooms between 2 and 4
