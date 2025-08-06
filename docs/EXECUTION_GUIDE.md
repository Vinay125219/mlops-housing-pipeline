# Complete MLOps Pipeline Execution Guide

## 🎯 Overview

This guide provides a **step-by-step walkthrough** of the complete MLOps pipeline, covering all five phases: Build, Track, Package, Deploy, and Monitor. Each step includes detailed explanations, commands, and expected outputs.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **Docker**: Latest version
- **Git**: For version control
- **Memory**: At least 4GB RAM
- **Storage**: 2GB free space

### Software Installation

**1. Python Environment**
```bash
# Check Python version
python --version
# Should show Python 3.10.x or higher

# Create virtual environment (recommended)
python -m venv mlops-env
source mlops-env/bin/activate  # On Windows: mlops-env\Scripts\activate
```

**2. Docker Installation**
```bash
# Check Docker installation
docker --version
# Should show Docker version 20.x or higher

# Test Docker
docker run hello-world
```

## 🚀 Phase-by-Phase Execution

### Phase 1: Build - Data Processing & Model Training

#### Step 1.1: Environment Setup

**1. Clone and Navigate**
```bash
# Clone the repository (replace with your actual repo URL)
git clone <your-repository-url>
cd mlops-housing-pipeline

# Verify project structure
ls -la
```

**Expected Output:**
```
total 20
drwxr-xr-x  5 user user 4096 Jan 15 10:00 .
drwxr-xr-x  3 user user 4096 Jan 15 10:00 ..
drwxr-xr-x  2 user user 4096 Jan 15 10:00 api
drwxr-xr-x  2 user user 4096 Jan 15 10:00 data
drwxr-xr-x  2 user user 4096 Jan 15 10:00 src
-rw-r--r--  1 user user  200 Jan 15 10:00 requirements.txt
-rw-r--r--  1 user user 1000 Jan 15 10:00 README.md
```

**2. Install Dependencies**
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import mlflow, fastapi, sklearn; print('✅ All dependencies installed')"
```

**Expected Output:**
```
Collecting fastapi
  Downloading fastapi-0.104.1-py3-none-any.whl (61 kB)
...
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 mlflow-2.8.1 ...
✅ All dependencies installed
```

#### Step 1.2: Data Processing

**1. Load and Preprocess Data**
```bash
# Run data preprocessing script
python src/load_data.py
```

**Expected Output:**
```
✅ Preprocessed data saved to data/housing.csv
```

**2. Verify Data Processing**
```bash
# Check the processed data
python -c "
import pandas as pd
df = pd.read_csv('data/housing.csv')
print(f'Dataset shape: {df.shape}')
print(f'Features: {list(df.columns[:-1])}')
print(f'Target: {df.columns[-1]}')
print(f'First 3 rows:')
print(df.head(3))
"
```

**Expected Output:**
```
Dataset shape: (20640, 9)
Features: ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
Target: MedHouseVal
First 3 rows:
   MedInc  HouseAge  AveRooms  AveBedrms  Population  AveOccup  Latitude  Longitude  MedHouseVal
