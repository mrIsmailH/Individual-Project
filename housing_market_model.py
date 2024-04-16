import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import agentpy as ap
from homebuyer import Homebuyer
from lender import Lender
from house import House

#Housing Model Class
class HousingMarketModel(ap.Model):
    def setup(self):
        #Initialises all the agents in the simulation as well as the data structures to store the simulation results
        self.buyers = ap.AgentList(self, self.p['num_buyers'], Homebuyer, wealth_range=self.p['wealth_range'])
        self.lender = Lender(self)
        self.houses = ap.AgentList(self, self.p['num_houses'], House)
        self.successful_buyers = []
        self.unsuccessful_buyers = []
        self.LoanRequests = []
        self.bids = []
        
    def step(self):
        #This method is responsible for modelling the interactions between all agents at each time step
        if not self.houses:
            return

        #An auction is held for each house
        for house in self.houses:
            highest_bid = 0
            highest_bidder = None

            for buyer in self.buyers:
                bid = min(house.price, buyer.deposit * 0.9)
                #The buyer only bids on the house if it matches their bedroom preference
                #If more than 10 time steps have passed, buyers will settle for any house they can bid on
                if buyer.bedroom_pref == house.bedrooms or self.t > 10:  
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
                    'Buyer Bedroom Preference': highest_bidder.bedroom_pref,
                    'House Bedrooms': house.bedrooms,
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
