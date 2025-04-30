import pandas as pd
from sklearn.model_selection import train_test_split
import os

# 1. Load the dataset
data_path = "data/raw/admission.csv"
df = pd.read_csv(data_path)

# 2. Optional cleanup (drop any unnecessary columns)
# If 'Serial No.' exists, drop it as we dont need it for our model
df.drop(columns=["Serial No."], inplace=True, errors="ignore")

# 3. Define features and target
X = df.drop(columns=["Chance of Admit"])
y = df["Chance of Admit"]

# 4. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Save the processed datasets
os.makedirs("data/processed", exist_ok=True)
X_train.to_csv("data/processed/X_train.csv", index=False)
X_test.to_csv("data/processed/X_test.csv", index=False)
y_train.to_csv("data/processed/y_train.csv", index=False)
y_test.to_csv("data/processed/y_test.csv", index=False)

print("✅ Data preparation complete.")
