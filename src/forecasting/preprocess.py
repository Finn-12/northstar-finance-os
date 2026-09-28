import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def create_features(df):

    df["margin"] = df["revenue"] - df["cost"]

    df["margin_pct"] = (
        df["margin"] / df["revenue"]
    )

    return df



from preprocess import *

df = load_data(
    "src/data/raw/project_forecast.csv"
)

df = create_features(df)

print(df.head())