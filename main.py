import agentpy as ap
import random
from matplotlib.widgets import TextBox, Button
import pandas as pd
from reacton import display
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#Homebuyer Class
class Homebuyer(ap.Agent):
    def setup(self):
        #Initialise all variables for each Homebuyer
        self.wealth = random.randint(20000, 100000)
        self.deposit = self.wealth
        self.bids_made = 0
        self.bids_won = 0
        self.loans_requested = 0
        self.loans_rejected = 0
        self.ltv = 0

#Lender Class
class Lender(ap.Agent):
    def decide(self, loan_request, house_price, ltv_limit):
        #This class decides whether a loan is accepted or rejected based on the loan amount and LTV limit
        max_loan = house_price * ltv_limit
        return loan_request <= max_loan

#House Class
class House(ap.Agent):
    def setup(self):
        #Initialises the attributes of the house
        self.price = random.randint(150000, 300000)

#Housing Model  Class
class HousingMarketModel(ap.Model):
    def setup(self):
        #Initialises all the agents in the simulation as well as the data structures to store the simulation results
        self.buyers = ap.AgentList(self, self.p['num_buyers'], Homebuyer)
        self.lender = Lender(self)
        self.houses = ap.AgentList(self, self.p['num_houses'], House)
        self.successful_buyers = []
        self.unsuccessful_buyers = []
        self.LoanRequests = []
        self.bids = []  # New table to record all bids

    def step(self):
        #This method is responsible for modelling the interactions between all agents at each time step

        if not self.houses:
            return

        #An auction is held for each house
        for house in self.houses:
            highest_bid = 0
            highest_bidder = None

            for buyer in self.buyers:
                #Homebuyers submit their bid on a house
                bid = min(house.price, buyer.deposit * 0.9)
                buyer.bids_made += 1

                #The bid details are added to the bids list
                self.bids.append({
                    'Buyer ID': buyer.id,
                    'House ID': house.id,
                    'Bid Amount': bid,
                    'Time Step': self.t,
                })


                #Checks if this bid is the highest bid so far
                if bid > highest_bid:
                    highest_bid = bid
                    highest_bidder = buyer

            #If no buyer could make a bid then the simulation moves on to the next house
            if highest_bidder is None:
                continue

            #This is an English auction so the winning bid is the same as the price paid
            winning_bid = highest_bid
            price_paid = winning_bid

            #The bids won is incremented as the highest bidder has won an auction
            highest_bidder.bids_won += 1

            #The bid is recorded and the auction won status is updated
            for bid in self.bids:
                if bid['Buyer ID'] == highest_bidder.id and bid['House ID'] == house.id:
                    bid['Auction Won'] = 'Yes'
                else:
                    bid['Auction Won'] = "No"

            #Checks if the winner of the auction is able to get a loan
            loan_request = house.price - price_paid
            highest_bidder.ltv = loan_request / house.price  # Calculate LTV

            if self.lender.decide(loan_request, house.price, self.p['ltv_limit']):
                ##if the lender decides to give the loan then the transaction is successful and the buyer buys the house
                highest_bidder.bids_won += 1
                highest_bidder.loans_requested += 1
                self.successful_buyers.append({
                    'Buyer ID': highest_bidder.id,
                    'House ID': house.id,
                    'Auction Won': 'Yes',
                    'Loan Accepted': 'Yes',
                    'Time Step': self.t,
                    'Bids Made': highest_bidder.bids_made,
                    'Loans Requested': highest_bidder.loans_requested,
                    'Wealth': highest_bidder.wealth,
                    'LTV': highest_bidder.ltv,
                })
                self.LoanRequests.append({
                    'Buyer ID': highest_bidder.id,
                    'House ID': house.id,
                    'Wealth': highest_bidder.wealth,
                    'House Value': house.price,
                    'Amount Paid': price_paid,
                    'Loan Required': loan_request,
                    'Current LTV Limit': self.p['ltv_limit'],
                    'Loan Status': 'Accepted',
                    'Time Step': self.t,
                })
                self.houses.remove(house)
                self.buyers.remove(highest_bidder)
            else:
                #If the lender does not accept the loan then the transaction is unsuccessful and the buyer remains in the market.
                highest_bidder.loans_rejected += 1
                self.LoanRequests.append({
                    'Buyer ID': highest_bidder.id,
                    'House ID': house.id,
                    'Wealth': highest_bidder.wealth,
                    'House Value': house.price,
                    'Amount Paid': price_paid,
                    'Loan Required': loan_request,
                    'Current LTV Limit': self.p['ltv_limit'],
                    'Loan Status': 'Rejected',
                    'Time Step': self.t,
                })

    def end(self):
    #At the end of the simulation if there are still buyers remaining they are unsuccessful
        for buyer in self.buyers:
            LoanRequests = len([request for request in self.LoanRequests if request['Buyer ID'] == buyer.id])
            bids_made = len([bid for bid in self.bids if bid['Buyer ID'] == buyer.id])
            self.unsuccessful_buyers.append({
                'Buyer ID': buyer.id,
                'Bids Made': bids_made,
                'Bids Won': buyer.bids_won,
                'Loans Requested': LoanRequests,
                'Wealth': buyer.wealth,
            })
        self.buyers.clear()  #Remove all buyers from the simulation
        self.houses.clear() 


