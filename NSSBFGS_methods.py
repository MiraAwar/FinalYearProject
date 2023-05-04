import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.ensemble import RandomForestRegressor
from datetime import date

def parse_maturity(maturities):
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

def NSS_curve(t, beta):
    alpha1 = (1-np.exp(-t/beta[4])) / (t/beta[4])
    alpha2 = alpha1 - np.exp(-t/beta[5])
    alpha3 = (1-np.exp(-t/beta[5])) / (t/beta[5]) - np.exp(-t/beta[5])
    return beta[0] + beta[1]*alpha1 + beta[2]*alpha2 + beta[3]*alpha3

def NSS_residuals(beta, t, y):
    return np.sum((NSS_curve(t, beta) - y)**2)

def Calibrate(maturity_bound, data_year = 2021, csv = None):
    if(csv == None):
        csv = 'daily-treasury-rates-'+str(data_year)
    data = pd.read_csv('data/'+csv+'.csv' , header=0, index_col=0)
    if )maurity_bound < 1):
        return []
    new_maturities = np.arange(1, maturity_bound)
    maturities = data.columns.values
    num_maturities = len(maturities)
    parse_maturity(maturities)
    maturities = maturities.astype(float)
    data = data.transpose()
    dates = data.columns.values
    num_dates = len(dates)
    data = data.transpose()
    data = data.fillna(method='ffill')  
    yields = data.values
    betas = np.zeros((num_dates, 6))
    beta_bounds = [(0, 5), (-5, 5), (-5, 5), (-1, 1), (0, 1), (0, 1)]
    for i in range(num_dates):
        betas[i] = np.empty(6)
        betas[i].fill(0.5)
        res = minimize(NSS_residuals, betas[i], args=(maturities, yields[i]), method='L-BFGS-B', bounds=beta_bounds)
        betas[i] = res.x        
    medians = np.median(betas, axis=0)
    stds = np.std(betas, axis=0)
    ranges = [(medians[i] - stds[i], medians[i] + stds[i]) for i in range(betas.shape[1])]
    clean_betas = betas[~np.any(np.logical_or(betas < np.array(ranges)[:, 0], betas > np.array(ranges)[:, 1]), axis=1)]
    weights = np.linspace(0.1, 1.0, num=clean_betas.shape[0])
    shuffle_idx = np.random.permutation(clean_betas.shape[0])
    clean_betas = clean_betas[shuffle_idx]
    weights = weights[shuffle_idx]
    split_idx = int(0.8 * clean_betas.shape[0])
    train_data, train_weights = clean_betas[:split_idx], weights[:split_idx]
    test_data, test_weights = clean_betas[split_idx:], weights[split_idx:]
    rf = RandomForestRegressor(n_estimators=2000, random_state=42)
    rf.fit(train_data, train_weights)
    pred_weights = rf.predict(test_data)
    pred_weights /= np.sum(pred_weights)
    final_pred = np.average(test_data, axis=0, weights=pred_weights)
    curve = []
    for j in range(len(new_maturities)):
        maturity = new_maturities[j]
        curve.append(NSS_curve(maturity, final_pred))
    return curve

def PredictArray(prediction_year, prediction_maturity, years_available, csv = None):
    if(csv == None):
        data_year = max(n for n in years_available if n <= prediction_year)
        csv = 'data/daily-treasury-rates-'+str(data_year)+'.csv'
    data = pd.read_csv(csv, header=0, index_col=0)
    maturities = data.columns.values
    num_maturities = len(maturities)
    parse_maturity(maturities)
    maturities = maturities.astype(float)
    data = data.transpose()
    dates = data.columns.values
    num_dates = len(dates)
    data = data.transpose()
    data = data.fillna(method='ffill')  
    yields = data.values
    betas = np.zeros((num_dates, 6))
    beta_bounds = [(0, 5), (-5, 5), (-5, 5), (-1, 1), (0, 1), (0, 1)]
    yields_pred = []
    for i in range(num_dates):
        betas[i] = np.empty(6)
        betas[i].fill(0.5)
        res = minimize(NSS_residuals, betas[i], args=(maturities, yields[i]), method='L-BFGS-B', bounds=beta_bounds)
        betas[i] = res.x
        yields_pred.append(NSS_curve(prediction_year, betas[i]))
    return yields_pred

def PredictValue(prediction_year, prediction_maturity, years_available, csv = None):
    if(csv == None):
        data_year = max(n for n in years_available if n <= prediction_year)
        csv = 'data/daily-treasury-rates-'+str(data_year)+'.csv'
    data = pd.read_csv(csv, header=0, index_col=0)
    maturities = data.columns.values
    num_maturities = len(maturities)
    parse_maturity(maturities)
    maturities = maturities.astype(float)
    data = data.transpose()
    dates = data.columns.values
    num_dates = len(dates)
    data = data.transpose()
    data = data.fillna(method='ffill')  
    yields = data.values
    betas = np.zeros((num_dates, 6))
    beta_bounds = [(0, 5), (-5, 5), (-5, 5), (-1, 1), (0, 1), (0, 1)]
    yields_pred = []
    for i in range(num_dates):
        betas[i] = np.empty(6)
        betas[i].fill(0.5)
        res = minimize(NSS_residuals, betas[i], args=(maturities, yields[i]), method='L-BFGS-B', bounds=beta_bounds)
        betas[i] = res.x
    medians = np.median(betas, axis=0)
    stds = np.std(betas, axis=0)
    ranges = [(medians[i] - stds[i], medians[i] + stds[i]) for i in range(betas.shape[1])]
    clean_betas = betas[~np.any(np.logical_or(betas < np.array(ranges)[:, 0], betas > np.array(ranges)[:, 1]), axis=1)]
    weights = np.linspace(0.1, 1.0, num=clean_betas.shape[0])
    shuffle_idx = np.random.permutation(clean_betas.shape[0])
    clean_betas = clean_betas[shuffle_idx]
    weights = weights[shuffle_idx]
    split_idx = int(0.8 * clean_betas.shape[0])
    train_data, train_weights = clean_betas[:split_idx], weights[:split_idx]
    test_data, test_weights = clean_betas[split_idx:], weights[split_idx:]
    rf = RandomForestRegressor(n_estimators=2000, random_state=42)
    rf.fit(train_data, train_weights)
    pred_weights = rf.predict(test_data)
    pred_weights /= np.sum(pred_weights)
    final_pred = np.average(test_data, axis=0, weights=pred_weights)
    curve = []
    predicted_value = NSS_curve(prediction_maturity, final_pred)
    return predicted_value




