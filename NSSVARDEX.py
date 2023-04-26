import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import VAR

def parse_maturity(maturities, maturity_column_name):
    # Change maturity unit to years
    for i in range(len(maturities)):
        m = maturities[i].split()
        if len(m) == 1:
            val = float(m[0])
        else:
            if m[1][0] == 'D' or m[1][0] =='d':
                val = round(int(m[0])/365, 3)
            elif m[1][0] == 'M' or m[1][0] =='m':
                val = round(int(m[0])/12, 3)
            elif m[1][0] == 'Y' or m[1][0] =='y':
                val = float(m[0])
            else:
                raise TypeError('Unknown measure of time')  
        maturity_column_name[val] = i
        maturities[i] = val

# NSS model functions
def B(t, beta):
    return ((1 - np.exp(-t / beta[2])) / (t / beta[2])) * beta[0] + ((1 - np.exp(-t / beta[2])) / (t / beta[2])) * beta[1] * (t / beta[2] + np.exp(-t / beta[2]) - 1) + ((1 - np.exp(-t / beta[3])) / (t / beta[3])) * beta[1] * (t / beta[3] + np.exp(-t / beta[3]) - 1)

def NSS_curve(t, beta):
    alpha1 = (1-np.exp(-t/beta[4])) / (t/beta[4])
    alpha2 = alpha1 - np.exp(-t/beta[5])
    alpha3 = (1-np.exp(-t/beta[5])) / (t/beta[5]) - np.exp(-t/beta[5])
    return beta[0] + beta[1]*alpha1 + beta[2]*alpha2 + beta[3]*alpha3

def NSS_residuals(beta, t, y):
    return np.sum((NSS_curve(t, beta) - y)**2)

currency_from = 'US'
currency_to = 'IN'
dataset = 'DEX'+currency_to+currency_from

# Load exchange rate data
exchange_data = pd.read_csv('data/'+dataset+'.csv', parse_dates=['DATE'])

# Replace NaN with the previous value using pandas fillna() function
exchange_data = exchange_data.fillna(method='ffill')

# User-specified date
prediction_date = input('Predict exchange rate for date (MM-DD-YYYY): ')
prediction_date = pd.to_datetime(prediction_date)
# Latest date in dataset
latest_date = exchange_data.iloc[-1]['DATE']

# Get raw exchange rate data values
exchange_rates = exchange_data.values

year = 2021
prediction_year = prediction_date.year

# If date is within dataset range, get the closest exchange rate to it
if(prediction_date <= latest_date):
    # Find the closest date in the dataset to the user-specified date
    closest_date = exchange_data['DATE'].iloc[(exchange_data['DATE'] - prediction_date).abs().argsort()[:1]].values[0]
    # Retrieve the exchange rate value for the closest date
    exchange_rate = exchange_data.loc[exchange_data['DATE'] == closest_date, dataset].values[0]
    print('Predicted exchange rate: ', exchange_rate)

