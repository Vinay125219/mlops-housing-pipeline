import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib
import os

# Load data
data = load_iris(as_frame=True)
df = data.frame
X = df.drop("target", axis=1)
y = df["target"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=42
)

# Create models directory if not exists
os.makedirs("models", exist_ok=True)

def train_and_save_model(model, model_name):
    print(f"Training {model_name}...")
    
    # Train the model
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Calculate metrics
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="weighted")

    # Save model locally
    joblib.dump(model, f"models/{model_name}.pkl")

    print(f"SUCCESS: {model_name} | Accuracy: {acc:.3f} | F1 Score: {f1:.3f} | Saved to models/{model_name}.pkl")
    
    return acc, f1

# Train models
print("Starting Iris Model Training...")
print("=" * 50)

acc1, f1_1 = train_and_save_model(LogisticRegression(max_iter=200), "LogisticRegression")
acc2, f1_2 = train_and_save_model(RandomForestClassifier(n_estimators=100), "RandomForest")

print("=" * 50)
print("📊 Training Summary:")
print(f"Logistic Regression - Accuracy: {acc1:.3f}, F1: {f1_1:.3f}")
print(f"Random Forest - Accuracy: {acc2:.3f}, F1: {f1_2:.3f}")
print("SUCCESS: All models saved successfully!") 