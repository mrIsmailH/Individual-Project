import agentpy as ap
import random
from matplotlib.widgets import CheckButtons, RadioButtons, TextBox, Button
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

#Housing Model Class
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

            #Checks if the winner of the auction is able to get a loan
            loan_request = house.price - price_paid
            highest_bidder.ltv = loan_request / house.price  #Calculate the LTV

            if self.lender.decide(loan_request, house.price, self.p['ltv_limit']):
                #if the lender decides to give the loan then the transaction is successful and the buyer buys the house
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
        self.buyers.clear() #Remove all buyers from the simulation
        self.houses.clear() 

#This method plots the histogram of Wealth against successful and unsuccessful buyer count
def plot_histogram(successful_buyers, unsuccessful_buyers, ltv_limit):
    successful_buyers_df = pd.DataFrame(successful_buyers, columns=['Wealth'])
    unsuccessful_buyers_df = pd.DataFrame(unsuccessful_buyers, columns=['Wealth'])

    plt.figure(figsize=(10, 6))

    #The wealth values for each buyer is taken from the successful & unsuccessful buyers dataframe
    sns.histplot(successful_buyers_df['Wealth'], kde=True, color='green', label='Successful Buyers')
    sns.histplot(unsuccessful_buyers_df['Wealth'], kde=True, color='red', label='Unsuccessful Buyers')

    plt.title(f'Wealth Distribution Of Buyers For LTV limit {ltv_limit}')
    plt.xlabel('Wealth')
    plt.ylabel('Count')
    plt.legend()

    plt.show()

#This method plots a scatter graph of the successful and unsuccessful buyer count against each LTV limit ran in the simulation
def plot_scatter(successful_buyers, unsuccessful_buyers):
    fig, ax = plt.subplots()
    
    #Successful buyers are marked as Green, Unsuccessful buyers are marked as red.
    if successful_buyers:
        ax.scatter(*zip(*successful_buyers), color='green', label='Successful Buyers')
    if unsuccessful_buyers:
        ax.scatter(*zip(*unsuccessful_buyers), color='red', label='Unsuccessful Buyers')

    ax.set_xlabel('LTV')
    ax.set_ylabel('HomeBuyer Count')

    ax.legend()
    plt.show()

#This method runs the simulation with a set of parameters
def run_simulation(num_buyers, num_houses, plot_types, save_results):
    #Initialize the lists to store the results of successful and unsuccessful buyers
    successful_buyers = []
    unsuccessful_buyers = []

    #Loop over a range of LTV limits from 0.1 to 1.0
    for ltv_limit in np.arange(0.1, 1.01, 0.1):
        parameters = {
            'num_buyers': num_buyers,
            'num_houses': num_houses,
            'ltv_limit': ltv_limit,
        }
        
        #Create an instance of HousingMarketModel with the parameters from earlier
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
        bids_df = pd.DataFrame(model.bids)
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

        if save_results:
            with pd.ExcelWriter('simulation_results.xlsx') as writer:
                successful_buyers_df.to_excel(writer, sheet_name='Successful Buyers')
                unsuccessful_buyers_df.to_excel(writer, sheet_name='Unsuccessful Buyers')
                bids_df.to_excel(writer, sheet_name='Bids')
                loanrequests_df.to_excel(writer, sheet_name='Loan Requests')

        #If the plot type includes Histogram then call the Histogram method from earlier to plot a histogram for wealth distribution at every LTV limit
        if 'Histogram' in plot_types:
            plot_histogram([buyer['Wealth'] for buyer in model.successful_buyers], 
                           [buyer['Wealth'] for buyer in model.unsuccessful_buyers], ltv_limit)

    #If the plot type includes the scatter graph then call the scatter method from earlier to plot buyer accounts for every LTV limit
    if 'Scatter' in plot_types:
        plot_scatter(successful_buyers, unsuccessful_buyers)



#User Interface For Policy Maker
fig, ax = plt.subplots(figsize=(8, 8))
ax.axis('off')

#Text Boxes To Enter Parameters
text_box1 = TextBox(plt.axes([0.35, 0.5, 0.3, 0.05]), 'Homebuyers')
text_box2 = TextBox(plt.axes([0.35, 0.4, 0.3, 0.05]), 'Homes')


#A check button is added to give the option for selecting whether to save the results or not
save_check = CheckButtons(plt.axes([0.35, 0.7, 0.3, 0.1]), ('Save Results',), actives=[False])
button = Button(plt.axes([0.35, 0.3, 0.3, 0.05]), 'Run')
#A check button is added so policy makers can choose plot types
check = CheckButtons(plt.axes([0.35, 0.6, 0.3, 0.1]), ('Scatter', 'Histogram'), actives=[True, True])

#Run button to run simulation with entered parameters when clicked
button = Button(plt.axes([0.35, 0.3, 0.3, 0.05]), 'Run')

#When the button is clicked, the parameters are used to run the simulation to produce results for each plot type
def on_button_clicked(event):
    #The parameters are fetched from the text boxes
    num_buyers = int(text_box1.text)
    num_houses = int(text_box2.text)

    #Whichever plot type is selected will be produced as a result after the end of the simulation
    plot_types = [label.get_text() for label, active in zip(check.labels, check.get_status()) if active]
    
    #This get the status of the 'Save Results' check button
    save_results = save_check.get_status()[0]
    run_simulation(num_buyers, num_houses, plot_types, save_results)

#This connects the method to the button
button.on_clicked(on_button_clicked)

plt.show()

if __name__ == "__main__":
    plt.show()
