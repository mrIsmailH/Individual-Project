import agentpy as ap
import random
from matplotlib.widgets import CheckButtons, RadioButtons, TextBox, Button
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from homebuyer import Homebuyer
from lender import Lender
from house import House
from housing_market_model import HousingMarketModel


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
def run_simulation(parameters, plot_types, save_results):
    #Initialize the lists to store the results of successful and unsuccessful buyers
    successful_buyers = []
    unsuccessful_buyers = []
    
    #Loop over a range of LTV limits from 0.1 to 1.0
    for ltv_limit in np.arange(0.1, 1.01, 0.1):
        
        parameters['ltv_limit'] = ltv_limit
        
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

        #Results from every dataframe for every LTV limit are added to the database file.
        if save_results:
            with pd.ExcelWriter('simulation_results.xlsx', engine='openpyxl', mode='a') as writer:
                if f'Successful Buyers {ltv_limit}' not in writer.sheets:
                    successful_buyers_df.to_excel(writer, sheet_name=f'Successful Buyers {ltv_limit}')
                if f'Unsuccessful Buyers {ltv_limit}' not in writer.sheets:
                    unsuccessful_buyers_df.to_excel(writer, sheet_name=f'Unsuccessful Buyers {ltv_limit}')
                if f'Bids {ltv_limit}' not in writer.sheets:
                    bids_df.to_excel(writer, sheet_name=f'Bids {ltv_limit}')
                if f'Loan Requests {ltv_limit}' not in writer.sheets:
                    loanrequests_df.to_excel(writer, sheet_name=f'Loan Requests {ltv_limit}')
                    
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
text_box1 = TextBox(plt.axes([0.3, 0.7, 0.4, 0.05]), 'Homebuyers')
text_box2 = TextBox(plt.axes([0.3, 0.6, 0.4, 0.05]), 'Homes')
text_box3 = TextBox(plt.axes([0.3, 0.5, 0.4, 0.05]), 'Minimum Buyer Wealth')
text_box4 = TextBox(plt.axes([0.3, 0.4, 0.4, 0.05]), 'Maximum Buyer Wealth')

check = CheckButtons(plt.axes([0.3, 0.8, 0.4, 0.1]), ('Scatter', 'Histogram', 'Save Results'), actives=[True, True, False])

#Run button to run simulation with entered parameters when clicked
button = Button(plt.axes([0.35, 0.25, 0.3, 0.1]), 'Run')

#When the button is clicked, the parameters are used to run the simulation to produce results for each plot type
def on_button_clicked(event):
    #The parameters are fetched from the text boxes
    num_buyers = int(text_box1.text)
    num_houses = int(text_box2.text)
    min_wealth = float(text_box3.text)
    max_wealth = float(text_box4.text)

    #Whichever plot type is selected will be produced as a result after the end of the simulation
    plot_types = [label.get_text() for label, active in zip(check.labels, check.get_status()) if active]
    
    #This get the status of the 'Save Results' check button
    save_results = 'Save Results' in plot_types
    if save_results:
        plot_types.remove('Save Results')

    parameters = {
        'num_buyers': num_buyers,
        'num_houses': num_houses,
        'wealth_range': (min_wealth, max_wealth),
    }

    run_simulation(parameters, plot_types, save_results)

#This connects the method to the button
button.on_clicked(on_button_clicked)

if __name__ == "__main__":
    plt.show()
