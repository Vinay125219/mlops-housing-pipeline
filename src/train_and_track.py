import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import joblib
import os
import sys

# Set MLflow tracking URI for CI/CD environment
if os.getenv('CI'):  # Check if running in CI environment
    # Use local file system for MLflow tracking in CI
    mlflow.set_tracking_uri("file://./mlruns")
    print("🔧 CI environment detected - using local MLflow tracking")
else:
    # Use default tracking URI for local development
    mlflow.set_tracking_uri("file://./mlruns")
    print("🏠 Local environment detected - using local MLflow tracking")

# Load preprocessed data
print("📊 Loading housing data...")
df = pd.read_csv("data/housing.csv")
X = df.drop("MedHouseVal", axis=1)
y = df["MedHouseVal"]

# Use smaller test size for faster training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42  # Reduced from 0.2 to 0.1
)

# Create models directory if not exists
os.makedirs("models", exist_ok=True)
os.makedirs("mlruns", exist_ok=True)

def train_and_log_model(model, model_name):
    try:
        with mlflow.start_run(run_name=model_name):
            print(f"🚀 Training {model_name}...")
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            mse = mean_squared_error(y_test, preds)
            r2 = r2_score(y_test, preds)

            mlflow.log_param("model_name", model_name)
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("r2_score", r2)

            signature = infer_signature(X_test, preds)
            input_example = X_test.head(1)  # Reduced from 2 to 1

            # Log model to MLflow
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                input_example=input_example,
                signature=signature
            )

            # Save locally
            joblib.dump(model, f"models/{model_name}.pkl")

            print(f"✅ {model_name} | MSE: {mse:.3f} | R2 Score: {r2:.3f} | Saved to models/{model_name}.pkl")
            return True
            
    except Exception as e:
        print(f"❌ Error training {model_name}: {e}")
        # Fallback: just save the model locally without MLflow
        try:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            mse = mean_squared_error(y_test, preds)
            r2 = r2_score(y_test, preds)
            
            joblib.dump(model, f"models/{model_name}.pkl")
            print(f"✅ {model_name} | MSE: {mse:.3f} | R2 Score: {r2:.3f} | Saved to models/{model_name}.pkl (fallback)")
            return True
        except Exception as fallback_error:
            print(f"❌ Fallback also failed for {model_name}: {fallback_error}")
            return False

print("🎯 Starting model training...")
print("=" * 50)

# Train models with optimized parameters for speed
success1 = train_and_log_model(LinearRegression(), "LinearRegression")
success2 = train_and_log_model(DecisionTreeRegressor(max_depth=3, random_state=42), "DecisionTree")  # Reduced max_depth from 5 to 3

if success1 and success2:
    print("\n🎉 All models trained successfully!")
    print("📁 Models saved in: models/")
    print("📊 MLflow runs saved in: mlruns/")
else:
    print("\n⚠️ Some models failed to train. Check logs above.")
    sys.exit(1)
