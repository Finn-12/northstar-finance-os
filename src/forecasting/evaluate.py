import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, r2_score

project_root = Path(__file__).resolve().parents[2]

df = pd.read_csv(
    project_root / "src" / "data" / "raw" / "project_forecast.csv"
)
df = df.dropna(subset=["cost", "revenue"])

X = df[["cost"]]
target = df["revenue"]

model = joblib.load(project_root / "models" / "revenue_model.pkl")
predictions = model.predict(X)

print("Training-set MAE:", mean_absolute_error(target, predictions))
print("Training-set R2:", r2_score(target, predictions))
