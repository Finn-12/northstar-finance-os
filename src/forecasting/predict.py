import joblib
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
model = joblib.load(
    project_root / "models" / "revenue_model.pkl"
)

sample = pd.DataFrame({
    "cost": [95000]
})

prediction = model.predict(sample)

print(
    f"Forecast Revenue: ${prediction[0]:,.0f}"
)