0  -0.941   -0.941    -0.941     -0.941      -0.941    -0.941    -0.941     -0.941         4.526
1  -0.941   -0.941    -0.941     -0.941      -0.941    -0.941    -0.941     -0.941         3.585
2  -0.941   -0.941    -0.941     -0.941      -0.941    -0.941    -0.941     -0.941         3.521
```

#### Step 1.3: Model Training

**1. Train Housing Regression Models**
```bash
# Train models with MLflow tracking
python src/train_and_track.py
```

**Expected Output:**
```
✅ LinearRegression | MSE: 0.524 | R2 Score: 0.476 | Saved to models/LinearRegression.pkl
✅ DecisionTree | MSE: 0.412 | R2 Score: 0.588 | Saved to models/DecisionTree.pkl
```

**2. Train Iris Classification Models**
```bash
# Train classification models
python src/train_iris.py
```

**Expected Output:**
```
✅ LogisticRegression | Accuracy: 0.960 | F1 Score: 0.960 | Saved to models/LogisticRegression.pkl
✅ RandomForest | Accuracy: 0.973 | F1 Score: 0.973 | Saved to models/RandomForest.pkl
```

**3. Verify Model Files**
```bash
# Check saved models
ls -la models/
```

**Expected Output:**
```
total 200
-rw-r--r-- 1 user user 50000 Jan 15 10:30 DecisionTree.pkl
-rw-r--r-- 1 user user 50000 Jan 15 10:30 LinearRegression.pkl
-rw-r--r-- 1 user user 50000 Jan 15 10:30 LogisticRegression.pkl
-rw-r--r-- 1 user user 50000 Jan 15 10:30 RandomForest.pkl
```

### Phase 2: Track - Experiment Management

#### Step 2.1: MLflow UI Setup

**1. Start MLflow UI**
```bash
# Start MLflow tracking server
mlflow ui --port 5000
```

**Expected Output:**
```
[2024-01-15 10:35:12 +0000] [INFO] Starting gunicorn 20.1.0
[2024-01-15 10:35:12 +0000] [INFO] Listening at: http://127.0.0.1:5000
[2024-01-15 10:35:12 +0000] [INFO] Using worker: sync
```

**2. Access MLflow UI**
- Open browser and navigate to: `http://localhost:5000`
- You should see experiment runs with metrics and artifacts

**3. Explore MLflow Features**
```bash
# List experiments
mlflow experiments list

# Get run details
mlflow runs list --experiment-id 0
```

#### Step 2.2: Model Registry

**1. Check Model Registry**
```bash
# List registered models
mlflow models list
```

**Expected Output:**
```
Name                    Version  Stage
----------------------  -------  ------
IrisClassifierModel     1        None
```

**2. Model Details**
```bash
# Get model version details
mlflow models describe --name IrisClassifierModel --version 1
```

### Phase 3: Package - API Development

#### Step 3.1: API Testing

**1. Start Housing API**
```bash
# Start the housing prediction API
uvicorn api.housing_api:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**2. Test API Health**
```bash
# Test health endpoint
curl http://localhost:8000/
```

**Expected Output:**
```json
{"message": "Housing price prediction API is running."}
```

**3. Test Prediction Endpoint**
```bash
# Make a prediction request
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

**Expected Output:**
```json
{"predicted_price": 2.847}
```

**4. Check Metrics**
```bash
# Get API metrics
curl http://localhost:8000/metrics
```

**Expected Output:**
```json
{"total_predictions": 1}
```

#### Step 3.2: Iris API Testing

**1. Start Iris API (in new terminal)**
```bash
# Start iris classification API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8001
```

**2. Test Iris Prediction**
```bash
# Test iris classification
curl -X POST "http://localhost:8001/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "sepal_length": 5.1,
       "sepal_width": 3.5,
       "petal_length": 1.4,
       "petal_width": 0.2
     }'
```

**Expected Output:**
```json
{"predicted_class": 0}
```

### Phase 4: Deploy - Containerization

#### Step 4.1: Docker Build

**1. Build Docker Image**
```bash
# Build the Docker image
docker build -t mlops-housing-api .
```

**Expected Output:**
```
Sending build context to Docker daemon  15.36MB
Step 1/7 : FROM python:3.10-slim
 ---> abc123def456
Step 2/7 : WORKDIR /app
 ---> Running in def456ghi789
Step 3/7 : COPY . .
 ---> Running in ghi789jkl012
Step 4/7 : RUN mkdir -p housinglogs
 ---> Running in jkl012mno345
Step 5/7 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in mno345pqr678
Step 6/7 : EXPOSE 8000
 ---> Running in pqr678stu901
Step 7/7 : CMD ["uvicorn", "api.housing_api:app", "--host", "0.0.0.0", "--port", "8000"]
 ---> Running in stu901vwx234
Successfully built abc123def456
Successfully tagged mlops-housing-api:latest
```

