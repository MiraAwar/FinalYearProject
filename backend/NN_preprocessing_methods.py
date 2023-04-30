import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

def preprocess_csv(csv_file_name):
    # Load the data from a CSV file
    data = pd.read_csv(csv_file_name)

    # Drop the date column
    data.drop('Date', axis=1, inplace=True)
    data.drop('2 Mo', axis=1, inplace=True)
    data.drop('4 Mo', axis=1, inplace=True)
    data.drop('20 Yr', axis=1, inplace=True)
    data.drop('30 Yr', axis=1, inplace=True)

    scaler = MinMaxScaler()
    model_input = scaler.fit_transform(data.iloc[:, :-1])
    scaler.fit_transform(data.iloc[:, -1:])
    return (model_input, scaler)
    
def scale_input(nd_array, scaler):
    return (scaler.inverse_transform(nd_array)).tolist()

def fix_list(list):
    return np.concatenate(list).tolist()

def impute_missing_data(csv_file_name):
    data = pd.read_csv(csv_file_name)
    date_col = data['Date']
    print("date:", date_col)
    data.drop('Date', axis=1, inplace=True)
    imputer = KNNImputer(n_neighbors=10)
    imputed_data = imputer.fit_transform(data)
    data = pd.DataFrame(imputed_data, columns=data.columns)
    data.to_csv("imputed_" + csv_file_name, index=False)