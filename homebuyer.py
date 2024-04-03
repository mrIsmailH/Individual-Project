import random
import agentpy as ap

#Homebuyer Class
class Homebuyer(ap.Agent):
    def setup(self, wealth_range=(20000, 100000)):
        #Initialise all variables for each Homebuyer including their bedroom preference
        self.wealth = random.randint(*wealth_range)
        self.deposit = self.wealth
        self.bids_made = 0
        self.bids_won = 0
        self.loans_requested = 0
        self.loans_rejected = 0
        self.ltv = 0
        self.bedroom_pref = random.randint(2, 4)
