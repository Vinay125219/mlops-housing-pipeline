import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Load preprocessed data
df = pd.read_csv("data/housing.csv")
X = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create models directory if not exists
os.makedirs("models", exist_ok=True)

def train_and_save_model(model, model_name):
    print(f"Training {model_name}...")
    
    # Train the model
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Calculate metrics
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    # Save model locally
    joblib.dump(model, f"models/{model_name}.pkl")

    print(f"SUCCESS: {model_name} | MSE: {mse:.3f} | R2 Score: {r2:.3f} | Saved to models/{model_name}.pkl")
    
    return mse, r2

# Train models
print("Starting Housing Model Training...")
print("=" * 50)

mse1, r2_1 = train_and_save_model(LinearRegression(), "LinearRegression")
mse2, r2_2 = train_and_save_model(DecisionTreeRegressor(max_depth=5), "DecisionTree")

print("=" * 50)
print("📊 Training Summary:")
print(f"Linear Regression - MSE: {mse1:.3f}, R²: {r2_1:.3f}")
print(f"Decision Tree - MSE: {mse2:.3f}, R²: {r2_2:.3f}")
print("SUCCESS: All models saved successfully!") 