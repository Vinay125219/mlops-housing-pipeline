import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import mlflow
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
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

# Load data
print("🌸 Loading iris data...")
data = load_iris(as_frame=True)
df = data.frame
X = df.drop("target", axis=1)
y = df["target"]

# Use smaller test size for faster training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42  # Reduced from 0.5 to 0.2
)

# Create models directory if not exists
os.makedirs("models", exist_ok=True)
os.makedirs("mlruns", exist_ok=True)

def train_and_log_model(model, model_name):
    try:
        with mlflow.start_run(run_name=model_name) as run:
            print(f"🚀 Training {model_name}...")
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            acc = accuracy_score(y_test, preds)
            f1 = f1_score(y_test, preds, average="weighted")

            mlflow.log_param("model_name", model_name)
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1_score", f1)

            signature = infer_signature(X_test, preds)
            input_example = X_test.head(1)  # Reduced from 2 to 1

            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                input_example=input_example,
                signature=signature
            )

            # Save locally
            joblib.dump(model, f"models/{model_name}.pkl")

            print(f"✅ {model_name} | Accuracy: {acc:.3f} | F1 Score: {f1:.3f} | Saved to models/{model_name}.pkl")

            # Optional registration (skip in CI to avoid permission issues)
            if model_name == "RandomForest" and not os.getenv('CI'):
                try:
                    mlflow.register_model(
                        model_uri=f"runs:/{run.info.run_id}/model",
                        name="IrisClassifierModel"
                    )
                    print("📝 Model registered in MLflow Model Registry")
                except Exception as reg_error:
                    print(f"⚠️ Model registration failed: {reg_error}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error training {model_name}: {e}")
        # Fallback: just save the model locally without MLflow
        try:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            f1 = f1_score(y_test, preds, average="weighted")
            
            joblib.dump(model, f"models/{model_name}.pkl")
            print(f"✅ {model_name} | Accuracy: {acc:.3f} | F1 Score: {f1:.3f} | Saved to models/{model_name}.pkl (fallback)")
            return True
        except Exception as fallback_error:
            print(f"❌ Fallback also failed for {model_name}: {fallback_error}")
            return False

print("🎯 Starting iris model training...")
print("=" * 50)

# Train models with optimized parameters for speed
success1 = train_and_log_model(LogisticRegression(max_iter=100, random_state=42), "LogisticRegression")  # Reduced max_iter from 200 to 100
success2 = train_and_log_model(RandomForestClassifier(n_estimators=50, random_state=42), "RandomForest")  # Reduced n_estimators from 100 to 50

if success1 and success2:
    print("\n🎉 All iris models trained successfully!")
    print("📁 Models saved in: models/")
    print("📊 MLflow runs saved in: mlruns/")
else:
    print("\n⚠️ Some iris models failed to train. Check logs above.")
    sys.exit(1)
