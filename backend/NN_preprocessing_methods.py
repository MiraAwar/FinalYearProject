import pandas as pd
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
    return scaler.inverse_transform(nd_array)