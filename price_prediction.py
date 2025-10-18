import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

df = pd.read_parquet('myntra_cleaned.parquet')
df = df[(df['original_price']>0)&(df['discounted_price']>0)]
X = df[['brand','gender','category','fabric','pattern','color','rating_count','discount_percent']]
y = df['original_price']
y = np.log1p(df['original_price'])

pre = ColumnTransformer([
  ('cat', OneHotEncoder(handle_unknown='ignore', min_frequency=100), ['brand','gender','category','fabric','pattern','color']),
  ('passthrough', 'passthrough', ['rating_count','discount_percent'])
])
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
rf = XGBRegressor(
    n_estimators=100,
    tree_method="hist",   # use hist + device=cuda for GPU
    device="cuda",        # runs on GPU
    random_state=42
)
from sklearn.pipeline import Pipeline
pipe = Pipeline([('pre', pre), ('rf', rf)]).fit(Xtr, ytr)
predictions = pipe.predict(Xte)
rmse = np.sqrt(mean_squared_error(np.expm1(yte), np.expm1(predictions)))
print('RMSE:', int(rmse))

# Persist the trained pipeline for API usage
os.makedirs('artifacts', exist_ok=True)
model_path = os.path.join('artifacts', 'price_model.joblib')
joblib.dump({'pipeline': pipe}, model_path)
print(f'Saved model to {model_path}')