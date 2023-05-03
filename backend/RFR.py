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

for year in range (2015, 2023):
    print(year)
    
    # Load bond yield data
    bond_data = pd.read_csv('data/daily-treasury-rates-'+str(year)+'.csv', header=0, index_col=0)
    
    bond_data.columns = [col.strip() for col in bond_data.columns]
    # Replace NaN with the previous value using pandas fillna() function
    bond_data = bond_data.fillna(method='ffill')  
    #print(bond_data)
    bond_data = bond_data.iloc[::-1]

    # Get raw bond yield data values
    bond_data_yields = bond_data.values
    
    # Get maturities
    maturities = bond_data.columns.values
    num_maturities = len(maturities)
    #print("Maturities:", maturities)

    '''
    data_smooth = []
    bond_data = bond_data.transpose()
    # Retrieve all dates
    dates = np.array(bond_data.columns.values)
    num_dates = len(dates)
    #print("Dates:",dates)
    for col in bond_data:
        window = np.ones(num_dates)/float(num_dates)
        data_smooth.append(np.convolve(col, window, 'same'))
    bond_data = bond_data.transpose()
'''

    maturity_column_name = {}
    parse_maturity(maturities, maturity_column_name)
    maturities = maturities.astype(float)
    
    future_maturity_yield = 30
    
    # Define the input and output data
    X = bond_data_yields[:,:-1]
    y = bond_data_yields[:,-1]
    
    # Split the data into training and testing sets
    train_size = int(len(bond_data) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    # Train a Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    future_maturity_yield = rf.predict(X_test)
    
    print("Predicted yield for future maturity:", future_maturity_yield[0])
    mse = mean_squared_error(y_test, future_maturity_yield)
    mape = np.mean(np.abs((np.array(y_test) - np.array(future_maturity_yield)) / np.array(y_test))) * 100
    mae = mean_absolute_error(y_test, future_maturity_yield)
    print('MSE', mse)
    print('MAE', mae)
    print('MAPE', mape)  