import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

df = pd.read_csv("app/data/raw/project_forecast.csv")

print(df.head())
print("\nMissing values:")
print(df.isna().sum())

df = df.dropna(subset=["revenue"])

X = [[i] for i in range(1, len(df)+1)]
y = df["revenue"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "revenue_model.pkl")

print("Model trained successfully.")