**2. Verify Docker Image**
```bash
# List Docker images
docker images | grep mlops-housing-api
```

**Expected Output:**
```
mlops-housing-api   latest   abc123def456   2 minutes ago   500MB
```

#### Step 4.2: Docker Deployment

**1. Run Container**
```bash
# Run the containerized API
docker run -d -p 8000:8000 --name mlops-api mlops-housing-api
```

**Expected Output:**
```
abc123def456
```

**2. Verify Container Status**
```bash
# Check container status
docker ps | grep mlops-api
```

**Expected Output:**
```
CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS         PORTS                    NAMES
abc123def456   mlops-housing-api  "uvicorn api.housing_…"   2 minutes ago   Up 2 minutes   0.0.0.0:8000->8000/tcp   mlops-api
```

**3. Test Containerized API**
```bash
# Test the containerized API
curl http://localhost:8000/
```

**Expected Output:**
```json
{"message": "Housing price prediction API is running."}
```

**4. Test Prediction in Container**
```bash
# Make prediction through container
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "total_rooms": 6.0,
       "total_bedrooms": 2.0,
       "population": 800.0,
       "households": 400.0,
       "median_income": 4.0,
       "housing_median_age": 30.0,
       "latitude": 37.7749,
       "longitude": -122.4194
     }'
```

**Expected Output:**
```json
{"predicted_price": 3.124}
```

### Phase 5: Monitor - Logging and Metrics

#### Step 5.1: Log Analysis

**1. Check Log Files**
```bash
# View prediction logs
tail -f housinglogs/predictions.log
```

**Expected Output:**
```
2024-01-15 10:45:23,456 - INFO - Input: {'total_rooms': 8.0, 'total_bedrooms': 3.0, ...} | Prediction: 2.847
2024-01-15 10:46:12,789 - INFO - Input: {'total_rooms': 6.0, 'total_bedrooms': 2.0, ...} | Prediction: 3.124
```

**2. Check Database Logs**
```bash
# Query SQLite database
sqlite3 housinglogs/predictions.db "SELECT * FROM housinglogs ORDER BY timestamp DESC LIMIT 5;"
```

**Expected Output:**
```
1|2024-01-15T10:46:12.789|{'total_rooms': 6.0, 'total_bedrooms': 2.0, ...}|3.124
2|2024-01-15T10:45:23.456|{'total_rooms': 8.0, 'total_bedrooms': 3.0, ...}|2.847
```

#### Step 5.2: Performance Monitoring

**1. API Performance Test**
```bash
# Test API response time
time curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "total_rooms": 5.0,
       "total_bedrooms": 2.0,
       "population": 600.0,
       "households": 300.0,
       "median_income": 3.0,
       "housing_median_age": 25.0,
       "latitude": 37.7749,
       "longitude": -122.4194
     }'
```

**Expected Output:**
```json
{"predicted_price": 2.891}
real    0m0.045s
user    0m0.002s
sys     0m0.003s
```

**2. Load Testing (Optional)**
```bash
# Install Apache Bench if available
# sudo apt-get install apache2-utils  # Ubuntu/Debian
# brew install httpd  # macOS

# Run load test
ab -n 100 -c 10 -p test_data.json -T application/json http://localhost:8000/predict/
```

## 🔧 Advanced Operations

### Model Retraining

**1. Retrain with New Parameters**
```bash
# Modify training script to try different hyperparameters
python src/train_and_track.py
```

**2. Compare Model Versions**
```bash
# Compare different model runs in MLflow UI
# Navigate to http://localhost:5000 and compare runs
```

### API Scaling

**1. Multiple Container Instances**
```bash
# Run multiple containers for load balancing
docker run -d -p 8001:8000 --name mlops-api-1 mlops-housing-api
docker run -d -p 8002:8000 --name mlops-api-2 mlops-housing-api
docker run -d -p 8003:8000 --name mlops-api-3 mlops-housing-api
```

