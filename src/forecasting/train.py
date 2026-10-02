import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

df = pd.read_csv(
    project_root / "src" / "data" / "raw" / "project_forecast.csv"
)
print(df.columns.tolist())

df = df.dropna(subset=["cost", "revenue"])
X = df[["cost"]]

y = df["revenue"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(
    model,
    project_root / "models" / "revenue_model.pkl"
)

print("Model trained successfully.")