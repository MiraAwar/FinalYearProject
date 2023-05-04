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

def NSS_curve(t, beta):
    alpha1 = (1-np.exp(-t/beta[4])) / (t/beta[4])
    alpha2 = alpha1 - np.exp(-t/beta[5])
    alpha3 = (1-np.exp(-t/beta[5])) / (t/beta[5]) - np.exp(-t/beta[5])
    return beta[0] + beta[1]*alpha1 + beta[2]*alpha2 + beta[3]*alpha3

def NSS_residuals(beta, t, y):
    return np.sum((NSS_curve(t, beta) - y)**2)

def PredictExchange(prediction_date, currency_from = None, currency_to = None, csv = None):
    year = 2021
    if(csv):
        dataset = csv
    else:
        dataset = 'DEX'+currency_to+currency_from
    exchange_data = pd.read_csv('data/'+dataset+'.csv', parse_dates=['DATE'])
    exchange_data = exchange_data.fillna(method='ffill')
    prediction_date = pd.to_datetime(prediction_date)
    latest_date = exchange_data.iloc[-1]['DATE']
    exchange_rates = exchange_data.values
    prediction_year = prediction_date.year
    if(prediction_date <= latest_date):
        closest_date = exchange_data['DATE'].iloc[(exchange_data['DATE'] - prediction_date).abs().argsort()[:1]].values[0]
        exchange_rate = exchange_data.loc[exchange_data['DATE'] == closest_date, dataset].values[0]
        return exchange_rate
    else:
        exchange_data = pd.read_csv('data/'+dataset+'.csv', parse_dates=['DATE'], header=0, index_col=0)
        exchange_data[dataset] = [float(x) if x != '.' else pd.np.nan for x in exchange_data[dataset]]
        exchange_data = exchange_data.fillna(method='ffill')
        bond_data = pd.read_csv('data/daily-treasury-rates-'+str(year)+'.csv', header=0, parse_dates=['Date'], index_col=0)
        bond_data.columns = [col.strip() for col in bond_data.columns]
        bond_data = bond_data.fillna(method='ffill')  
        bond_data = bond_data.iloc[::-1]
        bond_data_yields = bond_data.values
        maturities = bond_data.columns.values
        num_maturities = len(maturities)
        bond_data = bond_data.transpose()
        dates = np.array(bond_data.columns.values)
        num_dates = len(dates)
        bond_data = bond_data.transpose()
        maturity_column_name = {}
        parse_maturity(maturities, maturity_column_name)
        maturities = maturities.astype(float)
        betas = np.zeros((num_dates, 6))
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
            res = minimize(NSS_residuals, betas[i], args=(maturities, bond_data_yields[i]), method='L-BFGS-B', bounds=beta_bounds)
            betas[i] = res.x
            pre_maturity_pred = np.append(pre_maturity_pred, NSS_curve(pre_maturity, betas[i]))
            if(prediction_year != post_maturity):
                post_maturity_pred = np.append(post_maturity_pred,NSS_curve(post_maturity, betas[i]))
        pre_nss_residuals = np.zeros(pre_maturity_actual.shape)
        post_nss_residuals = np.zeros(post_maturity_actual.shape) 
        for i in range(num_dates):
            pre_nss_residuals[i] = pre_maturity_actual[i] - pre_maturity_pred[i]
        combined_residuals = pd.DataFrame({'Date': dates, 'Pre': pre_nss_residuals})
        if(len(post_maturity_actual)):   
            for i in range(num_dates):
                post_nss_residuals[i] = post_maturity_actual[i] - post_maturity_pred[i]
            combined_residuals = pd.DataFrame({'Date': dates, 'Pre': pre_nss_residuals, 'Post': post_nss_residuals})
        combined_residuals = combined_residuals.set_index('Date')
        combined_data = combined_residuals.join(exchange_data, how='inner')
        combined_data.reset_index(drop=True)
        months = 12*(prediction_year - year)
        train_data = combined_data.iloc[:len(combined_data)-months, :]
        test_data = combined_data.iloc[len(combined_data)-months:, :]
        model = VAR(train_data)
        results = model.fit(maxlags=2, ic='aic')
        lag_order = results.k_ar
        forecast_input = train_data.values[-lag_order:]
        forecast = results.forecast(y=forecast_input, steps=months)
        forecast = pd.DataFrame(forecast, index=test_data.index, columns=combined_data.columns)
        future_steps = (prediction_year - year) * 12 + prediction_date.month # Number of steps to forecast
        future_forecast = results.forecast(y=train_data.values[-lag_order:], steps=future_steps)
        future_forecast = pd.DataFrame(future_forecast, columns=combined_data.columns)
        return future_forecast[dataset].values[-1]
