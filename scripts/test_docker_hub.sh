#!/bin/bash

# Docker Hub Authentication Test Script
# This script helps test if your Docker Hub credentials are working correctly

echo "🐳 Docker Hub Authentication Test"
echo "================================"

# Check if environment variables are set
if [ -z "$DOCKER_USERNAME" ]; then
    echo "❌ DOCKER_USERNAME environment variable not set"
    echo "Please set it: export DOCKER_USERNAME=your-username"
    exit 1
fi

if [ -z "$DOCKER_PASSWORD" ]; then
    echo "❌ DOCKER_PASSWORD environment variable not set"
    echo "Please set it: export DOCKER_PASSWORD=your-token"
    exit 1
fi

echo "✅ Environment variables are set"
echo "Username: $DOCKER_USERNAME"
echo "Password: [HIDDEN]"

# Test Docker Hub login
echo ""
echo "Testing Docker Hub login..."
if docker login -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD" 2>/dev/null; then
    echo "✅ Docker Hub login successful!"
else
    echo "❌ Docker Hub login failed!"
    echo ""
    echo "Possible issues:"
    echo "1. Invalid username or password"
    echo "2. Access token has insufficient scopes"
    echo "3. Account is not verified"
    echo ""
    echo "To fix:"
    echo "1. Go to https://hub.docker.com/settings/security"
    echo "2. Create a new access token with 'Read & Write' permissions"
    echo "3. Update your GitHub secrets with the new token"
    exit 1
fi

# Test if we can push to the repository
echo ""
echo "Testing repository access..."
if docker pull "$DOCKER_USERNAME/mlops-app:latest" 2>/dev/null; then
    echo "✅ Can pull from repository"
else
    echo "⚠️ Cannot pull from repository (might not exist yet)"
fi

echo ""
echo "🎉 Authentication test completed!"
echo "If login was successful, your credentials should work in the CI/CD pipeline." 