# Production Deployment Fix Guide

This guide addresses the production deployment issues and provides step-by-step solutions.

## Issues Identified

### 1. Test Script Configuration
**Problem**: The test script was trying to test both housing API (port 8000) and iris API (port 8001), but only the housing API is configured in the Dockerfile.

**Solution**: Updated `scripts/test_api.py` to only test the housing API since that's what's configured in the Dockerfile.

### 2. CI/CD Pipeline Improvements
**Problem**: The Docker testing in the CI/CD pipeline was insufficient and could fail silently.

**Solution**: Enhanced the Docker testing with:
- Longer wait time for API startup (15 seconds)
- More comprehensive API testing
- Better error handling

### 3. Missing Dependencies
**Problem**: The `requests` library wasn't installed in the CI/CD environment.

**Solution**: Added `requests` to the pip install command in the workflow.

## Fixed Files

### 1. Updated Test Script (`scripts/test_api.py`)
- Removed iris API testing
- Focused only on housing API testing
- Improved error handling

### 2. Enhanced CI/CD Pipeline (`.github/workflows/ci-cd.yml`)
- Added `requests` to dependencies
- Improved Docker testing with comprehensive API checks
- Better error handling and logging

## Production Deployment Steps

### Step 1: Verify Local Setup

```bash
# Test the API locally
python -m uvicorn api.housing_api:app --host 0.0.0.0 --port 8000

# In another terminal, test the API
python scripts/test_api.py
```

### Step 2: Check GitHub Secrets

Ensure these secrets are set in your GitHub repository:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token

### Step 3: Push Changes to Trigger Pipeline

```bash
git add .
git commit -m "Fix production deployment issues"
git push origin main
```

### Step 4: Monitor the Pipeline

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Monitor the workflow execution
4. Check for any errors in the logs

### Step 5: Deploy to Production

Once the pipeline succeeds:

```bash
# Pull the latest image
docker pull YOUR_DOCKER_USERNAME/mlops-app:latest

# Run the container
docker run -p 8000:8000 YOUR_DOCKER_USERNAME/mlops-app:latest
```

## Testing the Deployment

### Health Check
```bash
curl http://localhost:8000/
```

Expected response:
```json
{"message": "Housing price prediction API is running."}
```

### Prediction Test
```bash
curl -X POST http://localhost:8000/predict \
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

Expected response:
```json
{"predicted_price": 4.860650727272711}
```

### Metrics Check
```bash
curl http://localhost:8000/metrics
```

Expected response:
```json
{"total_predictions": 1}
```

## Troubleshooting

### Issue 1: Docker Build Fails
**Symptoms**: Docker build errors in CI/CD pipeline
**Solutions**:
- Check if Docker Hub credentials are correct
- Verify Dockerfile syntax
- Ensure all required files are present

### Issue 2: API Tests Fail
**Symptoms**: API endpoints not responding
**Solutions**:
- Check if models were trained successfully
- Verify API server starts correctly
- Check port conflicts

### Issue 3: Container Won't Start
**Symptoms**: Docker container exits immediately
**Solutions**:
- Check container logs: `docker logs CONTAINER_ID`
- Verify all dependencies are installed
- Check if model files exist in the container

### Issue 4: Prediction Errors
**Symptoms**: API returns errors for predictions
**Solutions**:
- Verify model files are loaded correctly
- Check input data format
- Ensure all required features are provided

## Production Best Practices

### 1. Environment Variables
Consider using environment variables for configuration:

```bash
docker run -p 8000:8000 \
  -e MODEL_PATH=/app/models/DecisionTree.pkl \
  -e LOG_LEVEL=INFO \
  YOUR_DOCKER_USERNAME/mlops-app:latest
```

### 2. Health Checks
The API includes basic health checks:
- `GET /`: Basic health check
- `GET /metrics`: Performance metrics

### 3. Logging
The API logs all predictions to:
- File: `housinglogs/predictions.log`
- Database: `housinglogs/predictions.db`

### 4. Monitoring
Monitor the application using:
- Container logs: `docker logs CONTAINER_ID`
- API metrics: `GET /metrics`
- Application logs in the container

## Success Criteria

Your deployment is successful when:

✅ **Pipeline Completes**: All CI/CD jobs pass
✅ **Docker Image Builds**: Image is created and pushed to Docker Hub
✅ **Container Runs**: Container starts without errors
✅ **API Responds**: Health check endpoint returns success
✅ **Predictions Work**: Prediction endpoint returns valid results
✅ **Logs Generated**: Prediction logs are created

## Next Steps

After successful deployment:

1. **Monitor Performance**: Track API response times and accuracy
2. **Scale Infrastructure**: Consider Kubernetes for production scaling
3. **Add Monitoring**: Implement comprehensive logging and monitoring
4. **Security Hardening**: Regular security audits and updates
5. **Documentation**: Keep deployment guides updated

---

**Note**: This fix addresses the immediate deployment issues. For production use, consider implementing additional security measures, monitoring, and scaling solutions. 