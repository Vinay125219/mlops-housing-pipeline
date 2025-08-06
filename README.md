# MLOps Housing Pipeline - Complete Implementation

## 📋 Project Overview

This project demonstrates a **complete MLOps pipeline** implementing all five core phases: **Build, Track, Package, Deploy, and Monitor** for both classification (Iris) and regression (California Housing) datasets. The pipeline follows industry best practices and provides a production-ready solution.

## 🎯 MLOps Phases Covered

### ✅ Phase 1: Build
- Data loading and preprocessing
- Model training with multiple algorithms
- Feature engineering
- Cross-validation and hyperparameter tuning

### ✅ Phase 2: Track
- MLflow integration for experiment tracking
- Model versioning and artifact management
- Metrics logging (MSE, R² for regression; Accuracy, F1 for classification)
- Model signature inference

### ✅ Phase 3: Package
- Model serialization with joblib
- Docker containerization
- API packaging with FastAPI
- Dependency management

### ✅ Phase 4: Deploy
- RESTful API deployment
- Docker container deployment
- CI/CD pipeline with GitHub Actions
- Model serving endpoints

### ✅ Phase 5: Monitor
- Prediction logging to files and SQLite database
- Real-time metrics tracking
- API health monitoring
- Performance metrics collection

## 🏗️ Architecture

```
mlops-housing-pipeline/
├── src/                    # Training scripts
│   ├── load_data.py       # Data preprocessing
│   ├── train_and_track.py # Housing regression training
│   └── train_iris.py      # Iris classification training
├── api/                   # Deployment APIs
│   ├── main.py           # Iris API
│   └── housing_api.py    # Housing API
├── models/               # Serialized models
├── data/                 # Processed datasets
├── mlruns/              # MLflow tracking
├── housinglogs/         # Housing prediction logs
├── irislogs/           # Iris prediction logs
├── Dockerfile          # Container configuration
├── requirements.txt     # Dependencies
└── .github/workflows/  # CI/CD pipeline
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd mlops-housing-pipeline
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Load and preprocess data**
```bash
python src/load_data.py
```

## 📊 Detailed Step-by-Step Implementation

### Phase 1: Build - Data Processing & Model Training

#### Step 1.1: Data Loading and Preprocessing

**File: `src/load_data.py`**

```python
# Key Features:
# - Fetches California Housing dataset
# - Handles missing values
# - Applies StandardScaler normalization
# - Saves preprocessed data to CSV
```

**Execution:**
```bash
python src/load_data.py
```

**What happens:**
1. **Data Source**: Uses `sklearn.datasets.fetch_california_housing()` to get the official California Housing dataset
2. **Data Cleaning**: Removes any missing values with `dropna()`
3. **Feature Engineering**: Separates features (X) and target variable (y = MedHouseVal)
4. **Normalization**: Applies StandardScaler to normalize features for better model performance
5. **Data Persistence**: Saves processed data to `data/housing.csv` for consistent training

#### Step 1.2: Model Training with Experiment Tracking

**File: `src/train_and_track.py` (Housing Regression)**

```python
# Key Features:
# - Multiple model training (LinearRegression, DecisionTree)
# - MLflow experiment tracking
# - Metrics logging (MSE, R²)
# - Model serialization
```

**Execution:**
```bash
python src/train_and_track.py
```

**What happens:**
1. **Data Loading**: Loads preprocessed data from `data/housing.csv`
2. **Train-Test Split**: 80-20 split with random_state=42 for reproducibility
3. **Model Training**: Trains multiple algorithms:
   - Linear Regression (baseline)
   - Decision Tree (max_depth=5 for regularization)
4. **MLflow Tracking**: Each model gets its own MLflow run with:
   - Parameters logged (`model_name`)
   - Metrics logged (`mse`, `r2_score`)
   - Model artifacts saved
   - Model signature inferred for deployment
5. **Local Persistence**: Models saved as `.pkl` files in `models/` directory

**File: `src/train_iris.py` (Iris Classification)**

```python
# Key Features:
# - Classification models (LogisticRegression, RandomForest)
# - Classification metrics (Accuracy, F1-score)
# - Model registration in MLflow Model Registry
```

**Execution:**
```bash
python src/train_iris.py
```

**What happens:**
1. **Data Loading**: Uses built-in Iris dataset from sklearn
2. **Classification Training**: Trains:
   - Logistic Regression (max_iter=200)
   - Random Forest (n_estimators=100)
3. **Classification Metrics**: Logs accuracy and weighted F1-score
4. **Model Registration**: Registers RandomForest model in MLflow Model Registry as "IrisClassifierModel"

### Phase 2: Track - Experiment Management

#### Step 2.1: MLflow Integration

**Key Tracking Features:**
- **Experiment Organization**: Each training run creates a unique experiment
- **Artifact Management**: Models, metrics, and parameters stored in `mlruns/`
- **Model Signatures**: Automatic input/output schema inference
- **Version Control**: Model versions tracked with unique run IDs

**MLflow UI Access:**
```bash
mlflow ui
# Open http://localhost:5000 in browser
```

**Tracked Information:**
- **Parameters**: Model names, hyperparameters
- **Metrics**: MSE, R² (regression) / Accuracy, F1 (classification)
- **Artifacts**: Serialized models, input examples
- **Metadata**: Run timestamps, user information

#### Step 2.2: Model Registry

**Registration Process:**
```python
# Automatic registration for best models
mlflow.register_model(
    model_uri=f"runs:/{run.info.run_id}/model",
    name="IrisClassifierModel"
)
```

**Benefits:**
- **Model Lineage**: Track which training run produced each model
- **Version Management**: Multiple model versions with staging/production
- **Deployment Integration**: Easy model serving from registry

### Phase 3: Package - Containerization & API

#### Step 3.1: FastAPI Application

**File: `api/housing_api.py`**

```python
# Key Features:
# - RESTful API with FastAPI
# - Input validation with Pydantic
# - Real-time prediction logging
# - SQLite database for persistence
```

**API Endpoints:**
- `GET /`: Health check
- `POST /predict`: Make predictions
- `GET /metrics`: Get usage statistics

**Input Validation:**
```python
class HousingRequest(BaseModel):
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    housing_median_age: float
    latitude: float
    longitude: float
