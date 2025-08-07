# GitHub Repository Setup Guide

This guide will help you set up the GitHub repository and configure the CI/CD pipeline for the MLOps project.

## Prerequisites

1. **GitHub Account**: You need a GitHub account
2. **Docker Hub Account**: For container registry (optional but recommended)
3. **Git**: Installed on your local machine

## Step 1: Create GitHub Repository

### Option A: Create New Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `mlops-housing-pipeline`
   - **Description**: `Complete MLOps pipeline with Build, Track, Package, Deploy, and Monitor phases`
   - **Visibility**: Choose Public or Private
   - **Initialize with**: Check "Add a README file"
5. Click "Create repository"

### Option B: Push Existing Code

If you already have the code locally:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Complete MLOps pipeline implementation"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/mlops-housing-pipeline.git

# Push to GitHub
git push -u origin main
```

## Step 2: Configure GitHub Secrets

For the CI/CD pipeline to work with Docker Hub, you need to set up secrets:

### 2.1 Go to Repository Settings

1. In your GitHub repository, click on "Settings" tab
2. In the left sidebar, click on "Secrets and variables" → "Actions"

### 2.2 Add Docker Hub Credentials

Click "New repository secret" and add:

**DOCKER_USERNAME**
- Name: `DOCKER_USERNAME`
- Value: Your Docker Hub username

**DOCKER_PASSWORD**
- Name: `DOCKER_PASSWORD`
- Value: Your Docker Hub password or access token

### 2.3 Optional: Add Other Secrets

You can also add these if needed:

**MLFLOW_TRACKING_URI** (if using MLflow server)
- Name: `MLFLOW_TRACKING_URI`
- Value: Your MLflow tracking server URL

## Step 3: Verify Repository Structure

Ensure your repository has this structure:

```
mlops-housing-pipeline/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── api/
│   ├── housing_api.py
│   └── main.py
├── data/
│   └── housing.csv.dvc
├── docs/
│   ├── CI_CD_GUIDE.md
│   ├── EXECUTION_GUIDE.md
│   ├── GITHUB_SETUP.md
│   ├── MLOPS_SUMMARY.md
│   └── PHASE_1_BUILD.md
├── models/
├── scripts/
│   ├── test_api.py
│   └── verify_pipeline.py
├── src/
│   ├── load_data.py
│   ├── train_and_track.py
│   ├── train_and_track.py
│   ├── train_iris.py
│   └── train_iris_simple.py
├── Dockerfile
├── README.md
└── requirements.txt
```

## Step 4: Test the CI/CD Pipeline

### 4.1 Push Changes to Trigger Pipeline

```bash
# Make sure you're on the main branch
git checkout main

# Add all changes
git add .

# Commit changes
git commit -m "Update CI/CD pipeline with simplified training scripts"

# Push to trigger the pipeline
git push origin main
```

### 4.2 Monitor the Pipeline

1. Go to your GitHub repository
2. Click on the "Actions" tab
3. You should see the workflow running
4. Click on the workflow to see detailed logs

## Step 5: Verify Pipeline Success

The pipeline should complete these steps:

### ✅ Build-Test-Lint Job
- [ ] Set up Python environment
- [ ] Install dependencies
- [ ] Create necessary directories
- [ ] Run data preprocessing
- [ ] Train models (simplified scripts)
- [ ] Run linting with flake8
- [ ] Test API endpoints
- [ ] Check Dockerfile syntax

### ✅ Security Scan Job
- [ ] Run security scan with Bandit
- [ ] Check for hardcoded secrets

### ✅ Docker Build-Push Job (on main branch)
- [ ] Build Docker image
- [ ] Push to Docker Hub
- [ ] Test Docker container

## Step 6: Troubleshooting Common Issues

### Issue 1: Pipeline Fails on Model Training

**Symptoms**: MLflow permission errors
**Solution**: The simplified training scripts should work. Check logs for specific errors.

### Issue 2: Docker Build Fails

**Symptoms**: Docker-related errors
**Solutions**:
- Ensure Docker Hub credentials are set correctly
- Check if Dockerfile syntax is correct
- Verify Docker Hub repository exists

### Issue 3: API Tests Fail

**Symptoms**: API endpoints not responding
**Solutions**:
- Check if models were trained successfully
- Verify API server starts correctly
- Check port conflicts

### Issue 4: Security Scan Issues

**Symptoms**: Bandit finds security issues
**Solutions**:
- Review the security warnings
- Fix any actual security issues
- Update code to follow security best practices

### Issue 5: Production Deployment Issues

**Symptoms**: Container won't start or API not responding
**Solutions**:
- Check Docker Hub credentials in GitHub secrets
- Verify the Docker image was built successfully
- Use the deployment script: `bash scripts/deploy.sh`
- Check container logs: `docker logs mlops-app`
- Ensure port 8000 is available

## Step 7: Monitor and Maintain

### 7.1 Regular Monitoring

- Check pipeline status regularly
- Monitor Docker Hub for new images
- Review security scan results

### 7.2 Updating the Pipeline

To update the pipeline:

1. Make changes to `.github/workflows/ci-cd.yml`
2. Test locally using `python scripts/verify_pipeline.py`
3. Commit and push changes
4. Monitor the pipeline execution

### 7.3 Adding New Features

When adding new features:

1. Update the training scripts if needed
2. Add new API endpoints
3. Update tests in `scripts/test_api.py`
4. Update documentation
5. Test locally before pushing

## Step 8: Production Deployment

### 8.1 Using Docker Image

Once the pipeline creates a Docker image:

```bash
# Pull the latest image
docker pull YOUR_DOCKER_USERNAME/mlops-app:latest

# Run the container
docker run -p 8000:8000 YOUR_DOCKER_USERNAME/mlops-app:latest
```

### 8.2 Using Deployment Script

For easier deployment, use the provided deployment script:

```bash
# Set your Docker username
export DOCKER_USERNAME=your-username

# Run the deployment script
bash scripts/deploy.sh
```

The deployment script will:
- Pull the latest Docker image
- Stop any existing container
- Start a new container
- Test the API endpoints
- Show deployment status

### 8.2 Using GitHub Actions

The pipeline automatically:
- Builds the Docker image
- Pushes to Docker Hub
- Tests the container
- Provides deployment artifacts

## Success Criteria

Your setup is successful when:

✅ **Repository Structure**: All files are in the correct locations
✅ **CI/CD Pipeline**: Runs successfully on every push to main
✅ **Model Training**: Models are trained and saved
✅ **API Testing**: All API endpoints work correctly
✅ **Security**: No critical security issues found
✅ **Docker**: Image builds and pushes successfully
✅ **Documentation**: All guides are up to date

## Next Steps

After successful setup:

1. **Monitor Performance**: Track model performance over time
2. **Scale Infrastructure**: Consider Kubernetes for production
3. **Add Monitoring**: Implement comprehensive logging and monitoring
4. **Security Hardening**: Regular security audits
5. **Documentation**: Keep documentation updated

## Support

If you encounter issues:

1. Check the GitHub Actions logs for detailed error messages
2. Review the troubleshooting section above
3. Verify all prerequisites are met
4. Test locally using the verification script

---

**Congratulations!** Your MLOps pipeline is now ready for production use. 🎉 