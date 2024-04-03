import agentpy as ap

#Lender Class
class Lender(ap.Agent):
    def decide(self, loan_request, house_price, ltv_limit):
    #This class decides whether a loan is accepted or rejected based on the loan amount and LTV limit
        max_loan = house_price * ltv_limit
        return loan_request <= max_loan