# This method runs the simulation with a set of parameters
def run_simulation(num_buyers, num_houses):
    #Initialize the lists to store the results of successful and unsuccessful buyers
    successful_buyers = []
    unsuccessful_buyers = []
    
    #Loop over a range of LTV limits from 0.1 to 1.0
    for ltv_limit in np.arange(0.1, 1.01, 0.1):
        #parameters are defined as a dictionary
        parameters = {
            'num_buyers': num_buyers,
            'num_houses': num_houses,
            'ltv_limit': ltv_limit,
        }
        
        # Create an instance of HousingMarketModel with the parameters
        model = HousingMarketModel(parameters)
        
        #Run the model for 24 months
        model.run(24)

        #Get the number of successful and unsuccessful buyers
        successful = len(model.successful_buyers)
        unsuccessful = len(model.unsuccessful_buyers)

        #Append the simulation results to the lists
        successful_buyers.append((ltv_limit, successful))
        unsuccessful_buyers.append((ltv_limit, unsuccessful))

        #Create Dataframes for successful and unsuccessful buyers as well as a dataframe to hold the loan request details and bids details
        successful_buyers_df = pd.DataFrame(model.successful_buyers)
        unsuccessful_buyers_df = pd.DataFrame(model.unsuccessful_buyers)
        bids_df = pd.DataFrame(model.bids)  # Create a DataFrame for the bids
        loanrequests_df = pd.DataFrame(model.LoanRequests)

        #Prints All Data Frames to the terminal
        print("\nCURRENT LTV LIMIT:")
        print(ltv_limit)
        print("\nSuccessful Buyers:")
        print(successful_buyers_df)
        print("\nUnsuccessful Buyers:")
        print(unsuccessful_buyers_df)
        print("\nBids:")
        print(bids_df) 
        print("\nLoanRequests:")
        print(loanrequests_df) 


    #Return the results
    return successful_buyers, unsuccessful_buyers

#Create a figure and a subplot
fig, ax = plt.subplots()

#Create two text boxes for the parameters of Homebuyers and Homes
text_box1 = TextBox(plt.axes([0.3, 0.9, 0.1, 0.05]), 'Homebuyers')
text_box2 = TextBox(plt.axes([0.5, 0.9, 0.1, 0.05]), 'Homes')

#Create a button for running the simulation when clicked
button = Button(plt.axes([0.7, 0.9, 0.1, 0.05]), 'Run')

#This method defines what happens when the button is clicked
def on_button_clicked(event):
    #The parameters are fetched from the text boxes
    num_buyers = int(text_box1.text)
    num_houses = int(text_box2.text)
    
    #The simulation is run with the parameters from the textboxes
    successful_buyers, unsuccessful_buyers = run_simulation(num_buyers, num_houses)
    
    #Clear the current plot
    ax.clear()
    
    #Plot the results on a scatter graph
    ax.scatter(*zip(*successful_buyers), color='green', label='Successful Buyers')
    ax.scatter(*zip(*unsuccessful_buyers), color='red', label='Unsuccessful Buyers')

    ax.set_xlabel('LTV')
    ax.set_ylabel('Count')

    ax.legend()
    plt.draw()

#This connects the method to the button.
button.on_clicked(on_button_clicked)
  

if __name__ == "__main__":
    plt.show()
