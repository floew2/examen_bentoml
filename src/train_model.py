import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import bentoml

# 1. Load the processed data
X_train = pd.read_csv("data/processed/X_train.csv")
X_test = pd.read_csv("data/processed/X_test.csv")
y_train = pd.read_csv("data/processed/y_train.csv")
y_test = pd.read_csv("data/processed/y_test.csv")

# 2. Train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# 3. Evaluate performance
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"✅ RMSE: {rmse:.4f}")
print(f"✅ R² Score: {r2:.4f}")

# 4. Save the model using BentoML
model_ref = bentoml.sklearn.save_model("admissions_regression", model)
print(f"✅ Model saved: {model_ref}")
