import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

def parse_maturity(maturities):
    # Change maturity unit to years
    for i in range(len(maturities)):
        m = maturities[i].split()
        if len(m) == 1:
            maturities[i] = float(m[0])
        else:
            if m[1][0] == 'D' or m[1][0] =='d':
                maturities[i] = round(int(m[0])/365, 3)
            elif m[1][0] == 'M' or m[1][0] =='m':
                maturities[i] = round(int(m[0])/12, 3)
            elif m[1][0] == 'Y' or m[1][0] =='y':
                maturities[i] = float(m[0])
            else:
                raise TypeError('Unknown measure of time')   

# NSS model functions
def NSS_curve(t, beta):
    alpha1 = (1-np.exp(-t/beta[4])) / (t/beta[4])
    alpha2 = alpha1 - np.exp(-t/beta[5])
    alpha3 = (1-np.exp(-t/beta[5])) / (t/beta[5]) - np.exp(-t/beta[5])
    return beta[0] + beta[1]*alpha1 + beta[2]*alpha2 + beta[3]*alpha3

def NSS_residuals(beta, t, y):
    return np.sum((NSS_curve(t, beta) - y)**2)

for year in range (2015, 2023):
    
    # Load bond yield data
    data = pd.read_csv('data/daily-treasury-rates-'+str(year)+'.csv', header=0, index_col=0)
    
    # Get maturities before transposing array
    maturities = data.columns.values
    num_maturities = len(maturities)
    print("Maturities:", maturities)
    
    data = data.transpose()
    # Retrieve all dates
    dates = data.columns.values
    num_dates = len(dates)
    #print("Dates:",dates)
    data = data.transpose()
     
    parse_maturity(maturities)
    maturity_test = maturities[-1]
    maturities = maturities[:-1]
            
    print("Maturities:", maturities)
    maturities = maturities.astype(float)
    
    # Replace NaN with the previous value using pandas fillna() function
    data = data.fillna(method='ffill')  
    
    # Get raw data values
    data_yields = data.values
    num_dates = len(data_yields)
    
    yields = []  
    yields_test = []
    for i in range (num_dates):
        yields_test.append(data_yields[i][-1])
        yields.append(data_yields[i][:-1])
    
    # Initialize betas to zeros array
    betas = np.zeros((num_dates, 6))
    
    # Set upper bound for betas depending on values in data
    # upper_bound = np.amax(yields) - np.amin(yields)
    
    beta_bounds = [(0, 5), (-5, 5), (-5, 5), (-1, 1), (0, 1), (0, 1)]
    
    yields_pred = []
    for i in range(num_dates):
        betas[i] = np.empty(6)
        betas[i].fill(0.5)
        #betas[i] = np.array([1, -1, -1, -1, 0.1, -0.1])
        res = minimize(NSS_residuals, betas[i], args=(maturities, yields[i]), method='L-BFGS-B', bounds=beta_bounds)
        betas[i] = res.x
        yields_pred.append(NSS_curve(maturity_test, betas[i]))
        
    mse = mean_squared_error(yields_test, yields_pred)
    mape = np.mean(np.abs((np.array(yields_test) - np.array(yields_pred)) / np.array(yields_test))) * 100
    mae = mean_absolute_error(yields_test, yields_pred)
    print('Pre MSE', mse)
    print('Pre MAE', mae)
    print('Pre MAPE', mape)  
    
    medians = np.median(betas, axis=0)
    stds = np.std(betas, axis=0)
    
    # Define acceptable ranges for each column
    ranges = [(medians[i] - stds[i], medians[i] + stds[i]) for i in range(betas.shape[1])]
    
    # Remove rows containing values outside of acceptable ranges
    clean_betas = betas[~np.any(np.logical_or(betas < np.array(ranges)[:, 0], betas > np.array(ranges)[:, 1]), axis=1)]
    
    # select desired maturities
    new_maturities = np.arange(1, 41)
    
    # Define weights to assign to each row
    weights = np.linspace(0.1, 1.0, num=clean_betas.shape[0])
    #weights = np.empty(clean_betas.shape[0])
    #weights.fill(1)
    
    # Shuffle the data and corresponding weights
    shuffle_idx = np.random.permutation(clean_betas.shape[0])
    clean_betas = clean_betas[shuffle_idx]
    weights = weights[shuffle_idx]
    
    # Compute the final prediction by taking a weighted average of betas
    final_beta = np.average(clean_betas, axis=0, weights=weights)
    
    # Compute the NSS yield curve for the predicted parameters
    curve = []
    for j in range(len(new_maturities)):
        maturity = new_maturities[j]
        curve.append(NSS_curve(maturity, final_beta))
    #print(curve)
    plt.figure(j)
    plt.plot(new_maturities, curve)
    
    '''
    yields_test = []
    yields_pred = []
    for j in range(len(maturities)):
        yields_test.append(np.mean(np.array(data_yields[j])))
        yields_pred.append(NSS_curve(maturities[j], final_pred))
    print(yields_test)
    print(yields_pred)
    mse = mean_squared_error(yields_test, yields_pred)
    mape = np.mean(np.abs((np.array(yields_test) - np.array(yields_pred)) / np.array(yields_test))) * 100
    mae = mean_absolute_error(yields_test, yields_pred)
    print('Post MSE', mse)
    print('Post MAE', mae)
    print('Post MAPE', mape)  
    
 '''