**2. Docker Compose (Optional)**
```yaml
# docker-compose.yml
version: '3.8'
services:
  mlops-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./housinglogs:/app/housinglogs
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000
```

### Monitoring Dashboard

**1. Real-time Metrics**
```bash
# Monitor API metrics in real-time
watch -n 5 'curl -s http://localhost:8000/metrics'
```

**2. Log Monitoring**
```bash
# Monitor logs in real-time
tail -f housinglogs/predictions.log | grep -E "(ERROR|WARNING)"
```

## 🚨 Troubleshooting

### Common Issues and Solutions

**1. Port Already in Use**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn api.housing_api:app --port 8001
```

**2. Docker Permission Issues**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Restart Docker service
sudo systemctl restart docker
```

**3. MLflow Connection Issues**
```bash
# Check MLflow server
ps aux | grep mlflow

# Restart MLflow
pkill mlflow
mlflow ui --port 5000
```

**4. Model Loading Errors**
```bash
# Verify model files exist
ls -la models/

# Check model file integrity
python -c "import joblib; model = joblib.load('models/DecisionTree.pkl'); print('Model loaded successfully')"
```

**5. API Connection Refused**
```bash
# Check if API is running
curl http://localhost:8000/

# Check container logs
docker logs mlops-api

# Restart container
docker restart mlops-api
```

### Debug Commands

**1. System Information**
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Docker version
docker --version
```

**2. Network Connectivity**
```bash
# Test localhost connectivity
curl http://localhost:8000/

# Test Docker container connectivity
docker exec mlops-api curl http://localhost:8000/
```

**3. Resource Usage**
```bash
# Check CPU and memory usage
top

# Check disk space
df -h

# Check Docker resource usage
docker stats
```

## 📊 Performance Benchmarks

### Expected Performance Metrics

**1. Model Training Time**
- Linear Regression: ~2-5 seconds
- Decision Tree: ~5-10 seconds
- Random Forest: ~10-20 seconds

**2. API Response Time**
- Single prediction: <100ms
- Batch prediction: <500ms per request

**3. Memory Usage**
- Training: ~500MB RAM
- API serving: ~200MB RAM per container
- MLflow UI: ~100MB RAM

**4. Storage Requirements**
- Models: ~50MB total
- Logs: ~10MB per 10,000 predictions
- MLflow artifacts: ~100MB

## 🎯 Success Criteria

### Phase Completion Checklist

**✅ Phase 1: Build**
- [ ] Data preprocessing completed
- [ ] Models trained successfully
- [ ] Performance metrics logged
- [ ] Model files saved locally

**✅ Phase 2: Track**
- [ ] MLflow UI accessible
- [ ] Experiments tracked
- [ ] Model artifacts stored
- [ ] Model registry populated

**✅ Phase 3: Package**
- [ ] API endpoints responding
- [ ] Predictions working correctly
- [ ] Input validation functional
- [ ] Error handling implemented

**✅ Phase 4: Deploy**
- [ ] Docker image built successfully
- [ ] Container running properly
- [ ] API accessible through container
- [ ] Predictions working in container

**✅ Phase 5: Monitor**
- [ ] Logs being written
- [ ] Database storing predictions
- [ ] Metrics endpoint responding
- [ ] Performance monitoring active

## 🚀 Next Steps

After completing this execution guide, you have a **fully functional MLOps pipeline** with:

1. **Automated Data Processing**: Clean, scalable data pipeline
2. **Experiment Tracking**: Complete MLflow integration
3. **Model Deployment**: Production-ready API
4. **Containerization**: Docker-based deployment
5. **Monitoring**: Comprehensive logging and metrics

**Recommended next steps:**
1. **CI/CD Integration**: Set up GitHub Actions for automated deployment
2. **Advanced Monitoring**: Implement Prometheus + Grafana
3. **Model A/B Testing**: Deploy multiple model versions
4. **Auto-scaling**: Implement Kubernetes deployment
5. **Security**: Add authentication and authorization

---

**Congratulations! You've successfully implemented a complete MLOps pipeline following industry best practices.** 