# Otherwise, need to predict using VAR on NSS residuals on bond yield data
else:
    # Load exchange rate data with date as index
    exchange_data = pd.read_csv('data/'+dataset+'.csv', parse_dates=['DATE'], header=0, index_col=0)
    exchange_data[dataset] = [float(x) if x != '.' else pd.np.nan for x in exchange_data[dataset]]
    # Replace NaN with the previous value using pandas fillna() function
    exchange_data = exchange_data.fillna(method='ffill')
    
    # Load bond yield data
    bond_data = pd.read_csv('data/daily-treasury-rates-'+str(year)+'.csv', header=0, parse_dates=['Date'], index_col=0)
    bond_data.columns = [col.strip() for col in bond_data.columns]
    # Replace NaN with the previous value using pandas fillna() function
    bond_data = bond_data.fillna(method='ffill')  
    bond_data = bond_data.iloc[::-1]

    # Get raw bond yield data values
    bond_data_yields = bond_data.values

    # Get maturities
    maturities = bond_data.columns.values
    num_maturities = len(maturities)
    #print("Maturities:", maturities)

    bond_data = bond_data.transpose()
    # Retrieve all dates
    dates = np.array(bond_data.columns.values)
    num_dates = len(dates)
    #print("Dates:",dates)
    bond_data = bond_data.transpose()

    maturity_column_name = {}
    parse_maturity(maturities, maturity_column_name)
    maturities = maturities.astype(float)

    # Initialize betas to zeros array
    betas = np.zeros((num_dates, 6))

    # Set upper bound for betas depending on values in data
    # upper_bound = np.amax(yields) - np.amin(yields)
    beta_bounds = [(0, 5), (-5, 5), (-5, 5), (-1, 1), (0, 1), (0, 1)]
    
    pre_maturity = max(n for n in maturities if n <= prediction_year - year)
    post_maturity = prediction_year
    
    bond_data_yields = bond_data_yields.transpose()
    pre_maturity_actual = np.array(bond_data_yields[maturity_column_name[pre_maturity]])
    post_maturity_actual = np.zeros(0)
    pre_maturity_pred = np.zeros(0)
    post_maturity_pred = np.zeros(0)
    
    if(maturities[-1] >= prediction_year - year):
        post_maturity = min(n for n in maturities if n >= prediction_year - year)
        post_maturity_actual = np.array(bond_data[maturity_column_name[post_maturity]])
    
    bond_data_yields = bond_data_yields.transpose()
        
    for i in range(num_dates):
        betas[i] = np.empty(6)
        betas[i].fill(0.5)
        #betas[i] = np.array([1, -1, -1, -1, 0.1, -0.1])
        res = minimize(NSS_residuals, betas[i], args=(maturities, bond_data_yields[i]), method='L-BFGS-B', bounds=beta_bounds)
        betas[i] = res.x
        pre_maturity_pred = np.append(pre_maturity_pred, NSS_curve(pre_maturity, betas[i]))
        if(prediction_year != post_maturity):
            post_maturity_pred = np.append(post_maturity_pred,NSS_curve(post_maturity, betas[i]))
            
    pre_nss_residuals = np.zeros(pre_maturity_actual.shape)
    post_nss_residuals = np.zeros(post_maturity_actual.shape)
    
    # Get NSS Residuals for all available and relevant dates    
    for i in range(num_dates):
        pre_nss_residuals[i] = pre_maturity_actual[i] - pre_maturity_pred[i]
        
    combined_residuals = pd.DataFrame({'Date': dates, 'Pre': pre_nss_residuals})
        
    if(len(post_maturity_actual)):
        # Get NSS Residuals for all available and relevant dates    
        for i in range(num_dates):
            post_nss_residuals[i] = post_maturity_actual[i] - post_maturity_pred[i]
        combined_residuals = pd.DataFrame({'Date': dates, 'Pre': pre_nss_residuals, 'Post': post_nss_residuals})
        
    combined_residuals = combined_residuals.set_index('Date')
            
    combined_data = combined_residuals.join(exchange_data, how='inner')
    
    combined_data.reset_index(drop=True)
    
    months = 12*(prediction_year - year)
    
    # Split the data into a training set and a test set
    train_data = combined_data.iloc[:len(combined_data)-months, :]
    test_data = combined_data.iloc[len(combined_data)-months:, :]
    
    # Fit a VAR model to the training data
    model = VAR(train_data)
    results = model.fit(maxlags=2, ic='aic')
    
    # Use the VAR model to make predictions for the test data
    lag_order = results.k_ar
    forecast_input = train_data.values[-lag_order:]
    forecast = results.forecast(y=forecast_input, steps=months)
    
    # Convert the forecast results into a DataFrame
    forecast = pd.DataFrame(forecast, index=test_data.index, columns=combined_data.columns)
    print(forecast)
    print(mean_squared_error(forecast[dataset],test_data[dataset]))
    
    # Use the fitted model to make predictions for future dates
    future_steps = (prediction_year - year) * 12 + prediction_date.month # Number of steps to forecast
    future_forecast = results.forecast(y=train_data.values[-lag_order:], steps=future_steps)
    
    # Convert the forecast results into a DataFrame
    future_forecast = pd.DataFrame(future_forecast, columns=combined_data.columns)
    # Values under DEX____ represent future_steps months into the future
    print(forecast)    
'''
df = pd.read_csv('exchange_rates.csv')

# Convert the 'date' column to a pandas datetime object
df['date'] = pd.to_datetime(df['date'])

# User-specified date
user_date = pd.to_datetime('2022-01-01')

# Find the closest date in the dataset to the user-specified date
closest_date = df['date'].iloc[(df['date'] - user_date).abs().argsort()[:1]].values[0]

# Retrieve the exchange rate value for the closest date
exchange_rate = df.loc[df['date'] == closest_date, 'exchange_rate'].values[0]

# Print the results
print(f"The closest date to {user_date} is {closest_date}, with an exchange rate of {exchange_rate}")

'''