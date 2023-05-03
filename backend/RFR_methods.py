import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def parse_maturity(maturities, maturity_column_name):
    # Change maturity unit to years
    for i in range(len(maturities)):
        s = maturities[i]
        m = s.split()
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
        maturity_column_name[val] = s
        maturities[i] = val 
        
def Predict_RFR(prediction_year, prediction_maturity, years_available, csv = None):  
    if(csv == None):
        csv = 'daily-treasury-rates-'+str(prediction_year)
    bond_data = pd.read_csv('data/'+csv+'.csv', header=0, index_col=0)
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
    X = bond_data_yields[:,:-1]
    y = bond_data_yields[:,-1]       
    rf = RandomForestRegressor()
    rf.fit(X, y)
    future_maturity_yield = rf.predict(X)
    return future_maturity_yield