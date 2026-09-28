import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
df = pd.read_csv(project_root / "src" / "data" / "raw" / "project_forecast.csv")

print(df.head())
print("\nMissing values:")
print(df.isna().sum())

df = df.dropna(subset=["revenue"])

X = [[i] for i in range(1, len(df)+1)]
y = df["revenue"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, project_root / "models" / "revenue_model.pkl")

print("Model trained successfully.")