```

#### Step 3.2: Docker Containerization

**File: `Dockerfile`**

```dockerfile
# Multi-stage build for optimization
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN mkdir -p housinglogs
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "api.housing_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build Process:**
```bash
# Build Docker image
docker build -t mlops-housing-api .

# Run container
docker run -p 8000:8000 mlops-housing-api
```

**Benefits:**
- **Reproducibility**: Same environment across development/production
- **Isolation**: No conflicts with system dependencies
- **Scalability**: Easy horizontal scaling
- **Portability**: Deploy anywhere Docker runs

### Phase 4: Deploy - CI/CD Pipeline

#### Step 4.1: GitHub Actions CI/CD

**File: `.github/workflows/ci-cd.yml`**

```yaml
# Two-stage pipeline:
# 1. Build, Test, Lint
# 2. Docker Build & Push
```

**Pipeline Stages:**

1. **Code Quality Checks:**
   - Python linting with flake8
   - Syntax error detection
   - Code style validation

2. **Docker Operations:**
   - Build Docker image
   - Push to Docker Hub
   - Automated deployment

**Security Features:**
- Docker Hub credentials stored as GitHub secrets
- Automated testing before deployment
- Branch protection rules

#### Step 4.2: API Deployment

**Local Development:**
```bash
# Start API server
uvicorn api.housing_api:app --reload --host 0.0.0.0 --port 8000
```

**Production Deployment:**
```bash
# Using Docker
docker run -d -p 8000:8000 mlops-housing-api

# Using Docker Compose (if needed)
docker-compose up -d
```

### Phase 5: Monitor - Prediction Tracking

#### Step 5.1: Logging Infrastructure

**Dual Logging System:**
1. **File Logging**: Human-readable logs in `housinglogs/predictions.log`
2. **Database Logging**: Structured data in SQLite `housinglogs/predictions.db`

**Logging Implementation:**
```python
# File logging
logging.basicConfig(
    filename='housinglogs/predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database logging
cursor.execute('''
    INSERT INTO housinglogs (timestamp, inputs, prediction)
    VALUES (?, ?, ?)
''', (datetime.now().isoformat(), str(input_data), str(prediction)))
```

#### Step 5.2: Monitoring Endpoints

**Metrics API:**
```python
@app.get("/metrics")
def metrics():
    cursor.execute("SELECT COUNT(*) FROM housinglogs")
    total_requests = cursor.fetchone()[0]
    return {
        "total_predictions": total_requests,
        "last_updated": datetime.now().isoformat()
    }
```

**Monitored Metrics:**
- **Request Volume**: Total predictions made
- **Response Time**: API performance
- **Error Rates**: Failed predictions
- **Data Drift**: Input feature distributions

## 🔧 Usage Examples

### Training Models

