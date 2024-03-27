import agentpy as ap
import random
import pandas as pd

class Homebuyer(ap.Agent):
    def setup(self):
        self.wealth = random.randint(20000, 100000)
        self.deposit = self.wealth
        self.unsuccessful_bids = []
        self.attempts = 0

class Lender(ap.Agent):
    def decide(self, loan_request, house_price, ltv_limit):
        max_loan = house_price * ltv_limit
        return loan_request <= max_loan

class House(ap.Agent):
    def setup(self):
        self.price = random.randint(150000, 300000)

class HousingMarketModel(ap.Model):
    def setup(self):
        self.buyers = ap.AgentList(self, self.p['num_buyers'], Homebuyer)
        self.lender = Lender(self)
        self.houses = ap.AgentList(self, self.p['num_houses'], House)
        self.transactions = []

    def step(self):

        for buyer in self.buyers:
            #Every buyer chooses a random house in the houses list to try to purchase
            if not self.houses:
                continue
            
            house = random.choice(self.houses)
            loan_request = house.price - buyer.deposit
            max_loan = house.price * self.p['ltv_limit']
            if self.lender.decide(loan_request, house.price, self.p['ltv_limit']):
                #If the loan is approved, the buyer buys the house
                self.transactions.append({ 
                    #A dictionary of the transaction is appended to the transactions list
                    'Buyer': buyer.id,
                    'House': house.id,
                    'Price': house.price,
                    'LTV': self.p['ltv_limit'],
                    'Deposit': buyer.deposit,
                    'Loan Amount': loan_request,
                    'Max Loan': max_loan,
                    'Successful': 1,
                    'Attempts': buyer.attempts
                })
                self.houses.remove(house)
                self.buyers.remove(buyer)
            else:
                #If the loan is not approved then the buyer is unsuccessful
                buyer.unsuccessful_bids.append({
                    #A dictionary of the unsuccessful transaction is added to the unsuccessful bids list
                    'House': house.id,
                    'Price': house.price,
                    'Max Loan': max_loan,
                    'Wealth': buyer.wealth,
                    'LTV Limit': self.p['ltv_limit'],
                    'Loan Request': loan_request
                })
                buyer.attempts += 1

    def end(self):
        #Record the unsuccessful buyers who didn't manage to buy a house after the simulation has finished
        for buyer in self.buyers:
            max_loan = max([house.price * self.p['ltv_limit'] for house in self.houses])
            self.transactions.append({
                #If the buyer was unsuccessful then they are added the the transactions list as unsuccessful
                'Buyer': buyer.id,
                'House': 0,
                'Price': 0,
                'LTV': 0,
                'Deposit': 0,
                'Loan Amount': 0,
                'Max Loan': max_loan,
                'Successful': 0,
                'Attempts': buyer.attempts
            })
        self.buyers.clear()  # Remove all buyers
        self.houses.clear() 

#This method is used to run the simulation
def run_simulation(num_buyers, num_houses, ltv_limit):
    parameters = {
        #Three parameters are taken by this function
        'num_buyers': num_buyers,
        'num_houses': num_houses,
        'ltv_limit': ltv_limit,
    }
    model = HousingMarketModel(parameters) #An instance is created of the Housing Market Model
    model.run(24)  #Run the simulation for 24 months
    transactions_df = pd.DataFrame(model.transactions)
    print("Transactions:")
    print(transactions_df)
    print("\nUnsuccessful bids:")
    for buyer in model.buyers:
        if buyer.unsuccessful_bids:
            print('')
            print(f"Buyer {buyer.id} (LTV {model.p['ltv_limit']}, Wealth/Deposit: {buyer.wealth}):")
            print('')
            print(pd.DataFrame(buyer.unsuccessful_bids).drop(columns=['Wealth', 'LTV Limit']))

    #A Pandas DataFrame is created from the transactions list, this is then printed to the terminal


#This is the block of code that is executed when the main.py class is run
if __name__ == "__main__":
    run_simulation(7, 60, 0.6)

