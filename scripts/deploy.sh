#!/bin/bash

# Production Deployment Script
# This script helps deploy the MLOps application to production

set -e  # Exit on any error

echo "🚀 Starting Production Deployment..."

# Configuration
DOCKER_USERNAME=${DOCKER_USERNAME:-"your-docker-username"}
IMAGE_NAME="mlops-app"
TAG="latest"
PORT=8000

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    print_status "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running"
        exit 1
    fi
    
    print_status "Docker is ready"
}

# Pull the latest image
pull_image() {
    print_status "Pulling latest Docker image..."
    docker pull $DOCKER_USERNAME/$IMAGE_NAME:$TAG
    print_status "Image pulled successfully"
}

# Stop existing container
stop_existing() {
    print_status "Stopping existing container if running..."
    docker stop mlops-app 2>/dev/null || true
    docker rm mlops-app 2>/dev/null || true
    print_status "Existing container stopped"
}

# Start new container
start_container() {
    print_status "Starting new container..."
    docker run -d \
        --name mlops-app \
        -p $PORT:8000 \
        --restart unless-stopped \
        $DOCKER_USERNAME/$IMAGE_NAME:$TAG
    
    print_status "Container started with name 'mlops-app'"
}

# Wait for API to be ready
wait_for_api() {
    print_status "Waiting for API to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:$PORT/ &>/dev/null; then
            print_status "API is ready!"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - API not ready yet..."
        sleep 2
        ((attempt++))
    done
    
    print_error "API failed to start within expected time"
    return 1
}

# Test the API
test_api() {
    print_status "Testing API endpoints..."
    
    # Health check
    if curl -f http://localhost:$PORT/ &>/dev/null; then
        print_status "✅ Health check passed"
    else
        print_error "❌ Health check failed"
        return 1
    fi
    
    # Test prediction
    local test_response=$(curl -s -X POST http://localhost:$PORT/predict \
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
        }')
    
    if echo "$test_response" | grep -q "predicted_price"; then
        print_status "✅ Prediction endpoint working"
        print_status "Sample prediction: $test_response"
    else
        print_error "❌ Prediction endpoint failed"
        return 1
    fi
    
    return 0
}

# Show container status
show_status() {
    print_status "Container status:"
    docker ps --filter name=mlops-app --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    print_status "API endpoints:"
    echo "  Health: http://localhost:$PORT/"
    echo "  Predict: http://localhost:$PORT/predict"
    echo "  Metrics: http://localhost:$PORT/metrics"
}

# Main deployment function
deploy() {
    print_status "Starting deployment process..."
    
    check_docker
    pull_image
    stop_existing
    start_container
    wait_for_api
    test_api
    show_status
    
    print_status "🎉 Deployment completed successfully!"
    print_status "Your MLOps API is now running on http://localhost:$PORT"
}

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -u, --username DOCKER_USERNAME  Set Docker username"
    echo "  -p, --port     PORT             Set port (default: 8000)"
    echo "  -t, --tag      TAG              Set image tag (default: latest)"
    echo ""
    echo "Environment variables:"
    echo "  DOCKER_USERNAME  Your Docker Hub username"
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 -u myusername"
    echo "  $0 -u myusername -p 8080"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -u|--username)
            DOCKER_USERNAME="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if DOCKER_USERNAME is set
if [ "$DOCKER_USERNAME" = "your-docker-username" ]; then
    print_error "Please set DOCKER_USERNAME environment variable or use -u option"
    print_error "Example: export DOCKER_USERNAME=your-username"
    exit 1
fi

# Run deployment
deploy 