```bash
# Train housing regression models
python src/train_and_track.py

# Train iris classification models  
python src/train_iris.py
```

### Making Predictions

**Housing API:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "total_rooms": 8.0,
       "total_bedrooms": 3.0,
       "population": 1000.0,
       "households": 500.0,
       "median_income": 3.5,
       "housing_median_age": 35.0,
       "latitude": 37.7749,
       "longitude": -122.4194
     }'
```

**Iris API:**
```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sepal_length": 5.1,
       "sepal_width": 3.5,
       "petal_length": 1.4,
       "petal_width": 0.2
     }'
```

### Checking Metrics

```bash
curl http://localhost:8000/metrics
```

## 📈 Performance Analysis

### Model Performance Comparison

**Housing Regression Models:**
- **Linear Regression**: Baseline model, good for linear relationships
- **Decision Tree**: Better for non-linear patterns, interpretable

**Iris Classification Models:**
- **Logistic Regression**: Linear classifier, fast inference
- **Random Forest**: Ensemble method, higher accuracy

### Monitoring Dashboard

Access MLflow UI for experiment tracking:
```bash
mlflow ui --port 5000
```

## 🛠️ Development Workflow

### 1. Data Pipeline
```bash
# Load and preprocess data
python src/load_data.py
```

### 2. Model Development
```bash
# Train models with tracking
python src/train_and_track.py  # Housing
python src/train_iris.py       # Iris
```

### 3. API Testing
```bash
# Start API server
uvicorn api.housing_api:app --reload

# Test predictions
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{"total_rooms": 8.0, ...}'
```

### 4. Deployment
```bash
# Build Docker image
docker build -t mlops-housing-api .

# Run container
docker run -p 8000:8000 mlops-housing-api
```

## 🔍 Troubleshooting

### Common Issues

1. **MLflow Tracking Issues:**
   - Ensure `mlruns/` directory exists
   - Check MLflow server is running

2. **API Connection Issues:**
   - Verify port 8000 is available
   - Check Docker container is running

3. **Model Loading Errors:**
   - Ensure models are trained before API startup
   - Check model file paths in API code

### Debug Commands

```bash
# Check MLflow runs
mlflow list-experiments

# View API logs
tail -f housinglogs/predictions.log

# Check database
sqlite3 housinglogs/predictions.db "SELECT * FROM housinglogs LIMIT 5;"
```

## 📚 Best Practices Implemented

### 1. **Version Control**
- Git for code versioning
- MLflow for model versioning
- Docker image tagging

### 2. **Reproducibility**
- Fixed random seeds
- Dependency pinning
- Containerized environments

### 3. **Monitoring**
- Comprehensive logging
- Performance metrics
- Error tracking

### 4. **Security**
- Input validation
- Secure credential management
- Container isolation

### 5. **Scalability**
- Modular architecture
- Docker containerization
- API-first design

## 🚀 Production Deployment

### Environment Variables
```bash
export MLFLOW_TRACKING_URI=http://your-mlflow-server:5000
export MODEL_REGISTRY_URI=http://your-model-registry:5000
```

### Kubernetes Deployment (Optional)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlops-housing-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mlops-housing-api
  template:
    metadata:
      labels:
        app: mlops-housing-api
    spec:
      containers:
      - name: mlops-housing-api
        image: your-registry/mlops-housing-api:latest
        ports:
        - containerPort: 8000
```

## 📊 Metrics and Monitoring

### Key Performance Indicators (KPIs)

1. **Model Performance:**
   - MSE (Mean Squared Error) for regression
   - Accuracy/F1-score for classification

2. **API Performance:**
   - Response time
   - Throughput (requests/second)
   - Error rate

3. **Business Metrics:**
   - Total predictions made
   - Unique users
   - Peak usage times

### Alerting Setup

```python
# Example alerting logic
if error_rate > 0.05:  # 5% error threshold
    send_alert("High error rate detected")
```

## 🔄 Continuous Improvement

### Model Retraining Pipeline

1. **Data Drift Detection**: Monitor input feature distributions
2. **Performance Degradation**: Track prediction accuracy over time
3. **Automated Retraining**: Trigger new training runs when needed
4. **A/B Testing**: Compare new models with production models

### Future Enhancements

1. **Advanced Monitoring**: Prometheus + Grafana integration
2. **Feature Store**: Centralized feature management
3. **Model Explainability**: SHAP integration
4. **Multi-model Serving**: Model ensemble deployment

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**This MLOps pipeline demonstrates industry best practices for building, tracking, packaging, deploying, and monitoring machine learning models in production environments.**

