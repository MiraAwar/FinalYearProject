import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

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
def B(t, beta):
    return ((1 - np.exp(-t / beta[2])) / (t / beta[2])) * beta[0] + ((1 - np.exp(-t / beta[2])) / (t / beta[2])) * beta[1] * (t / beta[2] + np.exp(-t / beta[2]) - 1) + ((1 - np.exp(-t / beta[3])) / (t / beta[3])) * beta[1] * (t / beta[3] + np.exp(-t / beta[3]) - 1)

def NSS_curve(t, beta):
    alpha1 = (1-np.exp(-t/beta[4])) / (t/beta[4])
    alpha2 = alpha1 - np.exp(-t/beta[5])
    alpha3 = (1-np.exp(-t/beta[5])) / (t/beta[5]) - np.exp(-t/beta[5])
    return beta[0] + beta[1]*alpha1 + beta[2]*alpha2 + beta[3]*alpha3

def NSS_residuals(beta, t, y):
    return np.sum((NSS_curve(t, beta) - y)**2)

year = 2023

# Load bond yield data
data = pd.read_csv('data/daily-treasury-rates-'+str(year)+'.csv', header=0, index_col=0)

# Get maturities before transposing array
maturities = data.columns.values
num_maturities = len(maturities)
print("Maturities:", maturities)

# Transpose the DataFrame so that each row represents a date and each column represents a maturity
data = data.transpose()

# Retrieve all dates
dates = data.columns.values
num_dates = len(dates)
#print("Dates:",dates)
 
parse_maturity(maturities)
        
print("Maturities:", maturities)
maturities = maturities.astype(float)

# Replace NaN with the previous value using pandas fillna() function
data = data.fillna(method='ffill')  

# Transpose the DataFrame so that each row represents a date and each column represents a maturity
data = data.transpose()
# Retrieve 2D table of yields   
data_yields = data.values
yields = []
for i in range (num_dates):
    yields.append(data_yields[i])

# Initialize betas to zeros array
betas = np.zeros((num_dates, 6))

# Set upper bound for betas depending on values in data
# upper_bound = np.amax(yields) - np.amin(yields)

beta_bounds = [(0, 5), (-5, 5), (-5, 5), (-1, 1), (0, 1), (0, 1)]

for i in range(num_dates):
    betas[i] = np.empty(6)
    betas[i].fill(0.5)
    #betas[i] = np.array([1, -1, -1, -1, 0.1, -0.1])
    res = minimize(NSS_residuals, betas[i], args=(maturities, yields[i]), method='L-BFGS-B', bounds=beta_bounds)
    betas[i] = res.x

# select desired maturities
new_maturities = np.arange(1, 41)

# Define data and weight vector
weights = np.arange(num_dates, 0, -1)
'''
alpha = 0.1
weights = np.exp(-alpha*weights)
weights /= weights.sum()  # normalize weights

beta_avg = np.dot(weights, betas)

'''

weighted_beta_sum = np.zeros_like(betas[0])
total_weight = 0
for beta, weight in zip(betas, weights):
    weighted_beta_sum += beta * weight
    total_weight += weight

beta_avg = weighted_beta_sum / total_weight


# Compute the NSS yield curve for the predicted parameters
curve = []
for j in range(len(new_maturities)):
    maturity = new_maturities[j]
    b = B(maturity, beta_avg) 
    curve.append(NSS_curve(maturity, beta_avg))
print(curve)
plt.figure(j)
plt.plot(new_maturities, curve)

