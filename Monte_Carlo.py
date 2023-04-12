import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def monte_carlo_yield_estimation(csv_file):
    # Load data
    df = pd.read_csv(csv_file)
    
    # Set the index to be the date
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Define parameters
    num_simulations = 1000
    num_days = 600

    # Calculate daily returns
    returns = df.pct_change()

    # Calculate the mean and standard deviation of the daily returns
    mean_return = returns.mean()
    return_stdev = returns.std()

    # Create a list of dates starting from the last date in the data frame
    last_date = df.index[-1]
    dates = pd.date_range(last_date, periods=num_days)

    # Create an empty data frame to store the simulated yields
    simulated_yields = pd.DataFrame(index=dates, columns=df.columns)

    # Set the starting yields to be the yields on the last day in the data frame
    simulated_yields.iloc[0] = df.iloc[-1]

    # Simulate future yields using the Monte Carlo method
    for i in range(1, num_days):
        for j in range(num_simulations):
            simulated_yields.iloc[i] = simulated_yields.iloc[i - 1] * (1 + np.random.normal(mean_return, return_stdev))
    
    # Calculate the mean squared error (MSE) to evaluate the accuracy of the simulation
    # mse = ((simulated_yields - df.iloc[-1]) ** 2).mean()
    # print('MSE:', mse)
   
    return simulated_yields

# Call the function using the input csv file, and save the output to another csv file
monte_carlo_yield_estimation('daily-treasury-rates-3.csv').to_excel("output.xlsx")



# Plotting to be fixed (currently it's plotting the first yields in the different maturities instead of for a single maturity)
# Plot the simulated yields against the actual yields
# print(df.index)
# print('index: ', df.index)
# print(df.index)
# print(df['3 Mo'])
# plt.plot(df.index, df['3 Mo'], label='Actual Yield')
# print(simulated_yields.mean())
# plt.plot(simulated_yields.index, simulated_yields.mean(), label='Simulated Yield')
# plt.legend()
# plt.show()