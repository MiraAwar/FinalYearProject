# Importing Packages
import yfinance as yf
import numpy as np
from random import random
import matplotlib.pyplot as plt
from scipy.stats import norm

def predict_stock_closing_price(stock, number_of_days):
      # Defining the Ticker
      ticker = yf.Ticker(stock)

      # Obtain Historical Market Data
      start_date = '2012-05-04'
      end_date = '2022-01-01'
      hist = ticker.history(start=start_date, end=end_date)
      # print(hist.head())

      # Pulling Closing Price Data
      hist = hist[['Close']]
      # print("HISTORY", hist)

      # # Plotting Price Data
      # hist['Close'].plot(title="AAPL Stock Price", ylabel=
      #                    "Closing Price [$]", figsize=[10, 6])
      # plt.grid()
      # plt.show()

      # Create Day Count, Price, and Change Lists
      days = [i for i in range(1, len(hist['Close'])+1)]
      price_orig = hist['Close'].tolist()
      change = hist['Close'].pct_change().tolist()
      change = change[1:]  # Removing the first term since it is NaN
      # print("CHANGE", change)

      # Statistics for Use in Model
      mean = np.mean(change)
      std_dev = np.std(change)
      print('\nMean percent change: ' + str(round(mean*100, 2)) + '%')
      print('Standard Deviation of percent change: ' +   
            str(round(std_dev*100, 2)) + '%')

      # Simulation Number and Prediction Period
      simulations = 2000 # Change for more results
      days_to_sim = number_of_days # Trading days in 1 year

      # # Initializing Figure for Simulation
      # fig = plt.figure(figsize=[10, 6])
      # plt.plot(days, price_orig)
      # plt.title("Monte Carlo Stock Prices [" + str(simulations) + 
      #           " simulations]")
      # plt.xlabel("Trading Days After " + start_date)
      # plt.ylabel("Closing Price [$]")
      # plt.xlim([2000, len(days)+days_to_sim])
      # plt.grid()

      # Initializing Lists for Analysis
      close_end = []
      above_close = []

      # For Loop for Number of Simulations Desired
      # LOOP HERE HERE ----------------
      for i in range(simulations):
            num_days = [days[-1]]
            close_price = [hist.iloc[-1,0]]

            # For Loop for Number of Days to Predict
            for j in range(days_to_sim):
                  num_days.append(num_days[-1] + 1)
                  perc_change = norm.ppf(random(), loc = mean, scale = std_dev)
                  close_price.append(close_price[-1]* (1 + perc_change))
            
            if close_price[-1] > price_orig[-1]:
                  above_close.append(1)
            else:
                  above_close.append(0)
            
            close_end.append(close_price[-1])
            # plt.plot(num_days, close_price)

      # Average Closing Price and Probability of Increasing After 1 Year
      average_closing_price = sum(close_end)/simulations
      average_perc_change = (average_closing_price-
                        price_orig[-1])/price_orig[-1]
      probability_of_increase = sum(above_close)/simulations
      print('\nPredicted closing price after ' + str(simulations) + 
            ' simulations: $' + str(round(average_closing_price, 2)))
      print('Predicted percent increase after 1 year: ' + 
            str(round(average_perc_change*100, 2)) + '%')
      print('Probability of stock price increasing after 1 year: ' + 
            str(round(probability_of_increase*100, 2)) + '%')


      # Get Actual Closing Price
      actual_closing_price = ticker.history(period='1d')['Close'].iloc[0]

      # Get Predicted Closing Price and Calculate Difference
      predicted_closing_price = average_closing_price
      price_diff = actual_closing_price - average_closing_price

      # Get Actual Closing Price
      actual_closing_price = ticker.history(start="2022-02-01", end='2022-02-02')['Close'][0]
      print("CLOSING PRICE",actual_closing_price)

      # Get Predicted Closing Prices
      predicted_closing_prices = np.array(close_end)

      # print('Actual closing price after ' + end_date + ': $' + 
      #       str(round(actual_closing_price, 2)))
      # print('Difference between actual and predicted closing price: $' + 
      #       str(round(price_diff, 2)))

      print("Actual Price: ", actual_closing_price)
      print("Predicted Price: ", predicted_closing_price)      
      print('Percent error:', ((actual_closing_price - predicted_closing_price)/(actual_closing_price)) * 100)

      actual_prices = ticker.history(start='2022-01-01', end='2022-02-02')['Close'].tolist()

      # actual_prices = actual_prices[-21:]

      # predicted_prices = close_end[-21:]
      # print(actual_prices)
      # print(predicted_prices)

      # mse = np.mean((np.array(actual_prices) - np.array(predicted_prices)) ** 2) / simulations
      # print("MSE:", mse)


      # mae = np.mean(np.abs(np.array(actual_prices) - np.array(predicted_prices))) / simulations
      # print("MAE:", mae)

      # epsilon = 1e-10
      # mape = np.mean(np.abs((np.array(actual_prices) - np.array(predicted_prices)) / (np.array(actual_prices) + epsilon))) * 100
      # mape_normalized = mape 
      # print("MAPE", mape_normalized)

      # Displaying the Monte Carlo Simulation Lines
      # plt.show()


      # Get dates for actual prices
      actual_dates = ticker.history(start='2022-01-01', end='2022-02-02').index[-21:]

      return round(predicted_closing_price,2)
      # Plot actual prices and predicted prices
      # plt.plot(actual_dates, actual_prices, label='Actual Prices')
      # plt.plot(actual_dates, predicted_prices, label='Predicted Prices')
      # plt.title('Actual vs Predicted Prices')
      # plt.xlabel('Date')
      # plt.ylabel('Closing Price [$]')
      # plt.legend()
      # plt.show()

# print(predict_stock_closing_price("SPY", 10))
# print(predict_stock_closing_price("AMZN", 5))
# print(predict_stock_closing_price("GOOGL", 1))