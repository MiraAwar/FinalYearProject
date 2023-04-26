import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit

# Load bond yield data
data = pd.read_csv('daily-treasury-rates.csv', header=0, index_col=0)

# Get maturities before transposing array
maturities = data.columns.values
num_maturities = len(maturities)
print("Maturities:", maturities)

# Transpose the DataFrame so that each row represents a date and each column represents a maturity
data = data.transpose()

# Print the data to verify
print(data.head())

# Retrieve all dates
dates = data.columns.values
num_dates = len(dates)
print("Dates:",dates)

# Change maturity unit to years
for i in range(len(maturities)):
    m = maturities[i].split()
    if len(m) == 1:
        maturities[i] = int(m[0])
    else:
        if m[1][0] == 'D' or m[1][0] =='d':
            maturities[i] = round(int(m[0])/365, 3)
        elif m[1][0] == 'M' or m[1][0] =='m':
            maturities[i] = round(int(m[0])/12, 3)
        elif m[1][0] == 'Y' or m[1][0] =='y':
            maturities[i] = int(m[0])
        else:
            raise TypeError('Unknown measure of time')           
print("Maturities:", maturities)

# Replace NaN with the previous value using pandas fillna() function
data = data.fillna(method='ffill')  

# Retrieve 2D table of yields   
yields = data.values
print(yields[0])

# Initialize a random forest regressor
regressor = RandomForestRegressor()

#Initialize betas to zeros array
betas = np.zeros((num_maturities, 7))
for i in range(num_maturities):
    betas[i, :] = np.array([0.02, 0.03, 1.0, 0.03, 0.04, 0.05, 0.06])

# Train the regressor on the yield curves from all dates
regressor.fit(yields, betas)

# Initialize the array to be a straight line from 1% to 5% for each maturity
new_yield_curve = np.zeros((num_maturities, num_dates))

for i in range(num_maturities):
    new_yield_curve[i, :] = np.linspace(0.01, 0.05, num_dates)

# Use the trained regressor to predict the coefficients for a new yield curve    
predicted_betas = regressor.predict(new_yield_curve)

# NSS model functions
def B(t, beta):
    B = np.zeros(t.shape)
    B[t <= beta[2]] = beta[0] + beta[1] * (t[t <= beta[2]] - beta[2])
    B[t > beta[2]] = beta[0] + beta[1] * beta[2] + beta[3] * (t[t > beta[2]] - beta[2])
    return B

def nss_yield(maturities, betas):
    tau1, tau2, tau3 = betas[:3]
    beta0, beta1, beta2, beta3 = betas[3:]

    f = beta0 + beta1 * ((1 - np.exp(-maturities/tau1)) / (maturities/tau1))
    f += beta2 * (((1 - np.exp(-maturities/tau1)) / (maturities/tau1)) - np.exp(-maturities/tau1))
    f += beta3 * (((1 - np.exp(-maturities/tau1)) / (maturities/tau1)) - np.exp(-maturities/tau1) - (1 + (maturities/tau1)) * np.exp(-maturities/tau2))

    return f

def fit_nss(yields):
    p0 = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    beta_bounds = ([0, 0, 0, -np.inf, -np.inf, -np.inf, -np.inf],
                   [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])
    betas = np.zeros((yields.shape[0], 8))
    for i in range(yields.shape[0]):
        y = yields[i]
        betas[i], _ = curve_fit(nss_yield, maturities, y, p0=p0, bounds=beta_bounds)
        p0 = betas[i]  # use previous betas as initial guess for next curve fit
    return betas

nss_yields = []
for i in range(num_maturities):
    # Extract the parameters for the i-th maturity
    tau = predicted_betas[i][:3]
    beta = predicted_betas[i][3:]
    print(tau)
    print(beta)

    # Compute the NSS yield curve for the i-th maturity
    curve = []
    for j in range(num_maturities):
        maturity = maturities[j]
        b = B(tau, beta)
        yield_nss = beta[0] + beta[1] * b + beta[2] * (b / tau[1]) * (1 - np.exp(-maturity / tau[1])) + beta[3] * ((b / tau[1]) * (1 - np.exp(-maturity / tau[1])) - np.exp(-maturity / tau[1]))
        curve.append(yield_nss)
    nss_yields.append(curve)
