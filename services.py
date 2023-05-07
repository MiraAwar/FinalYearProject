import pandas as pd


def preprocess_csv(filename):
    df = pd.read_csv(filename)
    print(df.head())
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    print(X)
    print(y)

preprocess_csv('daily-treasury-rates.csv')